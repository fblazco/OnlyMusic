import json

# ===========================
# Cargar datos
# ===========================
with open("musicData.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ===========================
# Obtener todos los streams
# ===========================
all_streams = []

for genres in data.values():
    for details in genres.values():
        if isinstance(details, dict) and "total_streams" in details:
            all_streams.append(details["total_streams"])

all_streams.sort()

n = len(all_streams)

# Cuartiles
p25 = all_streams[int(0.25 * n)]
p50 = all_streams[int(0.50 * n)]
p75 = all_streams[int(0.75 * n)]

print("Cuartiles encontrados:")
print(f"P25: {p25:,}")
print(f"P50: {p50:,}")
print(f"P75: {p75:,}")
print()

# ===========================
# Clasificar
# ===========================
output = {}

category_count = {
    "Bajo": 0,
    "Medio-bajo": 0,
    "Medio-alto": 0,
    "Alto": 0
}

for country, genres in data.items():

    output[country] = {}

    for genre, details in genres.items():

        if not isinstance(details, dict):
            continue

        streams = details.get("total_streams")

        if streams is None:
            continue

        if streams < p25:
            category = "Bajo"
        elif streams < p50:
            category = "Medio-bajo"
        elif streams < p75:
            category = "Medio-alto"
        else:
            category = "Alto"

        category_count[category] += 1

        output[country][genre] = {
            "total_streams": streams,
            "category": category
        }

# ===========================
# Guardar JSON
# ===========================
with open("musicCategories.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=4)

# ===========================
# Resumen
# ===========================
print(f"Se procesaron {len(output)} países.")

total = sum(len(g) for g in output.values())

print(f"Se procesaron {total} géneros.\n")

print("Conteo por categoría:")
for category, count in category_count.items():
    print(f"{category:12}: {count:4} ({count/total*100:5.1f}%)")