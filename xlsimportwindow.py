"""
import pandas as pd
import openpyxl as op

# Importation des donnees d'un fichier Excel
class ExcelDataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def process_sheet(self, sheet_name):
        try:
            data = pd.read_excel(self.file_path, sheet_name=sheet_name)
            mean_value = data.mean().mean()
            min_value = data.min().min()
            max_value = data.max().max()
            return mean_value, min_value, max_value
        except Exception as e:
            print(f"An error occurred: {e}")
            return None, None, None
        
    def get_data(self):
        try:
            excel_file = pd.ExcelFile(self.file_path)
            sheet_names = excel_file.sheet_names
            return {sheet_name: self.process_sheet(sheet_name) for sheet_name in sheet_names}
        except Exception as e:
            print(f"An error occurred: {e}")
            return {}
        
    def get_max_min_consommation_brute_totale(self):
        data = self.get_data()
        max_min_values = {}
        for sheet_name, values in data.items():
            max_min_values[sheet_name] = {'max': values[2], 'min': values[1]}
        return max_min_values
    
    def get_mean_consommation_brute_totale(self):
        data = self.get_data()
        mean_values = {}
        for sheet_name, values in data.items():
            mean_values[sheet_name] = values[0]
        return mean_values
    

# Test de la classe ExcelDataProcessor
processing = ExcelDataProcessor('consommation-quotidienne-brute.xlsx')
print(processing.get_data())
"""


import sys
import pandas as pd
import numpy as np
import requests
from io import BytesIO
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QLabel, QComboBox, QPushButton,
    QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QDateEdit
)
from PyQt5.QtCore import QDate
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.interpolate import interp1d


class DataAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analyseur de Données Excel")
        self.data = None

        # Widgets
        self.import_btn = QPushButton("Importer un fichier Excel")
        self.url_input = QLineEdit("http://...")
        self.start_date = QDateEdit(QDate.currentDate())
        self.end_date = QDateEdit(QDate.currentDate())
        self.download_btn = QPushButton("Télécharger les données")

        self.column_selector = QComboBox()
        self.run_btn = QPushButton("Run")
        self.stats_label = QLabel()

        self.threshold_input = QLineEdit()
        self.threshold_result = QLabel()

        self.interp_mode = QComboBox()
        self.interp_mode.addItems(["linéaire", "cubic"])
        self.interp_btn = QPushButton("Interpoler")

        self.save_btn = QPushButton("Sauvegarder les résultats")

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.import_btn)

        url_layout = QHBoxLayout()
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.start_date)
        url_layout.addWidget(self.end_date)
        url_layout.addWidget(self.download_btn)
        layout.addLayout(url_layout)

        layout.addWidget(self.column_selector)
        layout.addWidget(self.run_btn)
        layout.addWidget(self.stats_label)
        layout.addWidget(QLabel("Valeur seuil :"))
        layout.addWidget(self.threshold_input)
        layout.addWidget(self.threshold_result)
        layout.addWidget(QLabel("Mode d'interpolation :"))
        layout.addWidget(self.interp_mode)
        layout.addWidget(self.interp_btn)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.canvas)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Signals
        self.import_btn.clicked.connect(self.load_file)
        self.download_btn.clicked.connect(self.download_file)
        self.run_btn.clicked.connect(self.analyze_data)
        self.interp_btn.clicked.connect(self.interpolate)
        self.save_btn.clicked.connect(self.save_results)

        self.last_analysis = ""

    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Ouvrir fichier", "", "Excel Files (*.xlsx *.xls)")
        if path:
            self.data = pd.read_excel(path)
            self.column_selector.clear()
            self.column_selector.addItems(self.data.columns)

    def download_file(self):
        url = self.url_input.text()
        start = self.start_date.date().toString("yyyy-MM-dd")
        end = self.end_date.date().toString("yyyy-MM-dd")
        try:
            response = requests.get(f"{url}?start={start}&end={end}")
            if response.ok:
                self.data = pd.read_excel(BytesIO(response.content))
                self.column_selector.clear()
                self.column_selector.addItems(self.data.columns)
        except Exception as e:
            self.stats_label.setText(f"Erreur de téléchargement : {e}")

    def analyze_data(self):
        if self.data is None:
            return
        col = self.column_selector.currentText()
        values = self.data[col].dropna()
        mean_val = values.mean()
        min_val = values.min()
        max_val = values.max()

        self.stats_label.setText(f"Moyenne : {mean_val:.2f}, Min : {min_val:.2f}, Max : {max_val:.2f}")

        try:
            seuil = float(self.threshold_input.text())
            inf = (values < seuil).sum()
            sup = (values > seuil).sum()
            self.threshold_result.setText(f"< {seuil} : {inf}, > {seuil} : {sup}")
        except ValueError:
            self.threshold_result.setText("Seuil invalide")
            inf = sup = None

        self.last_analysis = (
            f"Donnée : {col}\n"
            f"Moyenne : {mean_val:.2f}, Min : {min_val:.2f}, Max : {max_val:.2f}\n"
            f"Seuil : {self.threshold_input.text()}\n"
            f"< Seuil : {inf}, > Seuil : {sup}\n"
        )

        self.plot_histogram()

    def plot_histogram(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        means = self.data.mean(numeric_only=True)
        means.plot(kind='bar', ax=ax)
        ax.set_title("Histogramme des moyennes")
        self.canvas.draw()

    def interpolate(self):
        if self.data is None:
            return
        col = self.column_selector.currentText()
        x = np.arange(len(self.data[col]))
        y = self.data[col].dropna().to_numpy()

        if self.interp_mode.currentText() == "cubic" and len(x) >= 4:
            kind = 'cubic'
        else:
            kind = 'linear'

        try:
            f = interp1d(np.arange(len(y)), y, kind=kind)
            xnew = np.linspace(0, len(y) - 1, 500)
            ynew = f(xnew)

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(xnew, ynew, label=f"Interpolation {kind}")
            ax.set_title(f"Interpolation {kind} de {col}")
            ax.legend()
            self.canvas.draw()
        except Exception as e:
            self.stats_label.setText(f"Erreur interpolation : {e}")

    def save_results(self):
        if not self.last_analysis:
            self.stats_label.setText("Aucune analyse à sauvegarder.")
            return

        filename, _ = QFileDialog.getSaveFileName(self, "Enregistrer les résultats", "resultats.txt", "Text Files (*.txt)")
        if filename:
            try:
                with open(filename, 'w') as file:
                    file.write(self.last_analysis)
                self.stats_label.setText(f"Résultats sauvegardés dans : {filename}")
            except Exception as e:
                self.stats_label.setText(f"Erreur lors de la sauvegarde : {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataAnalyzer()
    window.show()
    sys.exit(app.exec_())