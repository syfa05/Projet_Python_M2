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
from sklearn.metrics import mean_squared_error
from scipy.interpolate import UnivariateSpline

class ExcelDataHandler:
    def __init__(self, date_debut_str, date_fin_str):
       self.date_debut_str = date_debut_str
       self.date_fin_str = date_fin_str  
   
            

    def generate_url(self):
        """
        Génère l'URL d'accès au fichier CSV à partir des dates sélectionnées.
        Assurez-vous que `self.date_debut_str` et `self.date_fin_str` sont au format 'yyyy-MM-dd'.
        """
        base_url = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/consommation-quotidienne-brute/exports/csv"
        url = (
            f"{base_url}"
            "?lang=fr"
            f"&qv1=(date_heure%3A%5B{self.date_debut_str}T00%3A00%3A00Z%20TO%20{self.date_fin_str}T23%3A59%3A59Z%5D)"
            "&timezone=Europe%2FParis"
            "&use_labels=true"
            "&delimiter=%3B"
        )
        return url

    def save_url_to_excel(self, output_file='output.xlsx'):
        """
        Télécharge le fichier CSV depuis l'URL générée, le convertit en Excel (.xlsx) et l'enregistre sous `output_file`.
        """
        try:
            url = self.generate_url()
            response = requests.get(url)
            response.raise_for_status()

            # Sauvegarde temporaire du fichier CSV
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_csv:
                tmp_csv.write(response.content)
                tmp_csv_path = tmp_csv.name

            # Conversion CSV → Excel
            data = pd.read_csv(tmp_csv_path, sep=';', engine='python')
            data.to_excel(output_file, index=False, engine='openpyxl')

            print(f"✅ Les données ont été enregistrées dans '{output_file}'")

        except Exception as e:
            print(f"❌ Une erreur s'est produite lors du téléchargement ou de la conversion : {e}")
        return data

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

    
    def plot_cubic_spline_interpolation(self, column_name):
        """
        Effectue une interpolation cubique pour la colonne spécifiée et affiche le résultat avec Plotly.
        """
        if column_name not in self.columns_of_interest:
            print(f"Colonne '{column_name}' non valide. Choisissez parmi : {self.columns_of_interest}")
            return None

        # Déterminer les dates de début et de fin pour le titre
        if 'Date' in self.data.columns:
            start_time = self.data['Date'].iloc[-1]
            end_time = self.data['Date'].iloc[0]
        elif 'Date - Heure' in self.data.columns:
            start_time = self.data['Date - Heure'].iloc[-1]
            end_time = self.data['Date - Heure'].iloc[0]
        else:
            start_time = ""
            end_time = ""

        fig = make_subplots(rows=1, cols=1, subplot_titles=(f'Interpolation Cubique - {column_name}',))
        y = self.data[column_name].values
        y = np.nan_to_num(y, nan=np.nanmean(y), posinf=np.nanmean(y), neginf=np.nanmean(y))
        cubic_spline = CubicSpline(self.x, y)
        x_new = np.linspace(0, len(self.data) - 1, 500)
        y_new = cubic_spline(x_new)
        if 'Date - Heure' in self.data.columns:
            x_dates = self.data['Date - Heure'].iloc[x_new.astype(int)].apply(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S%z"))
        elif 'Date' in self.data.columns:
            x_dates = self.data['Date'].iloc[x_new.astype(int)]
        else:
            x_dates = x_new
        fig.add_trace(go.Scatter(x=x_dates, y=y_new, mode='lines', name=column_name))

        fig.update_layout(
            template="plotly_white",
            height=600,
            width=800,
            title_text=f"Consommation de Gaz et d'Électricité du {start_time} au {end_time} - {column_name}"
        )
        fig.update_yaxes(title_text="Consommation (MW)")
        fig.update_layout(
            autosize=False,
            width=781,
            height=311,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
            fig.write_html(f.name)
            return f.name  # Chemin absolu vers le fichier HTML

    def plot_polynomial_interpolation(self, column_name, degree=8):
        """
        Effectue une interpolation polynomiale pour la colonne spécifiée et affiche le résultat avec Plotly.
        """
        if column_name not in self.columns_of_interest:
            print(f"Colonne '{column_name}' non valide. Choisissez parmi : {self.columns_of_interest}")
            return None

        fig = make_subplots(rows=1, cols=1, subplot_titles=(f'Interpolation Polynomiale - {column_name}',))
        y = self.data[column_name].values
        y = np.nan_to_num(y, nan=np.nanmean(y), posinf=np.nanmean(y), neginf=np.nanmean(y))
        coeffs = np.polyfit(self.x, y, degree)
        poly = np.poly1d(coeffs)
        x_new = np.linspace(0, len(self.data) - 1, 500)
        y_new = poly(x_new)
        if 'Date - Heure' in self.data.columns:
            x_dates = self.data['Date - Heure'].iloc[x_new.astype(int)].apply(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S%z"))
        elif 'Date' in self.data.columns:
            x_dates = self.data['Date'].iloc[x_new.astype(int)]
        else:
            x_dates = x_new
        fig.add_trace(go.Scatter(x=x_dates, y=y_new, mode='lines', name=column_name))
        fig.update_layout(
            template="plotly_white",
            height=600,
            width=800,
            title_text=f"Interpolation Polynomiale - {column_name}"
        )
        fig.update_yaxes(title_text="Consommation (MW)")
        fig.update_layout(
            autosize=False,
            width=781,
            height=311,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
            fig.write_html(f.name)
            return f.name  # Chemin absolu vers le fichier HTML

    def plot_best_fit_interpolation(self, column_name):
        """
        Tente plusieurs méthodes d'interpolation/régression et choisit celle qui minimise l'erreur quadratique moyenne (RMSE)
        pour la colonne spécifiée. Affiche le meilleur ajustement pour la série.
        """
        if column_name not in self.columns_of_interest:
            print(f"Colonne '{column_name}' non valide. Choisissez parmi : {self.columns_of_interest}")
            return None

        fig = make_subplots(rows=1, cols=1, subplot_titles=(f'Meilleur Ajustement - {column_name}',))
        y = self.data[column_name].values
        y = np.nan_to_num(y, nan=np.nanmean(y), posinf=np.nanmean(y), neginf=np.nanmean(y))

        # Préparer les méthodes à tester
        methods = {}

        # 1. Polynomiale (degré 4 à 7)
        for deg in range(4, 7):
            coeffs = np.polyfit(self.x, y, deg)
            poly = np.poly1d(coeffs)
            y_pred = poly(self.x)
            rmse = np.sqrt(mean_squared_error(y, y_pred))
            methods[f'Poly{deg}'] = (poly, rmse)

        # 2. Spline cubique
        try:
            cubic_spline = CubicSpline(self.x, y)
            y_pred = cubic_spline(self.x)
            rmse = np.sqrt(mean_squared_error(y, y_pred))
            methods['CubicSpline'] = (cubic_spline, rmse)
        except Exception:
            pass

        # 3. Spline lissée (UnivariateSpline)
        try:
            spline = UnivariateSpline(self.x, y, s=len(self.x))  # s: paramètre de lissage
            y_pred = spline(self.x)
            rmse = np.sqrt(mean_squared_error(y, y_pred))
            methods['SmoothSpline'] = (spline, rmse)
        except Exception:
            pass

        # Choisir la méthode avec le plus petit RMSE
        best_method = min(methods.items(), key=lambda item: item[1][1])

        # Générer les points pour affichage
        x_new = np.linspace(0, len(self.data) - 1, 500)
        if best_method[0].startswith('Poly'):
            y_new = best_method[1][0](x_new)
        else:
            y_new = best_method[1][0](x_new)

        # Gérer les dates pour l'axe x
        if 'Date - Heure' in self.data.columns:
            x_dates = self.data['Date - Heure'].iloc[x_new.astype(int)].apply(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S%z"))
        elif 'Date' in self.data.columns:
            x_dates = self.data['Date'].iloc[x_new.astype(int)]
        else:
            x_dates = x_new

        fig.add_trace(go.Scatter(x=x_dates, y=y_new, mode='lines', name=f"{column_name} ({best_method[0]})"))

        # Déterminer les dates de début et de fin pour le titre
        if 'Date' in self.data.columns:
            start_time = self.data['Date'].iloc[-1]
            end_time = self.data['Date'].iloc[0]
        elif 'Date - Heure' in self.data.columns:
            start_time = self.data['Date - Heure'].iloc[-1]
            end_time = self.data['Date - Heure'].iloc[0]
        else:
            start_time = ""
            end_time = ""

        fig.update_layout(
            template="plotly_white",
            height=600,
            width=800,
            title_text=f"Meilleur Ajustement du {start_time} au {end_time} - {column_name}"
        )
        fig.update_yaxes(title_text="Consommation (MW)")
        fig.update_layout(
            autosize=False,
            width=781,
            height=311,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
            fig.write_html(f.name)
            return f.name  # Chemin absolu vers le fichier HTML
