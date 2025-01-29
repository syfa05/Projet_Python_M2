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