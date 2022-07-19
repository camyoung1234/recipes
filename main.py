import os

def main():
    os.makedirs('dist', exist_ok=True)
    with open('dist/index.html', 'w') as index_html:
        index_html.write('<!DOCTYPE html><html><head><title>Recipes</title></head><body></body></html>')

if __name__ == '__main__':
    main()
