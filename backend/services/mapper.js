const fs = require('fs');
const path = require('path');

// Cargar los datos sincrónicamente al iniciar
const countries = JSON.parse(fs.readFileSync(path.join(__dirname, '../data/countries.json'), 'utf-8'));
const genres = JSON.parse(fs.readFileSync(path.join(__dirname, '../data/genres.json'), 'utf-8'));
const musicData = JSON.parse(fs.readFileSync(path.join(__dirname, '../data/musicData.json'), 'utf-8'));

function processVisionData(x, y, genreId) {
  let activeCountryId = null; 
  let activeCountryName = null;
  let activeGenre = genres[genreId] || null;

  // 1. Encontrar en qué país está el puntero
  for (const country of countries) {
    if (
      x >= country.bounds.minX && x <= country.bounds.maxX &&
      y >= country.bounds.minY && y <= country.bounds.maxY
    ) {
      activeCountryId = country.id;      // <-- CLAVE: Usamos el ID (Ej: "CL") para buscar en la base de datos
      activeCountryName = country.name;  // Guardamos el nombre para la web
      break;
    }
  }

  // 2. Buscar la información musical usando el ID del país
  let trackInfo = null;
  if (activeCountryId && activeGenre && musicData[activeCountryId] && musicData[activeCountryId][activeGenre]) {
    trackInfo = musicData[activeCountryId][activeGenre];
  }

  // 3. Retornar el estado completo listo para React
  return {
    pointer: { x, y },
    country: activeCountryName, // Enviamos el nombre bonito ("Chile")
    genre: activeGenre,
    music: trackInfo
  };
}

module.exports = { processVisionData };