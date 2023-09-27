document.getElementById('getRecipesBtn').addEventListener('click', async function () {
    await fetchRecipes();
  });
  
  async function fetchRecipes() {
    const appId = 'e77a7c29';
    const apiKey = '9f79c43f360b8bb14fa25c6068bdaf5a';
    const ingredientInput = document.getElementById('ingredient');
    const ingredient = ingredientInput.value.trim();
  
    if (!ingredient) {
      alert('Please enter an ingredient.');
      return;
    }
  
    const link = `https://api.edamam.com/search?q=${ingredient}&app_id=${appId}&app_key=${apiKey}`;
  
    try {
      const response = await fetch(link);
      const data = await response.json();
      displayRecipes(data.hits);
    } 
    catch (error) {
      console.error('Error fetching data:', error);
    }
  }
  
  function displayRecipes(recipeData) {
    const recipeList = document.getElementById('recipeList');
    recipeList.innerHTML = '';
  
    if (recipeData.length === 0) {
      recipeList.innerHTML = '<p>No recipes found.</p>';
      return;
    }
  
    for (let index = 0; index < recipeData.length; index++) {
      var recipe = recipeData[index];
      var recipeName = recipe.recipe.label;
      var recipeLink = recipe.recipe.url;
      var listItem = document.createElement('li');
      listItem.innerHTML = `<a href="${recipeLink}" target="_blank">${recipeName}</a>`;
      recipeList.appendChild(listItem);
    }
  }