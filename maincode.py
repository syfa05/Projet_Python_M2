from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QSpinBox, QLCDNumber
from PyQt5.QtCore import pyqtSlot
import sys
from urltoexcel import FileHandler,ExcelDataHandler
from interface_qt import Ui_MainWindow  # Assurez-vous que le fichier interface_qt.py contient une classe Ui_MainWindow
from importurl import Ui_Dialog

class App(Ui_MainWindow, Ui_Dialog):
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
        self.pushButton_13.clicked.connect(self.importdata_online)
        
       
# Creation de la class App qui herite de la classe Ui_MainWindow
    
    def importdata_online(self):
        exit_dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(exit_dialog)
        exit_dialog.exec_()
        #ui.pushButton_20.clicked.connect(exit(Ui_Dialog))  
        #date_debut = ui.dateEdit.date().toString("yyyy-MM-dd")
        #date_fin = ui.dateEdit_2.date().toString("yyyy-MM-dd")
        #print(date_debut,date_fin)
        #ui.pushButton_21.clicked.connect(ExcelDataHandler(date_debut, date_fin))
        ui.pushButton_21.clicked.connect(exit_dialog.close)         
    
    def exceldata(self):
        # Importer les données à partir d'un fichier Excel
        imported_data = FileHandler.import_and_save_excel_file()
        if imported_data is not None:
            print("Données importées avec succès")
        else:
            print("Aucune donnée importée")  
                            
    def goto_tab1(self):
        self.Main_Table.setCurrentIndex(0) 
        
    def goto_tab2(self):
        self.Main_Table.setCurrentIndex(1)
        
    def goto_tab3(self):
        self.Main_Table.setCurrentIndex(2) 

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