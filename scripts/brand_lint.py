import os
import sys

# 1. Configuración de términos prohibidos
FORBIDDEN_TERMS = [
    "Navantia Coex",              # Mal uso de mayúsculas
    "Centro Excelencia Navantia", # Nomenclatura no oficial
    "DigitalTwin",                # Falta de espacio
    "Navantia DT",                # Abreviatura prohibida
    "M-COM-001",                  # Referencia a PDF confidencial
    ".pdf",                       # Uso de archivos PDF en código
    "docs/internal/"              # Referencia a carpeta interna
]

# 2. Configuración de escaneo
ALLOWED_EXTENSIONS = ('.md', '.ts', '.tsx', '.css', '.html', '.js')

# Archivos y carpetas a ignorar (porque definen las reglas o son autogenerados)
IGNORED_FILES = ['IDENTIDAD.md', 'AI_CONTEXT.md', 'NOTICE.md', 'README.md']
IGNORED_DIRS = ['.git', 'node_modules', 'dist', 'scripts', 'assets']

def check_file(filepath):
    errors_found = 0
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line_number, line in enumerate(lines, 1):
                for term in FORBIDDEN_TERMS:
                    if term in line:
                        print(f"❌ Error en {filepath} (Línea {line_number}): Contiene el término prohibido '{term}'")
                        errors_found += 1
    except Exception as e:
        print(f"⚠️ No se pudo leer {filepath}: {e}")
    
    return errors_found

def main():
    total_errors = 0
    print("🔍 Iniciando Brand Linter de Navantia COEX...")

    for root, dirs, files in os.walk('.'):
        # Filtrar carpetas ignoradas
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for file in files:
            if file.endswith(ALLOWED_EXTENSIONS) and file not in IGNORED_FILES:
                filepath = os.path.join(root, file)
                total_errors += check_file(filepath)

    if total_errors > 0:
        print(f"\n💥 Linter falló: Se encontraron {total_errors} violaciones de marca.")
        sys.exit(1) # Falla el script (útil para pipelines CI/CD)
    else:
        print("\n✅ Linter aprobado: No se encontraron violaciones de marca.")
        sys.exit(0) # Script exitoso

if __name__ == '__main__':
    main()