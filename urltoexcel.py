import pandas as pd
import tkinter as tk
import requests
import plotly.graph_objects as go
import numpy as np
import tempfile
import scipy.interpolate as spi
from plotly.subplots import make_subplots
from datetime import datetime
from scipy.interpolate import CubicSpline
from tkinter import filedialog
import time

class ExcelDataHandler:
    def __init__(self, start_date, end_date):
        # Accepte start_date et end_date comme datetime, string, QDateEdit, ou QDate, puis les convertit en 'yyyy-mm-dd'
        self.date_debut_str = self._convert_to_str(start_date)
        self.date_fin_str = self._convert_to_str(end_date)
        
    def _convert_to_str(self, date_obj):
        # Si QDateEdit (PyQt5/6), extraire QDate puis convertir
        if hasattr(date_obj, "date"):
            date_obj = date_obj.date()
        # Si QDate, convertir en Python datetime
        if hasattr(date_obj, "toPyDate"):
            date_obj = date_obj.toPyDate()
        # Si string, convertir en datetime
        if isinstance(date_obj, str):
            return pd.to_datetime(date_obj).strftime("%Y-%m-%d")
        # Si datetime/date, formatter
        return date_obj.strftime("%Y-%m-%d")
        
    def generate_url(self):
        url = (
            "https://odre.opendatasoft.com/explore/dataset/consommation-quotidienne-brute/download/"
            "?format=csv&timezone=Europe/Paris"
            f"&q=date_heure:[{self.date_debut_str}T00:00:00Z TO {self.date_fin_str}T23:59:59Z]"
            "&sort=-date_heure"
        )
        return url

    def save_url_to_excel(self, output_file):
        try:
            response = requests.get(self.generate_url())
            # Save as CSV first
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_csv:
                tmp_csv.write(response.content)
                tmp_csv_path = tmp_csv.name
            # Read CSV and save as Excel
            data = pd.read_csv(tmp_csv_path, sep=';')
            data.to_excel(output_file, index=False, engine='openpyxl')
            print(f"Les données ont été enregistrées dans '{output_file}'")
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
        data = pd.read_excel(file_path, engine='openpyxl')
        print(f"Les données ont été importées à partir de '{file_path}'")
        # Enregistrer les données dans un fichier Excel dans le projet
        data.to_excel(output_file, index=False, engine='openpyxl')
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
        self.data = pd.read_excel(file_path, engine='openpyxl')
        self.columns_of_interest = [
            'Consommation brute gaz (MW PCS 0°C) - GRTgaz',
            'Consommation brute gaz (MW PCS 0°C) - Teréga',
            'Consommation brute gaz totale (MW PCS 0°C)',
            'Consommation brute électricité (MW) - RTE',
            'Consommation brute totale (MW)'
        ]
        self.x = np.arange(len(self.data))

    def count_days_by_seuil(self, seuil, column_name):
        """
        Compte le nombre de jours où la consommation de la colonne choisie est supérieure et inférieure au seuil donné.
        column_name doit être un des éléments de self.columns_of_interest.
        Retourne un tuple (nb_jours_sup, nb_jours_inf).
        """
        if column_name not in self.columns_of_interest:
            print(f"Colonne '{column_name}' non valide. Choisissez parmi : {self.columns_of_interest}")
            return None
        if 'Date' not in self.data.columns:
            print("Colonne 'Date' manquante dans les données.")
            return None
        # Convertir la colonne 'Date' en datetime si ce n'est pas déjà fait
        self.data['Date'] = pd.to_datetime(self.data['Date'], format='%d/%m/%Y', errors='coerce')
        # Grouper par jour et sommer la consommation pour chaque jour
        daily_consumption = self.data.groupby(self.data['Date'])[column_name].sum()
        nb_jours_sup = (daily_consumption > seuil).sum()
        nb_jours_inf = (daily_consumption < seuil).sum()
        return nb_jours_sup, nb_jours_inf
       
    def get_column_statistics(self, column_name):
        """
        Retourne le max, min et mean pour une colonne d'intérêt donnée.
        """
        if column_name not in self.columns_of_interest:
            print(f"Colonne '{column_name}' non valide. Choisissez parmi : {self.columns_of_interest}")
            return None
        col_data = self.data[column_name]
        stats = {
            'maxi': col_data.max(),
            'mini': col_data.min(),
            'moyenne': col_data.mean(),
            'mean_Total': self.data[self.columns_of_interest].mean()
        }
        return stats

    def plot_histograms(self, stats, value_type='mean_Total'):
        """
        Génère un fichier HTML contenant un histogramme Plotly, et retourne le chemin.
        """
        columns_of_interest_abr = ['GRTgaz', 'Teréga', 'Total Gaz', 'RTE', 'Total']
        values = stats.get(value_type)
        if values is None:
            print("Type de valeur non reconnu. Utilisez 'maxi', 'mini', 'moyenne' ou 'mean_Total'.")
            return None
        end_time = self.data['Date'].iloc[0]
        start_time = self.data['Date'].iloc[-1]
        fig = make_subplots(rows=1, cols=1, subplot_titles=(f"Valeurs {value_type.capitalize()}s",))
        color_map = {'maxi': 'blue', 'mini': 'red', 'moyenne': 'green', 'mean_Total': 'orange'}
        fig.add_trace(
            go.Bar(x=columns_of_interest_abr, y=values, marker_color=color_map.get(value_type, 'green')),
            row=1, col=1
        )
        fig.update_layout(
            template="plotly_white",
            height=600,
            width=800,
            title_text=f"Consommation de Gaz et d'Électricité du {start_time} au {end_time}"
        )
        # Ajuster la taille du graphique pour correspondre à la fenêtre OpenGLWidget
        fig.update_yaxes(title_text="Consommation (MW)")
        fig.update_layout(
            autosize=False,
            width=631,
            height=301,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
            fig.write_html(f.name)
            return f.name  # Chemin absolu vers le fichier HTML

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
"""
# Exemple d'utilisation
start_date = "2023-01-01"
end_date = "2023-03-01"
# Convertir une variable de type date en une chaîne de caractères
date_variable = datetime.strptime(start_date, "%Y-%m-%d")
date_string = date_variable.strftime("%d/%m/%Y")
print("Date de début :", start_date)
print("Date de fin :", end_date)

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