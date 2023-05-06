from getMacros import searchFoodItem, getIngredientNutritionInfo, displayResults
from fetchIngredient import (
    getIngredients,
    separateQuantity,
    removeExtra,
    separateServings,
    removeOthers,
    removePreparations,
    addLists,
    getAverageServings,
    getTitle,
)
from aiIntegration import getHealth

if __name__ == "__main__":
    pageURL = input("Please enter the URL of the recipe you wish to get: ")

    recipeTitle = getTitle(pageURL)[0]

    print("\n~ ~ DEMETER ~ ~")
    print("Displaying Ingredients for " + recipeTitle + ".\n")
    print("Link to recipe: " + pageURL)

    ingredientList = getIngredients(pageURL)
    servingCount = getAverageServings(pageURL)
    ingredientList.remove("Deselect All")
    quantityList, remainderList = separateQuantity(ingredientList)
    remainderList = removeExtra(remainderList)
    servingsList, remainderList = separateServings(remainderList)
    remainderList = removeOthers(remainderList)
    ingredientList = []

    for i in range(0, len(remainderList)):
        ingredientList.append(
            [
                remainderList[i],
                quantityList[i],
                servingsList[i],
            ]
        )

    totalMacros = [0, 0, 0, 0, 0, 0, 0]
    for ingredient in ingredientList:
        itemName = ingredient[0]
        itemID = searchFoodItem(itemName)
        count = 0

        while itemID == None and count < 3:
            itemName = removePreparations(itemName)
            itemID = searchFoodItem(itemName)
            count += 1

        if count == 3 and itemID == None:
            itemName = itemName.split()
            if len(itemName) >= 3:
                itemName = f"{itemName[0]} {itemName[2]}"
            elif len(itemName) == 2:
                itemName = f"{itemName[0]}"
            else:
                itemName = f"{itemName[0]}"
            itemID = searchFoodItem(itemName)
            count += 1

        if itemID == None:
            # print(itemName.title(), "is not searchable in the database, ignoring it.")
            continue

        itemQuantity = ingredient[1]
        itemUnits = ingredient[2]
        print(
            f"{itemID:>10} | {itemName.title():>25.25s} | {itemQuantity:>5.2f} | {itemUnits.title()}"
        )
        macroCount = getIngredientNutritionInfo(itemID, itemQuantity, itemUnits)
        totalMacros = addLists(macroCount, totalMacros)

    print("\nNUTRITIONAL INFORMATION:")
    print(displayResults(totalMacros))
    print("NUMBER OF SERVINGS:", servingCount, "\n")

    macroPerServing = [
        totalMacros[0] // servingCount,
        totalMacros[1] / servingCount,
        totalMacros[2] / servingCount,
        totalMacros[3] / servingCount,
        totalMacros[4] / servingCount,
        totalMacros[5] / servingCount,
        totalMacros[6] / servingCount,
    ]
    print("NUTRITION PER SERVING:")
    print(displayResults(macroPerServing))

    foodStatus, foodAlternative = getHealth(recipeTitle, macroPerServing)
    if "unhealthy" in foodStatus.lower():
        print(f"This recipe is unhealthy, consider having {foodAlternative} instead!")
    else:
        print(
            f"This recipe is relatively healthy, and would be a great fit for {foodStatus}!"
        )
