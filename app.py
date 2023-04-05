from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_philosophy_links(query):
    search_url = 'https://en.wikipedia.org/w/index.php?search={}&title=Special:Search&profile=advanced&fulltext=1&advancedSearch-current=%7B%7D&ns0=1'.format(query)
    response = requests.get(search_url)
    
    if response.status_code != 200:
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = soup.find_all('div', class_='mw-search-result-heading')
    
    philosophy_links = []
    
    for result in search_results:
        link = result.find('a')
        if 'philosophy' in link['title'].lower():
            philosophy_links.append({
                'title': link['title'],
                'url': "https://en.wikipedia.org{}".format(link['href'])
            })
    
    return philosophy_links

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        philosophy_links = get_philosophy_links(query)
        
        if not philosophy_links:
            message = 'No se encontraron resultados filosóficos.'
        else:
            message = 'Resultados filosóficos:'
        
        return render_template('index.html', message=message, links=philosophy_links)
    
    return render_template('index.html', message='', links=[])

if __name__ == '__main__':
    app.run(debug=True)
