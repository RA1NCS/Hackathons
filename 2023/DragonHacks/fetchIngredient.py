from requests import get
from bs4 import BeautifulSoup


def getTitle(pageURL):
    HTTP_RESPONSE = get(pageURL)
    if HTTP_RESPONSE.status_code != 200:
        return ["Webpage not found."]
    GET_HTML = BeautifulSoup(HTTP_RESPONSE.text, "html.parser")
    titleListHTML = GET_HTML.find("div", class_="assetTitle")
    if not titleListHTML:
        return ["Webpage Title Found."]
    return [
        span.get_text(strip=True)
        for span in titleListHTML.find_all(
            "span", class_="o-AssetTitle__a-HeadlineText"
        )
    ]


def getServingCount(pageURL):
    HTTP_RESPONSE = get(pageURL)
    if HTTP_RESPONSE.status_code != 200:
        return ["Webpage not found."]
    GET_HTML = BeautifulSoup(HTTP_RESPONSE.text, "html.parser")
    ServingListHTML = GET_HTML.find("div", class_="o-RecipeInfo")
    if not ServingListHTML:
        return ["Servings Not Found."]
    return [
        span.get_text(strip=True)
        for span in ServingListHTML.find_all(
            "span", class_="o-RecipeInfo__a-Description"
        )
    ]


def getAverageServings(pageURL):
    servingRange = []
    totalCount = 0
    servingCountString = getServingCount(pageURL)[-1]

    for word in servingCountString.split():
        if word.isdigit():
            servingRange.append(int(word))

    rangeLength = len(servingRange)
    for i in range(0, rangeLength):
        totalCount += servingRange[i]

    averageServings = totalCount // rangeLength
    return averageServings


def fetchIngredients(pageURL):
    HTTP_RESPONSE = get(pageURL)
    if HTTP_RESPONSE.status_code != 200:
        return ["Webpage not found."]
    GET_HTML = BeautifulSoup(HTTP_RESPONSE.text, "html.parser")
    ingredientListHTML = GET_HTML.find("div", class_="o-Ingredients__m-Body")
    if not ingredientListHTML:
        return ["Ingredients Not Found."]
    return [
        span.get_text(strip=True)
        for span in ingredientListHTML.find_all(
            "span", class_="o-Ingredients__a-Ingredient--CheckboxLabel"
        )
    ]


def getIngredients(pageURL):
    while True:
        functionResponse = fetchIngredients(pageURL)
        if functionResponse[0] == "Webpage not found.":
            print("Webpage not found, please check the link entered. ")
        elif functionResponse[0] == "Ingredients Not Found.":
            print(
                "Couldn't find ingredients from link, please enter a different one from foodnetwork.com. "
            )
        else:
            return functionResponse


def isFraction(word):
    return (
        float(int(word[0]) / int(word[2]))
        if len(word) == 3 and word[1] == "/"
        else False
    )


def separateQuantity(ingredientList):
    quantityList = []
    remainderList = []
    for ingredient in ingredientList:
        ingredient = ingredient.strip()
        words = ingredient.split()
        foundCheck = False
        emptyLine = True
        totalAmount = 0
        remainder = ""
        for word in words:
            floatCheck = isFraction(word)

            if foundCheck == False:
                if word.isdigit():
                    totalAmount += int(word)
                    emptyLine = False
                elif isinstance(floatCheck, float):
                    totalAmount += floatCheck
                    emptyLine = False
                else:
                    foundCheck = True
                    remainder += word + " "
            else:
                remainder += word + " "

        if emptyLine == False:
            quantityList.append(totalAmount)
            remainderList.append(remainder.strip())

    return quantityList, remainderList


def removeExtra(ingredientList):
    newList = []
    for ingredient in ingredientList:
        if "(" not in ingredient:
            newList.append(ingredient)
        else:
            start = ingredient.find("(")
            end = ingredient.find(")")
            newLine = ingredient[:start] + ingredient[end + 2 :]
            newList.append(newLine)
    return newList


def separateServings(ingredientList):
    quantityList = (
        "pound",
        "pounds",
        "ounce",
        "ounces",
        "cup",
        "cups",
        "pint",
        "large",
        "pints",
        "quart",
        "quarts",
        "gallon",
        "gallons",
        "teaspoon",
        "teaspoons",
        "tablespoon",
        "tablespoons",
        "fluid ounce",
        "fluid ounces",
        "milliliter",
        "milliliters",
        "liter",
        "liters",
        "slice",
        "slices",
        "piece",
        "pieces",
        "package",
        "packages",
        "can",
        "cans",
        "jar",
        "jars",
        "bottle",
        "bottles",
        "bunch",
        "bunches",
        "bag",
        "bags",
        "box",
        "boxes",
        "roll",
        "rolls",
        "stick",
        "sticks",
        "whole",
        "halves",
        "quarters",
        "container",
        "containers",
    )

    servingsList = []
    remainderList = []

    for ingredient in ingredientList:
        ingredient = ingredient.split()
        found = False
        for serving in quantityList:
            if serving in ingredient:
                ingredient.remove(serving)
                remainderList.append(ingredient)
                servingsList.append(serving)
                found = True
                break
        if not found:
            remainderList.append(ingredient)
            servingsList.append("units")

    return servingsList, remainderList


def removePreparations(ingredient):
    techniqueList = (
        "chopped ",
        "basic ",
        "diced ",
        "grated ",
        "minced ",
        "sliced ",
        "shredded ",
        "julienned ",
        "cubed ",
        "crushed ",
        "mashed ",
        "pureed ",
        "whipped ",
        "beaten ",
        "melted ",
        "softened ",
        "creamed ",
        "chilled ",
        "frozen ",
        "thawed ",
        "toasted ",
        "roasted ",
        "grilled ",
        "fried ",
        "sautéed ",
        "baked ",
        "boiled ",
        "steamed ",
        "poached ",
        "braised ",
        "marinated ",
        "seasoned ",
        "flavored ",
        "dried ",
        "soaked ",
        "rinsed ",
        "drained ",
        "blanched ",
        "unpeeled " "peeled ",
        "cored ",
        "seeded ",
        "deveined ",
        "trimmed ",
        "halved ",
        "quartered ",
        "whole ",
        "ground ",
        "powdered ",
        "fermented ",
        "leaf ",
        "freshly ",
        "fresh ",
        "sprigs ",
        "stripped ",
        "and ",
        "finely ",
        "chopped ",
        "small ",
        "good ",
    )

    for technique in techniqueList:
        if technique in ingredient:
            ingredient = ingredient.replace(technique, "")
    return ingredient


def removeOthers(ingredientList):
    otherList = (
        "!",
        '"',
        "#",
        "$",
        "%",
        "&",
        "'",
        "(",
        ")",
        "*",
        "+",
        ",",
        ".",
        ":",
        ";",
        "<",
        "=",
        ">",
        "?",
        "@",
        "[",
        "\\",
        "]",
        "^",
        "_",
        "`",
        "{",
        "|",
        "}",
        "~",
        " basic",
        " recipe follows",
        " see recipe",
        " refer to recipe",
        " as needed",
        " to taste",
        " optional",
        " garnish",
        " for serving",
    )
    remainderList = []
    finalList = []

    for ingredient in ingredientList:
        joinedSentence = " ".join(ingredient)
        remainderList.append(joinedSentence.lower())

    for ingredient in remainderList:
        for other in otherList:
            if other in ingredient:
                ingredient = ingredient.replace(other, "")
        finalList.append(ingredient)
    return finalList


def addLists(list1, list2):
    return [
        float(list1[0]) + list2[0],
        list1[1] + list2[1],
        list1[2] + list2[2],
        list1[3] + list2[3],
        list1[4] + list2[4],
        list1[5] + list2[5],
        list1[6] + list2[6],
    ]
