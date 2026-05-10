import json
import os
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def to_markdown(recipe):
    md = f"# {recipe['title']}\n\n"
    md += "## Ingredients\n"
    for group in recipe.get('ingredient_groups', []):
        purpose = group.get('purpose')
        if purpose:
            md += f"**{purpose}**\n"
        for ingredient in group.get('ingredients', []):
            md += f"* {ingredient}\n"

    md += "\n## Instructions\n"
    for i, instruction in enumerate(recipe.get('instructions_list', []), 1):
        md += f"{i}. {instruction}\n"
    return md

def main():
    if not os.path.exists('recipes.json'):
        print("recipes.json not found")
        return

    with open('recipes.json', 'r') as f:
        recipes = json.load(f)

    os.makedirs('markdown', exist_ok=True)

    for url, recipe in recipes.items():
        title = recipe.get('title', 'Untitled')
        filename = slugify(title) + '.md'
        filepath = os.path.join('markdown', filename)

        with open(filepath, 'w') as f:
            f.write(to_markdown(recipe))
        print(f"Generated {filepath}")

if __name__ == '__main__':
    main()
