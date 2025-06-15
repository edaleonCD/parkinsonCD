import torch
import torchaudio
from transformers import Pipeline
from librosa import resample
from soundfile import write
from sgmse.model import ScoreModel
from sgmse.util.other import pad_spec

class CustomSpeechEnhancementPipeline(Pipeline):
    def __init__(self, model, target_sr=16000, pad_mode="zero_pad", args=None):
        """
        Custom pipeline for speech enhancement using ScoreModel.

        Args:
            model: The speech enhancement model loaded from a checkpoint (ScoreModel).
            target_sr: Target sample rate for the input audio (default is 16 kHz).
            pad_mode: Padding mode for spectrogram (default is "zero_pad").
            args: Parsed arguments (device, corrector, corrector_steps, snr, etc.).
        """
        super().__init__(model=model)
        self.target_sr = target_sr
        self.pad_mode = pad_mode
        self.args = args

    def preprocess(self, audio_path):
        # Load the audio file
        y, sr = torchaudio.load(audio_path)

        # Resample if necessary
        if sr != self.target_sr:
            y = torch.tensor(resample(y.numpy(), orig_sr=sr, target_sr=self.target_sr))

        # Normalize the audio
        norm_factor = y.abs().max()
        y = y / norm_factor

        # Prepare the input for the model by transforming to the frequency domain
        Y = torch.unsqueeze(self.model._forward_transform(self.model._stft(y.to(self.args.device))), 0)
        Y = pad_spec(Y, mode=self.pad_mode)

        return Y, norm_factor, y.size(1)  # Return input spec, normalization factor, and original length

    def _forward(self, model_inputs):
        Y, norm_factor, T_orig = model_inputs

        # Perform reverse sampling using the model's PC sampler
        sampler = self.model.get_pc_sampler(
            'reverse_diffusion', 
            self.args.corrector, 
            Y.to(self.args.device), 
            N=self.args.N, 
            corrector_steps=self.args.corrector_steps, 
            snr=self.args.snr
        )

        # Get the enhanced speech sample
        sample, _ = sampler()

        # Convert back to time domain
        x_hat = self.model.to_audio(sample.squeeze(), T_orig)

        # Renormalize the audio
        x_hat = x_hat * norm_factor

        return x_hat

    def postprocess(self, model_outputs):
        # Convert the enhanced output back to NumPy for further processing or saving
        return model_outputs.cpu().numpy()

    def pad_spec(self, Y):
        """
        Apply padding to the spectrogram as per the model's required padding mode.

        Args:
            Y: Input spectrogram tensor.

        Returns:
            Padded spectrogram.
        """
        # Implement padding as per the provided mode
        return torch.nn.functional.pad(Y, (0, 0, 0, 1), mode=self.pad_mode)
