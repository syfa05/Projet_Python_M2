import sys
from PyQt5 import QtWidgets
from SONKOUE_YEMLONG_Fresnel_gui_ui import Ui_MainWindow
#from Exitpage_gui_ui import Ui_Dialog
from importurl import Ui_Dialog
# Creation de la classe App qui herite de la classe Ui_MainWindow
    

class App(Ui_MainWindow, Ui_Dialog):
    def __init__(self, dialog):
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)
        # Connection du signal .clicked() avec le slot .calculate()
        self.pushButton.clicked.connect(self.calculate)
        self.pushButton_2.clicked.connect(self.reset)
        self.pushButton_3.clicked.connect(self.show_exit_dialog)

    def show_exit_dialog(self):
        exit_dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(exit_dialog)
        exit_dialog.exec_()
        #self.QDialogButtonBox.accepted.connect(QtWidgets.QApplication.allWidgets().exit)
        #ui.buttonBox.hide()
        #ui.buttonBox.accepted.connect(QtWidgets.qApp.)
        #ui.buttonBox.rejected.connect(QtWidgets.QApplication.quit)
        ui.pushButton_20.clicked.connect(exit_dialog.close) 

# Creation d'un slot pour faire le calcul
    def calculate(self):
        self.statusbar.clearMessage()
        result = self.spinBox.value()/self.spinBox_2.value()
        print("CALCUL FAIT :", self.lineEdit.text(), "*", self.spinBox.value())
        #print("CALCUL FAIT :", result)
        print("CALCUL FAIT :", self.lineEdit.text(), "* (", self.spinBox.value(),"/", self.spinBox_2.value(),")")
        if (self.lineEdit.text().isnumeric()):
            self.lcdNumber.display(int(self.lineEdit.text()) * self.spinBox.value())
            self.lcdNumber_2.display(int(self.lineEdit.text()) * (self.spinBox.value() / self.spinBox_2.value()))
        else:
            self.statusbar.showMessage(
            "Erreur : texte entré à la place d'une valeur numérique !")
            
    def reset(self):
        
        self.lineEdit.clear()
        self.spinBox.setValue(0)
        self.spinBox_2.setValue(0)
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()
    #Dialog = QtWidgets.QDialog()
    clement = App(dialog)
    #fresnel = App(Dialog)
    dialog.show()
    #Dialog.show()   
    sys.exit(app.exec_())