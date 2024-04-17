from colorthief import ColorThief
import json
import os
from recipe_scrapers import scrape_me
import requests
from tqdm import tqdm
import datetime

def scrape():
    try:
        with open('urls.txt', 'r') as f:
            urls = f.read().split()
    except:
        urls = []
    try:
        with open('recipes.json', 'r') as f:
            recipes = json.load(f)
    except:
        recipes = {}
    with open(f'recipes_{str(datetime.datetime.now()).replace("-", "_").replace(" ", "_").replace(":", "_").replace(".", "_")}.json', 'w') as f:
        json.dump(recipes, f)
    for url in tqdm(urls):
        if url in recipes:
            continue
        try:
            recipe = scrape_me(url, wild_mode=True).to_json()
        except:
            print(f'failed to scrape {url}')
            continue
        try:
            print(recipe['image'])
            image_ext = os.path.splitext(recipe['image'])[1]
            with open(f'tmp{image_ext}', 'wb') as f:
                f.write(requests.get(recipe['image']).content)
            color_thief = ColorThief(f'tmp{image_ext}')
            recipe['dominant_color'] = color_thief.get_color(quality=1)
            recipe['palette'] = color_thief.get_palette(color_count=6)
        except Exception as e:
            print(e)
        del recipe['instructions']
        recipes[url] = recipe
    with open('recipes.json', 'w') as f:
        json.dump(recipes, f)

if __name__ == '__main__':
    scrape()
