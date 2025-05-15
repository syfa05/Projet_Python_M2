import pandas as pd
import tkinter as tk
import requests
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import scipy.interpolate as spi
from plotly.subplots import make_subplots
# Removed unused import
from datetime import datetime
from scipy.interpolate import CubicSpline
from tkinter import filedialog
import time

class ExcelDataHandler:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def generate_url(self):
        base_url = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/consommation-quotidienne-brute/exports/xlsx?lang=fr"
        formatted_start_date = datetime.strptime(self.start_date, "%Y-%m-%d").strftime("%Y-%m-%dT%H:%M:%SZ")
        formatted_end_date = datetime.strptime(self.end_date, "%Y-%m-%d").strftime("%Y-%m-%dT%H:%M:%SZ")
        query = f"(date_heure%3A%5B{formatted_start_date}%20TO%20{formatted_end_date}%5D)"
        return f"{base_url}&qv1={query}&timezone=Europe%2FParis&use_labels=true&delimiter=%3B"

    def save_url_to_excel(self, output_file):
        try:
            # Lire les données à partir de l'URL
            response = requests.get(self.generate_url())
            with open(output_file, 'wb') as f:
                f.write(response.content)
            data = pd.read_excel(output_file)

            # Enregistrer les données dans un fichier Excel
            data.to_excel(output_file, index=False)
            
            print(f"Les données ont été enregistrées dans '{output_file}'")
        except PermissionError:
            print(f"Erreur : Impossible d'écrire dans le fichier '{output_file}'. Assurez-vous qu'il n'est pas ouvert ou utilisé par un autre programme.")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
        



class FileHandler:
    @staticmethod
    def select_file():
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre principale
        file_path = filedialog.askopenfilename(title="Sélectionner un fichier Excel", filetypes=[("Excel files", "*.xlsx")])
        return file_path

    @staticmethod
    def import_and_save_excel_file(output_file='output.xlsx'):
        # Demander à l'utilisateur de sélectionner un fichier
        file_path = FileHandler.select_file()

        if not file_path:
            print("Aucun fichier sélectionné")
            return None
        
        # Lire les données à partir du fichier Excel
        data = pd.read_excel(file_path)
        print(f"Les données ont été importées à partir de '{file_path}'")
        
        # Enregistrer les données dans un fichier Excel dans le projet
        data.to_excel(output_file, index=False)
        print(f"Les données ont été enregistrées dans '{output_file}'")
        
        return data
"""
# Importer les données à partir d'un fichier Excel
imported_data = FileHandler.import_and_save_excel_file()
if imported_data is not None:
    print("Données importées avec succès")
else:
    print("Aucune donnée importée")
    # Définir les dates de début et de fin
    start_date = "2023-01-01"
    end_date = "2023-03-01"

    # Créer une instance de ExcelDataHandler
    excel_handler = ExcelDataHandler(start_date, end_date)

    # Nom du fichier de sortie
    output_file = 'output.xlsx'

    # Appeler la fonction pour sauvegarder les données de l'URL dans un fichier Excel
    excel_handler.save_url_to_excel(output_file)

"""
class DataAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_excel(file_path)
        self.columns_of_interest = [
            'Consommation brute gaz (MW PCS 0°C) - GRTgaz',
            'Consommation brute gaz (MW PCS 0°C) - Teréga',
            'Consommation brute gaz totale (MW PCS 0°C)',
            'Consommation brute électricité (MW) - RTE',
            'Consommation brute totale (MW)'
        ]
        self.x = np.arange(len(self.data))

    def plot_histograms(self,Valeur_seuille):
        max_values = self.data[self.columns_of_interest].max()
        min_values = self.data[self.columns_of_interest].min()
        mean_values = self.data[self.columns_of_interest].mean()

        end_time = self.data['Date'].iloc[0]
        start_time = self.data['Date'].iloc[-1]

        columns_of_interest_abr = [
            'GRTgaz',
            'Teréga',
            'Total Gaz',
            'RTE',
            'Total'
        ]

        fig = make_subplots(rows=1, cols=1, subplot_titles=('Valeurs Maximales', 'Valeurs Minimales', 'Valeurs Moyennes'))

        #fig.add_trace(go.Bar(x=columns_of_interest_abr, y=max_values, marker_color='blue', name='Valeurs Maximales'), row=1, col=1)
        #fig.add_trace(go.Bar(x=columns_of_interest_abr, y=min_values, marker_color='red', name='Valeurs Minimales'), row=2, col=1)
        fig.add_trace(go.Bar(x=columns_of_interest_abr, y=mean_values, marker_color='green', name='Valeurs Moyennes'), row=1, col=1)

        fig.update_layout(template="plotly_white", height=800, width=800, title_text=f"Consommation de Gaz et d'Électricité du {start_time} au {end_time}")
        fig.update_yaxes(title_text="Consommation (MW)", range=[0, 40000])

        fig.show()

    def plot_linear_interpolation(self):
        fig = make_subplots(rows=1, cols=1, subplot_titles=('Interpolation Linéaire'))
        for col in self.columns_of_interest:
            y = self.data[col].values
            y = np.nan_to_num(y, nan=np.nanmean(y), posinf=np.nanmean(y), neginf=np.nanmean(y))
            linear_interp = np.interp(self.x, self.x, y)
            fig.add_trace(go.Scatter(x=self.data['Date - Heure'].apply(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S%z")), y=linear_interp, mode='lines', name=col))
        fig.update_layout(template="plotly_white", height=600, width=800, title_text="Interpolation Linéaire")
    
    def plot_polynomial_interpolation(self):
        fig = make_subplots(rows=1, cols=1, subplot_titles=('Interpolation Polynomiale (Degré 5)'))
        for col in self.columns_of_interest:
            y = self.data[col].values
            y = np.nan_to_num(y, nan=np.nanmean(y), posinf=np.nanmean(y), neginf=np.nanmean(y))
            
            # Interpolation polynomiale de degré 5
            degree = 12
            coefficients = np.polyfit(self.x, y, degree)
            polynomial = np.poly1d(coefficients)
            y_new = polynomial(self.x)
            fig.add_trace(go.Scatter(
                x=self.data['Date - Heure'].apply(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S%z")),
                y=y_new,
                mode='lines',
                name=f"{col} (Degré {degree})"
            ))
        
        fig.update_layout(template="plotly_white", height=600, width=800, title_text="Interpolation Polynomiale (Degré 5)")
        fig.show()

    def plot_cubic_spline_interpolation(self):
        fig = make_subplots(rows=1, cols=1, subplot_titles=('Interpolation Cubique'))
        for col in self.columns_of_interest:
            y = self.data[col].values
            y = np.nan_to_num(y, nan=np.nanmean(y), posinf=np.nanmean(y), neginf=np.nanmean(y))
            cubic_spline = CubicSpline(self.x, y)
            x_new = np.linspace(0, len(self.data) - 1, 500)
            y_new = cubic_spline(x_new)
            fig.add_trace(go.Scatter(x=self.data['Date - Heure'].iloc[x_new.astype(int)].apply(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S%z")), y=y_new, mode='lines', name=col))
        fig.update_layout(template="plotly_white", height=600, width=800, title_text="Interpolation Cubique")
        fig.show()

    def plot_spline_interpolation(self):
        fig = make_subplots(rows=1, cols=1, subplot_titles=('Interpolation Spline'))
        for col in self.columns_of_interest:
            y = self.data[col].values
            y = np.nan_to_num(y, nan=np.nanmean(y), posinf=np.nanmean(y), neginf=np.nanmean(y))
            spline_interp = spi.UnivariateSpline(self.x, y)
            x_new = np.linspace(0, len(self.data) - 1, 500)
            y_new = spline_interp(x_new)
            fig.add_trace(go.Scatter(x=self.data['Date - Heure'].iloc[x_new.astype(int)].apply(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S%z")), y=y_new, mode='lines', name=col))
        fig.update_layout(template="plotly_white", height=600, width=800, title_text="Interpolation Spline")
        fig.show()


class CodeTimer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    def elapsed_time(self):
        if self.start_time is not None and self.end_time is not None:
            return self.end_time - self.start_time
        else:
            return None

start_date = "2023-01-01"
end_date = "2023-03-01"
# Convertir une variable de type date en une chaîne de caractères
date_variable = datetime.strptime(start_date, "%Y-%m-%d")
date_string = date_variable.strftime("%d/%m/%Y")
print("Date de début :", start_date)
print("Date de fin :", end_date)
"""

# Utilisation de CodeTimer pour mesurer le temps d'exécution
timer = CodeTimer()
timer.start()

# Placez ici le code dont vous voulez mesurer le temps d'exécution
# Exemple : data_analyzer.plot_polynomial_interpolation()
# Créer une instance de DataAnalyzer et appeler les fonctions pour tracer les graphiques
data_analyzer = DataAnalyzer('output.xlsx')
#data_analyzer.plot_histograms()
#data_analyzer.plot_linear_interpolation()
data_analyzer.plot_cubic_spline_interpolation()
#data_analyzer.plot_spline_interpolation()
data_analyzer.plot_polynomial_interpolation()


timer.stop()
print(f"Temps d'exécution : {timer.elapsed_time():.2f} secondes")


# Créer une instance de DataAnalyzer et appeler les fonctions pour tracer les graphiques
data_analyzer = DataAnalyzer('output.xlsx')
#data_analyzer.plot_histograms()
#data_analyzer.plot_linear_interpolation()
#data_analyzer.plot_cubic_spline_interpolation()
#data_analyzer.plot_spline_interpolation()
data_analyzer.plot_polynomial_interpolation()


"""