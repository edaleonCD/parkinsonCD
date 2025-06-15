import sys
import os
import torch
from torch.serialization import add_safe_globals

# 1. Añadir la ruta del proyecto a sys.path
repo_path = r"C:\Users\leonl_4g2zj04\Documents\CD\repositories\speech-enhancement-sgmse"
sys.path.append(repo_path)

# 2. Importar la clase que se necesita para cargar el checkpoint
from sgmse.data_module import SpecsDataModule

# 3. Agregar clase permitida explícitamente
add_safe_globals({'sgmse.data_module.SpecsDataModule': SpecsDataModule})

# 4. Ruta del checkpoint
ckpt_path = os.path.join(repo_path, "train_vb_29nqe0uh_epoch=115.ckpt")

# 5. Cargar el checkpoint completo
checkpoint = torch.load(
    ckpt_path,
    map_location="cpu",
    weights_only=False  # Esto es lo que habilita la deserialización completa
)

# 6. Verificar contenido
print("Checkpoint cargado correctamente.")
print("Claves principales:", list(checkpoint.keys()))
