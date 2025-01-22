import requests

url = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/consommation-quotidienne-brute/records?limit=100&refine=date_heure%3A%222024%2F01%2F01%22"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
else:
    print(f"Failed to retrieve data: {response.status_code}")


data_filter = []

if 'results' in data:
    for record in data['results']:
        date = record.get('date')
        heure = record.get('heure')
        consommation_brute_gaz_grtgaz = record.get('consommation_brute_gaz_grtgaz')
        consommation_brute_gaz_terega = record.get('consommation_brute_gaz_terega')
        consommation_brute_gaz_totale = record.get('consommation_brute_gaz_totale')
        consommation_brute_electricite_rte = record.get('consommation_brute_electricite_rte')
        consommation_brute_totale = record.get('consommation_brute_totale')
        data_filter.append({
            'date': date,
            'heure': heure,
            'consommation_brute_gaz_grtgaz': consommation_brute_gaz_grtgaz,
            'consommation_brute_gaz_terega': consommation_brute_gaz_terega,
            'consommation_brute_gaz_totale': consommation_brute_gaz_totale,
            'consommation_brute_electricite_rte': consommation_brute_electricite_rte,
            'consommation_brute_totale': consommation_brute_totale
        })
else:
    print("No results found in the data.")

data_filtrer = [record for record in data_filter if all(value is not None for value in record.values())]

print(data_filtrer)
