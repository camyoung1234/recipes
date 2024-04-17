import colorsys
import html
import json
import shutil

def load_recipes():
    try:
        with open('recipes.json', 'r') as f:
            recipes = json.load(f)
    except:
        recipes = {}
    return recipes

def create_body(recipes):
    return ''.join([create_recipe_html(recipe) for recipe in recipes.values()])

def create_ingredient_html(ingredient):
    return f'<li>{encode(ingredient)}</li>'

def create_ingredients_html(ingredients):
    return f'<ul class="ingredients-list">{"".join([create_ingredient_html(ingredient) for ingredient in ingredients])}</ul>'

def create_ingredient_groups_html(ingredient_groups, color):
    result = ''
    for ingredient_group in ingredient_groups:
        result += ''.join([f'<div class="ingredients-title" style="color:{color}">{ingredient_group_title}</div>{create_ingredients_html(ingredient_group[ingredient_group_title])}' if ingredient_group[ingredient_group_title] is not None else '' for ingredient_group_title in ingredient_group])
    return result

def create_instruction_html(instruction):
    return f'<li>{encode(instruction)}</li>'

def create_instructions_html(instructions):
    return f'<ol class="instructions-list">{"".join([create_instruction_html(instruction) for instruction in instructions])}</ol>'

def create_recipe_html(recipe):
    if 'dominant_color' in recipe:
        dominant_color = recipe['dominant_color']
        color = color_hex(dominant_color)
        hls = colorsys.rgb_to_hls(dominant_color[0] / 255, dominant_color[1] / 255, dominant_color[2] / 255)
        bg_color = colorsys.hls_to_rgb(hls[0], 0.95, hls[2])
        bg_color = [int(bg_color[0] * 255), int(bg_color[1] * 255), int(bg_color[2] * 255)]
        bg_color = color_hex(bg_color)
        color = colorsys.hls_to_rgb(hls[0], 0.3, hls[2])
        color = [int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)]
        color = color_hex(color)
    else:
        color = '#000000'
        bg_color = '#eeeeee'
    return f'''\
<div class="recipe">
  <div class="title" style="color:{color}">{recipe["title"]}</div>
  <div class="ingredients" style="background-color:{bg_color}">
    {create_ingredient_groups_html(recipe["ingredient_groups"], color)}
  </div>
  <div class="instructions">
    <div class="instructions-title" style="color:{color}">Instructions</div>
    {create_instructions_html(recipe["instructions_list"])}
  </div>
</div>
'''

def load_css():
    with open('style.css', 'r') as css:
        return css.read()

def encode(x):
    return x.encode('ascii', 'xmlcharrefreplace').decode('ascii')

def color_hex(color):
    return '#' + hex(color[0])[2:] + hex(color[1])[2:] + hex(color[2])[2:]

def build():
    os.makedirs('dist', exist_ok=True)
    shutil.copy('_headers', 'dist/_headers')
    index_html = f'''\
<!DOCTYPE html>
<html>
  <head>
    <title>Recipes</title>
    <style type="text/css">
      {load_css()}
    </style>
  </head>
  <body>
    {create_body(load_recipes())}
  </body>
</html>
'''
    with open('dist/index.html', 'w') as f:
        f.write(index_html)
    return

    with open('dist/index.html', 'w') as index_html:
        index_html.write('</style></head><body>')
        try:
            with open('recipes.json', 'r') as recipes_json:
                recipes = json.load(recipes_json)
        except:
            recipes = {}
        for recipe in recipes.values():

            index_html.write('<div class="recipe">')
            #if 'image' in recipe:
            #    print(recipe['image'])
            #    index_html.write(f'<img src={recipe["image"]}></img>')
            if 'title' in recipe:
                index_html.write(f'<h1 class="title" style="background-color:{bg_color}"')
                #index_html.write(f' style="color:{color};"')
                index_html.write(f'>{encode(recipe["title"])}</h1>')
            index_html.write(f'<div class="ingredients" style="background-color:{bg_color};"')
            #if 'palette' in recipe:
            #    lightest_color = colorsys.hls_to_rgb(*max([colorsys.rgb_to_hls(*color) for color in recipe['palette']], key=lambda hls: hls[1]))
            #    index_html.write(f' style="background-color:#{int(lightest_color[0]):02x}{int(lightest_color[1]):02x}{int(lightest_color[2]):02x};"')
            index_html.write('><h2 class="title">Ingredients</h2>')
            index_html.write('<table>')
            for ingredient in recipe['ingredients']:
                index_html.write(f'<tr><td class="ingredient">{encode(ingredient)}</td></tr>')
            index_html.write('</table>')
            index_html.write('</div>')
            index_html.write(f'<div class="instructions"><h2 class="title" style="color:{color};">Instructions</h2>')
            index_html.write('<ol class="instructions-list">')
            for instruction in recipe['instructions_list']:
                index_html.write(f'<li>{encode(instruction)}</li>')
            index_html.write('</ol>')
            index_html.write('</div>')
            index_html.write('</div>')
        index_html.write('</body></index_html>')

if __name__ == '__main__':
    build()
