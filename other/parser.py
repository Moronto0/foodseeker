import requests
import pandas as pd
import json
from bs4 import BeautifulSoup

#food;ingridients;category;kitchen;url

url_site = "https://eda.ru/recepty/osnovnye-blyuda"
site_req = requests.get(url_site)

foods = []
try:
    while True:
        soup_site = BeautifulSoup(site_req.text, "html.parser")

        for food in json.loads(soup_site.find('script', type='application/ld+json').text)["itemListElement"]:
            food_url = food["url"]
            site_food_req = requests.get(food_url)
            soup_food = BeautifulSoup(site_food_req.text, "html.parser")

            food_name = soup_food.find("h1", class_="emotion-gl52ge").text

            ingredients_lists = soup_food.find("div", class_="emotion-yj4j4j").find_all('span', {'itemprop': 'recipeIngredient'})

            ingredients = []
            for ingredient in ingredients_lists:
                ingredients.append(ingredient.text.lower())

            sections_lists = soup_food.find("ul", class_="emotion-1kcflwj").find_all("meta", {'itemprop': 'name'})

            try:
                category = sections_lists[1].get("content")
            except:
                category = ""
            try:
                kitchen = sections_lists[2].get("content")
            except:
                kitchen = ""

            foods.append([food_name, ', '.join(ingredients), category, kitchen, food_url])

        site_req = requests.get(soup_site.find('link', rel='next').get('href'))
        if not site_req:
            break
except Exception as exc:
    print(exc, sections_lists)
finally:
    pd = pd.DataFrame(foods, columns=["food", "ingredients", "category", "kitchen", "food_url"])
    pd.to_csv("Foods_osnovnye-blyuda.csv", index=False, sep=";")
