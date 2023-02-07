# Buczynski, Fortier - Final Project

import requests
import csv
import json
import config

def get_food_ids(searchterm, num_results):
    """
    Returns a list of FDC IDs of all results matching the search term
    """

    results = []

    url = "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=" + config.TOKEN + "&query=" + searchterm.replace(" ", "%20") + "&pageSize=" + str(num_results)
    headers = { 'Content-Type': 'application/json' }  
    parameters = {}
    response = requests.get(url, params=parameters, headers=headers)
    data = json.loads(response.text)

    for food in data['foods']:
        results.append(str(food['fdcId']))

    return results


def get_details_by_id(ids):
    """
    Get basic nutritional details and food information from a list of FDA IDs
    """

    results = {}

    url = "https://api.nal.usda.gov/fdc/v1/foods?fdcIds=" + '&fdcIds='.join(ids) + "&api_key=" + config.TOKEN
    headers = { 'Content-Type': 'application/json' }  
    parameters = {}
    response = requests.get(url, params=parameters, headers=headers)
    data = json.loads(response.text)

    for food in data:
        if "labelNutrients" in food.keys() and "fdcId" in food:
            id = food['fdcId']
            results[id] = {}
            results[id]["description"] = food['description']
            results[id]["nutrients"] = {}
            for n in food['labelNutrients']:
                nut = results[id]['nutrients']
                results[id]['nutrients'][n] = food['labelNutrients'][n]['value']
        

    return results


def write_to_csv(data, filepath):
    with open(filepath, 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["id", "description", "fat", "sodium", "carbohydrates", "fiber", "sugars",
        "addedSugar", "protein", "calories"])
                        
        for breads in data:
            ids = breads.keys()
            values = ["fat", "sodium", "carbohydrates", "fiber", "sugars", "addedSugar", "protein", "calories"]

            for id in ids:
                nutrients = breads[id]['nutrients'].keys()
                for v in values:
                    if v not in nutrients:
                        breads[id]['nutrients'][v] = None

                writer.writerow([id, breads[id]['description'], breads[id]['nutrients']['fat'],
                breads[id]['nutrients']['sodium'], breads[id]['nutrients']['carbohydrates'],
                breads[id]['nutrients']['fiber'], breads[id]['nutrients']['sugars'], breads[id]['nutrients']['addedSugar'],
                breads[id]['nutrients']['protein'], breads[id]['nutrients']['calories']])


if __name__ == '__main__':

    breads = []
    bread_list = ["Whole Wheat Bread", "Sourdough Bread", "White Bread",
    "Multigrain Bread", "Rye Bread", "Pumpernickel", "Ciabatta", "Baguette",
    "Brioche", "Challah", "Naan Bread"]

    for b in bread_list:
        ids = get_food_ids(b, 20)
        breads.append(get_details_by_id(ids))

    write_to_csv(breads, "breads.csv")
