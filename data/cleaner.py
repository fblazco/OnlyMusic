import json

# Diccionario de correcciones (lo mantenemos por si acaso hay datos ocultos más abajo)
correcciones = {
    "Culiacán": "MX",
    "Monterrey": "MX",
    "Florida": "US",
    "England": "GB"
}

# 1. Cargar el JSON resumido crudo
# Asegúrate de que el nombre del archivo calce con el que tienes en /raw/
with open('./sources/raw/data_resumida_1.json', 'r', encoding='utf-8') as f:
    datos = json.load(f)

# 2. Guardamos los encabezados
encabezados = datos[0]
datos_limpios = [encabezados]

# 3. Iterar sobre las filas
for fila in datos[1:]:
    # En data_resumida, el país está en el índice 4
    pais_actual = fila[4]
    
    # Aplicar corrección si es necesario
    if pais_actual in correcciones:
        fila[4] = correcciones[pais_actual]
        
    datos_limpios.append(fila)

# 4. Guardar el nuevo JSON limpio
with open('./sources/clean/data_resumida_limpia.json', 'w', encoding='utf-8') as f:
    json.dump(datos_limpios, f, ensure_ascii=False, indent=4)

print("¡Limpieza terminada! Archivo guardado en ./sources/clean/data_resumida_limpia.json")