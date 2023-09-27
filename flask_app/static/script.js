async function fetchNutritionData(measurement, foodItem) {
    const appId = '8bfb3c09';
    const appKey = '364ddd2be45ca29c06eb966b3e6889ed';
  
    try {
      const response = await fetch(`https://api.edamam.com/api/nutrition-data?app_id=${appId}&app_key=${appKey}&ingr=${encodeURIComponent(measurement + ' ' + foodItem)}`);
      const data = await response.json();
      console.log(data); 
      return data;
    } 
    catch (error) {
      console.error('Error retrieving data:', error);
      return null;
    }
  }


  function displayNutritionData(nutritionData) {
    const nutritionInfoDiv = document.getElementById('nutritionInfo');
    if (nutritionData) {
      const { calories, dietLabels, totalCO2Emissions, totalWeight } = nutritionData;
      const fats = nutritionData.totalNutrients.FAT.quantity.toFixed(2)
      const protein = nutritionData.totalNutrients.PROCNT.quantity.toFixed(2)
      const nutritionInfoHTML = `
        <h2>Nutritional Information</h2>
        <p>Calories: ${calories}</p>
        <p>Total CO2 Emissions: ${totalCO2Emissions}</p>
        <p>Total Weight: ${totalWeight} g</p>
        <p>Fats: ${fats} g</p>
        <p>Protein: ${protein} g</p>
        <p>Diet Labels: ${dietLabels.join(', ')}</p>`;

      nutritionInfoDiv.innerHTML = nutritionInfoHTML;
    } 
    else {
      alert('<p>Nutritional data not found</p>');
    }
  }
  
  async function getNutritionData() {
    const measurement = document.getElementById('inputMeasurement').value;
    const foodItem = document.getElementById('inputFood').value;
  
    if (measurement === '' || foodItem === '') {
      alert('Please enter both the measurement and the food item.');
      return;
    }
  
    const nutritionData = await fetchNutritionData(measurement, foodItem);
    displayNutritionData(nutritionData);
  }
