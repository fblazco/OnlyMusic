import json
from collections import defaultdict
import random

# 1. Cargar los países directamente desde tu countries.json
with open('countries.json', 'r', encoding='utf-8') as f:
    countries_data = json.load(f)

# Extraemos solo los IDs de los países (CL, AR, BR, etc.)
paises_mapa = [c["id"] for c in countries_data]

# 2. Cargar la data musical limpia
with open('/Users/felipeblasquezcontreras/Desktop/Archivos/2026-1/InfoVis/OnlyMusic/data/sources/clean/data_resumida_limpia.json', 'r', encoding='utf-8') as f:
    datos = json.load(f)

# Estructuras para procesar
datos_procesados = defaultdict(lambda: defaultdict(lambda: {"tracks": [], "total_streams": 0}))
todos_los_generos = set()

# 3. Procesar las canciones reales y recolectar todos los géneros que existen
for fila in datos[1:]:
    streams = int(fila[0])
    track_name = fila[1]
    artist = fila[2]
    genre = fila[3]
    country = fila[4]
    
    # Guardamos el género en nuestro set global para saber cuántos existen en total
    todos_los_generos.add(genre)
    
    if country in paises_mapa:
        datos_procesados[country][genre]["tracks"].append({
            "name": track_name,
            "artist": artist,
            "streams": streams,
            "genre": genre
        })
        datos_procesados[country][genre]["total_streams"] += streams

lista_generos_global = list(todos_los_generos)

# 4. Generar la estructura final (Todos los países x Todos los géneros)
music_data_final = {}

# Diccionario de artistas falsos para darle realismo a los mocks
artistas_falsos = {
    "CL": ["Los Prisioneros", "Mon Laferte", "Los Bunkers", "Cris MJ", "Paloma Mami"],
    "AR": ["Soda Stereo", "Duki", "Bizarrap", "Charly García", "Tini"],
    "BR": ["Anitta", "João Gilberto", "Caetano Veloso", "Jorge Ben Jor", "Ludmilla"],
    "PE": ["Gian Marco", "Grupo 5", "Los Mirlos", "Pedro Suárez-Vértiz", "Daniela Darcourt"],
    "CO": ["J Balvin", "Shakira", "Carlos Vives", "Feid", "Karol G"],
    "MX": ["Peso Pluma", "Luis Miguel", "Café Tacvba", "Christian Nodal", "Danna Paola"],
    "ES": ["Rosalía", "C. Tangana", "Héroes del Silencio", "Alejandro Sanz", "Quevedo"],
    "FR": ["Daft Punk", "Stromae", "Edith Piaf", "Justice", "David Guetta"],
    "DE": ["Rammstein", "Kraftwerk", "Scorpions", "Robin Schulz", "Zedd"],
    "NG": ["Burna Boy", "Wizkid", "Davido", "Fela Kuti", "Rema"],
    "ZA": ["Die Antwoord", "Master KG", "Miriam Makeba", "Tyla", "Black Coffee"],
    "EG": ["Amr Diab", "Sherine", "Tamer Hosny", "Umm Kulthum", "Mohamed Ramadan"],
    "RU": ["t.A.T.u.", "Oxxxymiron", "Morgenshtern", "Little Big", "Zivert"],
    "CN": ["Jay Chou", "Faye Wong", "Teresa Teng", "G.E.M.", "Jackson Wang"],
    "IN": ["A.R. Rahman", "Arijit Singh", "Badshah", "Lata Mangeshkar", "Diljit Dosanjh"],
    "JP": ["Kenshi Yonezu", "Utada Hikaru", "BABYMETAL", "YOASOBI", "Ado"],
    "US": ["Taylor Swift", "Kendrick Lamar", "Billie Eilish", "Bruno Mars", "Drake"],
    "GB": ["Harry Styles", "Coldplay", "Arctic Monkeys", "Ed Sheeran", "Adele"],
    "KR": ["BTS", "BLACKPINK", "NewJeans", "Stray Kids", "TWICE"]
}

# Iteramos sobre todos los países del mapa
for pais in paises_mapa:
    music_data_final[pais] = {}
    
    # Artistas base para inventar en caso de no tener reales
    artistas_locales = artistas_falsos.get(pais, [f"Artista de {pais}", f"Banda Local {pais}", f"DJ {pais}"])
    
    # Iteramos sobre ABSOLUTAMENTE TODOS los géneros descubiertos
    for genero in lista_generos_global:
        
        # Si el país tiene datos reales para este género específico
        if pais in datos_procesados and genero in datos_procesados[pais] and len(datos_procesados[pais][genero]["tracks"]) > 0:
            
            data_genero = datos_procesados[pais][genero]
            canciones_ordenadas = sorted(data_genero["tracks"], key=lambda x: x["streams"], reverse=True)
            
            music_data_final[pais][genero] = {
                "total_streams": data_genero["total_streams"],
                "top_10": canciones_ordenadas[:10],
                "is_mock": False
            }
            
        else:
            # Si no hay datos, inventamos un Top 10 para este país y este género
            top_10_falso = []
            total_streams_falso = 0
            
            for i in range(10):
                # Generamos streams aleatorios decrecientes para que tenga sentido el "Top"
                streams = random.randint(100000, 5000000) // (i + 1) 
                total_streams_falso += streams
                top_10_falso.append({
                    "name": f"Pista {i+1} de {genero}",
                    "artist": random.choice(artistas_locales),
                    "streams": streams,
                    "genre": genero
                })
            
            music_data_final[pais][genero] = {
                "total_streams": total_streams_falso,
                "top_10": top_10_falso,
                "is_mock": True
            }

# 5. Guardar el resultado en el JSON definitivo
ruta_salida = 'musicData.json'
with open(ruta_salida, 'w', encoding='utf-8') as f:
    json.dump(music_data_final, f, ensure_ascii=False, indent=4)

print(f"¡Procesamiento terminado! Se cruzaron {len(paises_mapa)} países con {len(lista_generos_global)} géneros.")
print(f"Archivo guardado en {ruta_salida}")