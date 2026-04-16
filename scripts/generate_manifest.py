import os
import hashlib
import json

# Rutas
ASSETS_DIR = 'assets/brand/upstream'
MANIFEST_FILE = 'assets-manifest.json'

def calculate_sha256(filepath):
    """Calcula la huella digital (SHA256) de un archivo."""
    sha256_hash = hashlib.sha256()
    # Leemos el archivo en bloques para no saturar la memoria si la imagen es muy grande
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def main():
    print("🔒 Escaneando imágenes y calculando huellas digitales (SHA256)...")
    manifest = {}
    
    if not os.path.exists(ASSETS_DIR):
        print(f"⚠️ No se encontró la carpeta {ASSETS_DIR}")
        return

    # Escanear archivos en la carpeta de assets
    for filename in os.listdir(ASSETS_DIR):
        filepath = os.path.join(ASSETS_DIR, filename)
        
        if os.path.isfile(filepath):
            file_hash = calculate_sha256(filepath)
            # Guardamos la ruta relativa y su hash
            manifest[f"upstream/{filename}"] = file_hash
            print(f"  ✓ {filename} -> {file_hash[:8]}...") # Mostramos solo los primeros 8 caracteres en consola

    # Guardar el resultado en un archivo JSON
    with open(MANIFEST_FILE, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
        
    print(f"\n✅ ¡Manifiesto de seguridad generado con éxito en {MANIFEST_FILE}!")

if __name__ == '__main__':
    main()