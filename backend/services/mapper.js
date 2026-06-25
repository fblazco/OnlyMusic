const fs = require('fs');
const path = require('path');

// Cargar los datos sincrónicamente al iniciar
const countries = JSON.parse(fs.readFileSync(path.join(__dirname, '../data/countries.json'), 'utf-8'));
const genres = JSON.parse(fs.readFileSync(path.join(__dirname, '../data/genres.json'), 'utf-8'));
const musicData = JSON.parse(fs.readFileSync(path.join(__dirname, '../data/musicData.json'), 'utf-8'));
const qData = JSON.parse(fs.readFileSync(path.join(__dirname, '../data/musicCategories.json'), 'utf-8'));

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
      activeCountryId = country.id;      
      activeCountryName = country.name;  
      break;
    }
  }

  // 2. Buscar la info musical y la categoría
  let trackInfo = null;
  let activeCategory = null; // NUEVA VARIABLE

  if (activeCountryId && activeGenre) {
    // Info del top 10
    if (musicData[activeCountryId] && musicData[activeCountryId][activeGenre]) {
      trackInfo = musicData[activeCountryId][activeGenre];
    }
    // Categoría del cuartil
    if (qData[activeCountryId] && qData[activeCountryId][activeGenre]) {
      activeCategory = qData[activeCountryId][activeGenre].category;
    }
  }

  // 3. Retornar el estado completo listo para React
  return {
    pointer: { x, y },
    country: activeCountryName, 
    genre: activeGenre,
    music: trackInfo,
    category: activeCategory // NUEVO DATO ENVIADO AL FRONTEND
  };
}

module.exports = { processVisionData };