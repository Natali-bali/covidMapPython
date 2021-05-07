import folium
import requests
import json
import matplotlib.pyplot as plt
from datetime import date
date = date.today()
codes = ['AL', 'AT', 'BA', 'BE', 'BG', 'GB', 'CY', 'CH',
'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'HR', 'IE', 'IT',
  'IS', 'LI','LV', 'LT', 'LU', 'ME', 'MK', 'MT', 'NL', 'NO',
  'PL', 'PT', 'RO', 'RS', 'SK', 'SI', 'ES', 'SE']
responses = []
try:
    for code in codes:
        resp = requests.get(' https://corona-api.com/countries/'+code)
        resp.raise_for_status()
        jsonResponse = resp.json()
        coordinates = jsonResponse['data']['coordinates']
        name = jsonResponse['data']['name']
        dataToday = jsonResponse['data']['today']
        data = jsonResponse['data']['latest_data']
        cases = jsonResponse['data']['latest_data']['calculated']['cases_per_million_population']
        country = jsonResponse['data']['code']
        responses.append([name, coordinates, dataToday, data, cases, country])
except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')

map = folium.Map(location = [53.58, 9.999], zoom_start = 3, tiles = "Stamen Terrain")
fg=folium.FeatureGroup(name="Covid Data")
html = """
            <h3>Country: {}</h3>
            <h4>Date: {}</h4>
            <h5>Deaths today: {}</h5>
            <h5>Cases today: {}</h5>
            </br>
            <h5>Total cases:{}</h5>
            <h5>Total deaths:{}</h5>
            """
for item in responses:
    fg.add_child(folium.Marker([item[1]['latitude'],item[1]['longitude']],
    popup=html.format(item[0], date, str(item[2]['deaths']),
    str(item[2]['confirmed']), str(item[3]['confirmed']),
    str(item[3]['deaths'])),
    icon=folium.Icon(color="green")))

# check the numbers where i change color on map
cases_per_mil = []
for item in responses:
    cases_per_mil.append(item[4])
# print(cases_per_mil)
cases_per_mil.sort()
# plt.plot(cases_per_mil)
# plt.show()
# --style function
def style_fcn(x):
    color = 'grey'
    countryCode = x['properties']['wb_a2']
    if countryCode in codes:
        for item in responses:
            if item[5] == countryCode:
                if 0>item[4]<340:
                    color = 'green'
                elif 340>=item[4]<1000:
                     color = 'yellow'
                elif 1000>=item[4]<2600:
                     color = 'orange'
                elif 2600>=item[4]<4000:
                     color = 'violet'
                else:
                     color = 'red'
    return {"fillOpacity": 0.5,
            "fillColor": color}
# --creating geojson file only for our countries
file=open('custom.geo.json', 'r', encoding='utf-8-sig')
d = file.read()
file.close()
d = json.loads(d)

fg.add_child(folium.GeoJson(d,
style_function = style_fcn))

map.add_child(fg)

map.save("map.html")


# other way to add Marker
# folium.Marker(
#     [53.5843692323313, 9.996319675785987], popup="<b>French Cafe</b>", icon=folium.Icon(color="green")
# ).add_to(map)