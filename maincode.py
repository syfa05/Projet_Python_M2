from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox, QFormLayout
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QSpinBox, QLCDNumber
from PyQt5.QtCore import pyqtSlot
import sys
import time
from urltoexcel import FileHandler,ExcelDataHandler,DataAnalyzer
from interface_qt import Ui_MainWindow  # Assurez-vous que le fichier interface_qt.py contient une classe Ui_MainWindow
from importurl import Ui_Form
from datetime import datetime


class FormWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton_20.clicked.connect(self.urlimport)
        # Bouton "Cancel" pour fermer juste cette fenêtre
        self.ui.pushButton_21.clicked.connect(self.close)
        
    def urlimport(self):
        time.sleep(8)
        self.date_debut = self.ui.dateEdit.date().toString("yyyy-MM-dd")
        self.date_fin = self.ui.dateEdit_2.date().toString("yyyy-MM-dd")
        # Convertir les dates au format "yyyy-MM-dd"
        # Convertir les variables de type QDate en chaînes de caractères au format "yyyy-MM-dd"
        debut_string = f"{self.date_debut}"
        fin_string = f"{self.date_fin}"
        time.sleep(1)
        print(debut_string, fin_string)
        # Créer une instance de la classe ExcelDataHandler
        excel_handler = ExcelDataHandler(debut_string, fin_string)
        # Attente de 5 secondes
        time.sleep(5)
        # Nom du fichier de sortie  
        output_file = 'output.xlsx'
        # Appeler la fonction pour sauvegarder les données de l'URL dans un fichier Excel
        excel_handler.save_url_to_excel(output_file)
        print("Données importées avec succès")
        # Attente de 10 secondes
        #time.sleep(15)
        # Fermer la fenêtre de dialogue après l'importation réussie
        QMessageBox.information(self, "Success", "Données importées avec succès")
        self.close()


class App(Ui_MainWindow, Ui_Form):
    def __init__(self, dialog):
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)
        self.Main_Table.setCurrentIndex(0)
                
        self.pushButton.clicked.connect(exit)
        self.pushButton_11.clicked.connect(exit)
        self.pushButton_7.clicked.connect(exit)
        self.pushButton_1.clicked.connect(self.goto_tab2)
        self.pushButton_8.clicked.connect(self.goto_tab1)
        self.pushButton_9.clicked.connect(self.goto_tab2)
        self.commandLinkButton.clicked.connect(self.goto_tab3)
        self.pushButton_5.clicked.connect(self.exceldata)
        self.pushButton_13.clicked.connect(self.open_form_window)
        
       
# Creation de la class App qui herite de la classe Ui_MainWindow
    
    def importdata_online(self):
        exit_dialog = QtWidgets.QDialog()
        ui = Ui_Form()
        ui.setupUi(exit_dialog)
        exit_dialog.exec_()
        #ui.pushButton_20.clicked.connect(exit(Ui_Dialog))  
        #date_debut = ui.dateEdit.date().toString("yyyy-MM-dd")
        #date_fin = ui.dateEdit_2.date().toString("yyyy-MM-dd")
        #print(date_debut,date_fin)
        #ui.pushButton_21.clicked.connect(ExcelDataHandler(date_debut, date_fin))
        ui.pushButton_21.clicked.connect(exit_dialog.close)  
               
    def open_form_window(self):
        self.form = FormWindow(self)
        self.form.show()  # ou self.form.exec_() si tu veux bloquer la mainwindow pendant

    
    def exceldata(self):
        # Importer les données à partir d'un fichier Excel
        imported_data = FileHandler.import_and_save_excel_file()
        if imported_data is not None:
            
            print("Données importées avec succès")
            # Fermer la fenêtre de dialogue après l'importation réussie
            QMessageBox.information(self, "Success", "Données importées avec succès")
        else:
            print("Aucune donnée importée")  
                            
    def goto_tab1(self):
        self.Main_Table.setCurrentIndex(0) 
        
    def goto_tab2(self):
        self.Main_Table.setCurrentIndex(1)
        
    def goto_tab3(self):
        self.Main_Table.setCurrentIndex(2)
        
    def  dataprocessing(self):
        # Créer une instance de DataAnalyzer
        data_analyzer = DataAnalyzer('output.xlsx')
        # Appeler la méthode pour analyser les données
        data_analyzer.analyze_data()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()
    #Dialog = QtWidgets.QDialog()
    Fresnel = App(dialog)
    #fresnel = App(Dialog)
    dialog.show()
    #Dialog.show()   
    sys.exit(app.exec_())
    
"""
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
    
   
    
class App(Ui_MainWindow, Ui_Dialog):
def __init__(self, dialog):
    Ui_MainWindow.__init__(self)
    self.setupUi(dialog)
    # Connection du signal .clicked() avec le slot .calculate()
    
    #self.pushButton.clicked.connect(self.calculate)
    #self.pushButton_2.clicked.connect(self.reset)
    self.pushButton.clicked.connect(self.show_exit_dialog)
    #self.pushButton_3.clicked.connect(self.show_exit_dialog)
    
    """