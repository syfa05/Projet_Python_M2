import requests
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import os
import scipy
from datetime import datetime

from scipy.interpolate import CubicSpline


class DataFetcher:
    def __init__(self, url):
        self.url = url

    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            return None

    def filter_data(self, data):
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
        return [record for record in data_filter if all(value is not None for value in record.values())]

    def get_filtered_data(self):
        data = self.fetch_data()
        if data:
            return self.filter_data(data)
        return []
    
    def max_min_consommation_brute_totale(self):
         
         Keys= ['consommation_brute_gaz_grtgaz',
               'consommation_brute_gaz_terega',
               'consommation_brute_gaz_totale',
               'consommation_brute_electricite_rte',
               'consommation_brute_totale']
         Consomation_Max = []*len(Keys)
         Consomation_Min = []*len(Keys)
         for key in Keys:
                data_filtrer = self.get_filtered_data()
                Valeur_Max = max(data_filtrer, key=lambda x: x[key])
                Consomation_Max.append(Valeur_Max[key])
                Valeur_Min = min(data_filtrer, key=lambda x: x[key])
                Consomation_Min.append(Valeur_Min[key])

         return Consomation_Max, Consomation_Min
                         
    def moyenne_consommation(self):

        Keys= ['consommation_brute_gaz_grtgaz',
               'consommation_brute_gaz_terega',
               'consommation_brute_gaz_totale',
               'consommation_brute_electricite_rte',
               'consommation_brute_totale']
        
        consomation_moyenne = []*len(Keys)

        for key in Keys:
            data_filtrer = self.get_filtered_data()
            consomation_moyenne.append(sum([record[key] for record in data_filtrer]) / len(data_filtrer))
        return consomation_moyenne
        



def interpolate_and_plot(data, key, title, degree):
    if degree >= 6:
        raise ValueError("Degree must be less than 6")

    def calculate_time_vector(data):
        time_vector = []
        for record in data:
            date_str = record['date']
            time_str = record['heure']
            datetime_str = f"{date_str} {time_str}"
            datetime_obj = datetime.strptime(datetime_str, "%d/%m/%Y %H:%M")
            seconds = (datetime_obj - datetime(1970, 1, 1)).total_seconds()
            time_vector.append(seconds)
        return time_vector

    time_vector = calculate_time_vector(data)
    values = [record[key] for record in data]

    # Ensure the time vector is sorted
    sorted_indices = np.argsort(time_vector)
    sorted_time_vector = np.array(time_vector)[sorted_indices]
    sorted_values = np.array(values)[sorted_indices]

    # Polynomial interpolation
    coefficients = np.polyfit(sorted_time_vector, sorted_values, degree)
    polynomial = np.poly1d(coefficients)
    interpolated_values_poly = polynomial(sorted_time_vector)

    # Cubic spline interpolation
    cs = CubicSpline(sorted_time_vector, sorted_values)
    interpolated_values_spline = cs(sorted_time_vector)

    plt.figure(figsize=(10, 5))
    plt.plot(sorted_time_vector, sorted_values, 'o', label='Original Data')
    plt.plot(sorted_time_vector, interpolated_values_poly, '-', label=f'Polynomial Degree {degree}')
    plt.plot(sorted_time_vector, interpolated_values_spline, '--', label='Cubic Spline')
    plt.title(title)
    plt.xlabel('Time (seconds since epoch)')
    plt.ylabel(key)
    plt.legend()
    plt.tight_layout()
    plt.show()


                
url = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/consommation-quotidienne-brute/records?limit=100&refine=date_heure%3A%222024%2F01%2F01%22"
fetcher = DataFetcher(url)
data_filtrer = fetcher.get_filtered_data()
Conso_Max, Conso_Min = fetcher.max_min_consommation_brute_totale()
Conso_Moy = fetcher.moyenne_consommation()
print(Conso_Max, Conso_Min, Conso_Moy)

keys = [
    'consommation_brute_gaz_grtgaz',
    'consommation_brute_gaz_terega',
    'consommation_brute_gaz_totale',
    'consommation_brute_electricite_rte',
    'consommation_brute_totale'
]

titles = [
    'Consommation Brute Gaz GRTgaz',
    'Consommation Brute Gaz Terega',
    'Consommation Brute Gaz Totale',
    'Consommation Brute Electricite RTE',
    'Consommation Brute Totale'
]
    # Example usage
degree = 3 # User-defined degree of the polynomial
for key, title in zip(keys, titles):
    interpolate_and_plot(data_filtrer, key, title, degree)