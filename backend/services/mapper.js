const fs = require('fs');
const path = require('path');

// Cargar los datos sincrónicamente al iniciar
const countries = JSON.parse(fs.readFileSync(path.join(__dirname, '../data/countries.json'), 'utf-8'));
const genres = JSON.parse(fs.readFileSync(path.join(__dirname, '../data/genres.json'), 'utf-8'));
const musicData = JSON.parse(fs.readFileSync(path.join(__dirname, '../data/musicData.json'), 'utf-8'));

function processVisionData(x, y, genreId) {
  let activeCountry = null;
  let activeGenre = genres[genreId] || null;

  // 1. Encontrar en qué país está el puntero
  for (const country of countries) {
    if (
      x >= country.bounds.minX && x <= country.bounds.maxX &&
      y >= country.bounds.minY && y <= country.bounds.maxY
    ) {
      activeCountry = country.name;
      break;
    }
  }

  // 2. Buscar la información musical si tenemos ambos datos
  let trackInfo = null;
  if (activeCountry && activeGenre && musicData[activeCountry] && musicData[activeCountry][activeGenre]) {
    trackInfo = musicData[activeCountry][activeGenre];
  }

  // 3. Retornar el estado completo listo para React
  return {
    pointer: { x, y },
    country: activeCountry,
    genre: activeGenre,
    music: trackInfo
  };
}

module.exports = { processVisionData };