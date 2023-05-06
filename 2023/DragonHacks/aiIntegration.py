import openai


openai.api_key = "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"


def determineHealth(name, macros):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{prompt}\n{prompt(name, macros)}",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    output_str = response.choices[0].text.strip()
    return output_str


def prompt(name, macros):
    prompt = f"""
    Given the name of a food item and it's macronutrients per serving, determine if the food is 'healthy':
    Format of MacroCount:
    [calories, carbs, sugars, fibre, netCarbs, protein, fats]
    
    Give your answer as Bulking, Cutting, or Unhealthy ONLY,. If it is Unhealthy, suggest better alternatives to that food item, in the next line, only giving the name of the food item.
    
    Give your output in the format:
    
    [bulking / cutting / unhealthy]\n[alternative food item]
    
    DO NOT OUTPUT ANY SORT OF CODE OR EXPLANATION LIKE 'BETTER ALTERNATIVES: ', JUST GIVE YOUR REPLY IN THE FOLLOWING FASHION. DO NOT ADD A FULL STOP ANYWHERE.
    
    Name: {name}
    Macros: {macros}
    """
    return prompt


def getHealth(name, macros):
    aiAnswer = determineHealth(name, macros)
    aiAnswer = aiAnswer.split()
    foodStatus = aiAnswer[0]
    aiAnswer.pop(0)
    foodAlternative = " ".join(aiAnswer)

    return foodStatus, foodAlternative
