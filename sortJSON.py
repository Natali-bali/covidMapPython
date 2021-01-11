import json
file=open('custom.geo.json', 'r', encoding='utf-8-sig')
data = file.read()
file.close()
data = json.loads(data)
codes = ['AT', 'BE', 'BG', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT',
  'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE']
countries = {}
for item in data['features']:
    if item['properties']['wb_a2'] in codes:
        countries[item['properties']['wb_a2']] = item['geometry']
print(countries)
