from PyQt5 import QtWidgets 
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox, QFormLayout  
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QSpinBox, QLCDNumber
from PyQt5.QtCore import pyqtSlot , QTimer ,QUrl
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
        
        date_debut = self.ui.dateEdit.date()
        date_fin = self.ui.dateEdit_2.date()
    # Convertir les dates en chaînes de caractères au format "yyyy-MM-dd"
        str_date_debut = date_debut.toString("yyyy-MM-dd")
        str_date_fin = date_fin.toString("yyyy-MM-dd")
        
        # Créer une instance de la classe ExcelDataHandler
        excel_handler = ExcelDataHandler(str_date_debut, str_date_fin).save_url_to_excel()
        # Appeler la méthode pour importer les données à partir de l'URL
        url_handler = ExcelDataHandler(str_date_debut, str_date_fin).generate_url()
        # Appeler la méthode pour importer les données à partir de l'URL
        if excel_handler is not None:
            # Afficher un message de succès
            print("Données importées avec succès")
            time.sleep(4)
            QMessageBox.information(self, "Success", "Données importées avec succès")
        else:
            # Afficher un message d'erreur
            print("Erreur lors de l'importation des données")
            print(str_date_debut, str_date_fin)
            print(url_handler)
            time.sleep(4)
            QMessageBox.critical(self, "Error", "Erreur lors de l'importation des données")
        # Fermer la fenêtre de dialogue après l'importation réussie
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
        self.progressBar_2.setValue(0)
        self.pushButton_12.clicked.connect(self.fonctionInterpolation)
       
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
     
    
    def afficher_graphe(self, stats,colonne):
        # Générer le fichier HTML avec le graphique
        data_analyzer = DataAnalyzer('output.xlsx')
        data = data_analyzer.get_column_statistics(colonne)
        html_file = data_analyzer.plot_histograms(data, value_type='mean_Total')

        if html_file is None:
            return

        # Nettoyer le layout du widget avant d’ajouter un nouveau graphique
        layout = self.openGLWidget.layout()
        if layout is not None:
            for i in reversed(range(layout.count())):
                widget_to_remove = layout.itemAt(i).widget()
                if widget_to_remove:
                    widget_to_remove.setParent(None)

        else:
            # Si aucun layout n'était défini
            from PyQt5.QtWidgets import QVBoxLayout
            self.openGLWidget.setLayout(QVBoxLayout())
            layout = self.openGLWidget.layout()

        # Affichage dans le widget
        web_view = QWebEngineView()
        web_view.load(QUrl.fromLocalFile(html_file))
        layout.addWidget(web_view)
 
                
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
        Histogram = self.afficher_graphe(start_data["mean_Total"],colonne_name)
        # Afficher le graphique dans le widget OpenGL
        
    def showplot(self,html_file):
        
        # Nettoyer le layout du widget avant d’ajouter un nouveau graphique
        layout = self.openGLWidget_2.layout()
        if layout is not None:
            for i in reversed(range(layout.count())):
                widget_to_remove = layout.itemAt(i).widget()
                if widget_to_remove:
                    widget_to_remove.setParent(None)

        else:
            # Si aucun layout n'était défini
            from PyQt5.QtWidgets import QVBoxLayout
            self.openGLWidget_2.setLayout(QVBoxLayout())
            layout = self.openGLWidget_2.layout()

        # Affichage dans le widget
        web_view = QWebEngineView()
        web_view.load(QUrl.fromLocalFile(html_file))
        layout.addWidget(web_view)
        
       
    def fonctionInterpolation(self):
        # Créer une instance de DataAnalyzer
        data_analyzer = DataAnalyzer('output.xlsx')
        # Appeler la méthode pour analyser les données
        date_name = self.comboBox_2.currentText()
        interpolation = self.comboBox_3.currentText()
        # Appeler la méthode pour analyser les données
        if interpolation == "cubic_spline_interpolation":
            html_file1 =data_analyzer.plot_cubic_spline_interpolation(date_name)
            result1 = self.showplot(html_file1)
        elif interpolation == "polynomial_interpolation":
            html_file2 = data_analyzer.plot_polynomial_interpolation(date_name)
            result2 = self.showplot(html_file2)
        elif interpolation == "bets_optimation_interpolation": 
            html_file3 =data_analyzer.plot_best_fit_interpolation(date_name)
            result = self.showplot(html_file3)
            

        
    
    

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