from PyQt5 import QtWidgets 
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox, QFormLayout  
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QSpinBox, QLCDNumber
from PyQt5.QtCore import pyqtSlot , QTimer
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
        
      
        # Créer une instance de la classe ExcelDataHandler
        excel_handler = ExcelDataHandler(self.ui.dateEdit, self.ui.dateEdit_2)
        # Attente de 5 secondes
        time.sleep(5)
        # Nom du fichier de sortie  
        output_file = 'output.xlsx'
        # Appeler la fonction pour sauvegarder les données de l'URL dans un fichier Excel
        excel_handler.save_url_to_excel(output_file)
        print("Données importées avec succès")
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
        self.pushButton_6.clicked.connect(self.indicateurstatistique)
        self.progressBar.setValue(0)
       
# Creation de la class App qui herite de la classe Ui_MainWindow
                  
    def open_form_window(self):
        self.form = FormWindow(self)
        self.form.show()  # ou self.form.exec_() si tu veux bloquer la mainwindow pendant

    
    def exceldata(self):
        # Importer les données à partir d'un fichier Excel
        imported_data = FileHandler.import_and_save_excel_file()
        if imported_data is not None:
            
            print("Données importées avec succès")
            # Fermer la fenêtre de dialogue après l'importation réussie
            
        else:
            print("Aucune donnée importée")  
                            
    def goto_tab1(self):
        self.Main_Table.setCurrentIndex(0) 
        
    def goto_tab2(self):
        self.Main_Table.setCurrentIndex(1)
        
    def goto_tab3(self):
        self.Main_Table.setCurrentIndex(2)
        
    def update_progress(self):
        self.progress_value += 1
        self.progressBar.setValue(self.progress_value)

        if self.progress_value >= 100:
            self.timer.stop()
            print("Fin du délai de 10 secondes")
                
    def indicateurstatistique(self):
        # Créer une instance de DataAnalyzer
        data_analyzer = DataAnalyzer('output.xlsx')
        colonne_name = self.comboBox.currentText()
        # Appeler la méthode pour analyser les données
        start_data = data_analyzer.get_column_statistics(colonne_name)
       
        # Afficher les résultats dans les LCDNumber
        self.lcdNumber.display(start_data["maxi"])
        self.lcdNumber_4.display(start_data["mini"])
        self.lcdNumber_5.display(start_data["moyenne"])
        seuil_conso = self.spinBox.value()
        j_sup , j_inf = data_analyzer.count_days_by_seuil(seuil_conso,colonne_name)
        self.lcdNumber_3.display(j_sup)
        self.lcdNumber_8.display(j_inf)
        
        self.progressBar.setValue(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.progress_value = 0
        self.timer.start(100)  # 100 ms = 0.1 
        

        
    
    

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