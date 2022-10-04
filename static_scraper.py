import requests
from bs4 import BeautifulSoup

page =requests.get('https://realpython.github.io/fake-jobs/')
soup = BeautifulSoup(page.content, 'html.parser')

resultsDiv = soup.find(id='ResultsContainer')
#resultCards = resultsDiv.find_all(class_='card-content')
pythonResultTitles = resultsDiv.find_all(
    'h2', 
    class_='title is-5', 
    string= lambda title: 'python' in title.lower()
)
pythonResultCards = []
for title in pythonResultTitles:
    pythonResultCards.append(title.parent.parent.parent)

print()
for card in pythonResultCards:
    title = card.find('h2', class_='title is-5')
    company = card.find('h3', class_='subtitle is-6 company')
    location = card.find('p', class_='location')
    links = card.find_all('a')
    print(title.text.strip())
    print(company.text.strip())
    print(location.text.strip())
    print(links[1]['href'])
    print()

input()