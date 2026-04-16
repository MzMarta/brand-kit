import json
import os

# Definir las rutas
TOKEN_FILE = 'design-tokens/brand.tokens.json'
DIST_DIR = 'dist'
CSS_FILE = os.path.join(DIST_DIR, 'tokens.css')
TS_FILE = os.path.join(DIST_DIR, 'tokens.ts')

# 1. Asegurar que existe la carpeta dist/
os.makedirs(DIST_DIR, exist_ok=True)

# 2. Leer el archivo JSON
with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
    tokens = json.load(f)

# Función auxiliar para convertir la estructura anidada en variables planas (ej: colors-primary-hex)
def flatten_json(y):
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '-')
        else:
            out[name[:-1]] = x
    flatten(y)
    return out

flat_tokens = flatten_json(tokens)

# 3. Generar el contenido CSS
css_content = "/* Archivo autogenerado a partir de brand.tokens.json */\n:root {\n"
for key, value in flat_tokens.items():
    css_content += f"  --{key}: {value};\n"
css_content += "}\n"

with open(CSS_FILE, 'w', encoding='utf-8') as f:
    f.write(css_content)

# 4. Generar el contenido TypeScript
# Convertimos el diccionario de Python de vuelta a texto JSON para TypeScript
ts_content = "/* Archivo autogenerado a partir de brand.tokens.json */\n"
ts_content += f"export const tokens = {json.dumps(tokens, indent=2)};\n"

with open(TS_FILE, 'w', encoding='utf-8') as f:
    f.write(ts_content)

print("✅ ¡Éxito! Archivos CSS y TS generados en la carpeta dist/")

# 5. Generar configuración para Tailwind CSS (Extensión 1)
TAILWIND_FILE = os.path.join(DIST_DIR, 'tailwind.config.js')

# Extraemos solo los colores para inyectarlos en Tailwind
colores_tailwind = json.dumps(tokens.get("colors", {}), indent=4)

tailwind_content = f"""/** @type {{import('tailwindcss').Config}} */
module.exports = {{
  content: ["./**/*.{{html,js,ts,jsx,tsx,md}}"],
  theme: {{
    extend: {{
      colors: {colores_tailwind}
    }}
  }},
  plugins: [],
}}
"""

with open(TAILWIND_FILE, 'w', encoding='utf-8') as f:
    f.write(tailwind_content)

print("✅ ¡Extra! Archivo tailwind.config.js generado en dist/")