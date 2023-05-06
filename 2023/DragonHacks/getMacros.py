from requests import get
from sys import exit


def searchFoodItem(query):
    HTTP_URL = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/ingredients/search"
    querystring = {"query": query}
    HTTP_HEADERS = {
        "X-RapidAPI-Key": "73d82610b7msheaba598fed24841p1e0f71jsn6bfe6217691f",
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    }
    HTTP_RESPONSE = get(HTTP_URL, headers=HTTP_HEADERS, params=querystring)
    HTTP_RESPONSE_JSON = HTTP_RESPONSE.json()
    HTTP_RESULTS = HTTP_RESPONSE_JSON["results"]
    if HTTP_RESULTS:
        return HTTP_RESULTS[0]["id"]
    else:
        return None


def getIngredientNutrition(ingredientId, amount, unit):
    HTTP_URL = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/ingredients/{ingredientId}/information"
    querystring = {"amount": amount, "unit": unit}
    HTTP_HEADERS = {
        "content-type": "application/octet-stream",
        "X-RapidAPI-Key": "73d82610b7msheaba598fed24841p1e0f71jsn6bfe6217691f",
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    }
    HTTP_RESPONSE = get(HTTP_URL, headers=HTTP_HEADERS, params=querystring)
    if HTTP_RESPONSE.status_code == 200:
        HTTP_RESPONSE_JSON = HTTP_RESPONSE.json()
        nutrition = HTTP_RESPONSE_JSON.get("nutrition")
        return nutrition
    else:
        print("Unable to fetch data from website, Exiting...")
        exit(0)


def getIngredientNutritionInfo(ingredientId, amount, unit):
    nutrition = getIngredientNutrition(ingredientId, amount, unit)

    nutrients = {}
    for nutrient in nutrition["nutrients"]:
        nutrients[nutrient["name"]] = nutrient["amount"]

    calories = nutrients.get("Calories", 0)
    carbs = nutrients.get("Carbohydrates", 0)
    sugars = nutrients.get("Sugars", 0)
    fibre = nutrients.get("Fiber", 0)
    netCarbs = nutrients.get("Net Carbohydrates", 0)
    protein = nutrients.get("Protein", 0)
    fats = nutrients.get("Fat", 0)

    macroInfo = [calories, carbs, sugars, fibre, netCarbs, protein, fats]

    return macroInfo


def displayResults(macroList):
    displayResults = f"""    > Energy: {macroList[0]:.02f} Kcals
    > Carbohydrates: {macroList[1]:.02f} g
       > Sugars: {macroList[2]:.02f} g
       > Fibre: {macroList[3]:.02f} g
       > Net Carbohydrates: {macroList[4]:.02f} g
    > Protein: {macroList[5]:.02f} g
    > Fats: {macroList[6]:.02f} g
    """

    return displayResults
