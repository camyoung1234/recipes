import os

def combine():
    markdown_dir = 'markdown'
    if not os.path.exists(markdown_dir):
        print(f"{markdown_dir} directory not found")
        return

    files = sorted([f for f in os.listdir(markdown_dir) if f.endswith('.md')])
    all_markdown = []

    for filename in files:
        with open(os.path.join(markdown_dir, filename), 'r') as f:
            all_markdown.append(f.read())

    os.makedirs('dist', exist_ok=True)
    with open('dist/recipes.md', 'w') as f:
        f.write('\n\n---\n\n'.join(all_markdown))
    print("Generated dist/recipes.md")

if __name__ == '__main__':
    combine()
