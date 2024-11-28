from bs4 import BeautifulSoup
import requests

print('Parsing Weather')

url = 'https://meteopost.com/city/5688/'

response = requests.get(url)

if response.status_code == 200:
    item_site = BeautifulSoup(response.text, features='html.parser')

    temperature_elements = item_site.find_all('span', {'class': 't'})

    for temp_element in temperature_elements:
        try:
            temperature = temp_element.text.strip().replace('°', '').replace('C', '').replace(',', '.')
            print(f'Temperature: {temperature}°C')
        except Exception as e:
            print(f'Error extracting temperature: {e}')
