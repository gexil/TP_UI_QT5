# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------

# Import des objets de la bibliothèque PyQt5 utilisés pour gérer les interfaces graphiques QT  
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QMessageBox
from PyQt5 import QtGui
from PyQt5.uic import loadUi

# Notre widget bar d'outils de la bibliothèque MatplotLib
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

# Quelques bibliotheques scientifiques python, un must have :) !
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

# GraphicWindow est notre classe de gestion de la fenêtre d'affichage graphique
class GraphicWindow(QMainWindow):
    
    # Fonction d'initialisation de la class GraphicWindow
    def __init__(self):
        
        # Initialisation nécessaire pour hériter des propriétaires de la classe parente QMAinWindow
        super().__init__()

        # Chargement du design de notre fenêtre graphique
        loadUi("interfaces/display.ui",self)

        # On définit la taille de notre fenêtre
        self.width = 500
        self.height = 500
        self.setGeometry(0, 0, self.width, self.height)

        # on définit un titre pour notre fenêtre
        self.setWindowTitle("Mon graphique")

        # On définit une icône
        self.setWindowIcon(QtGui.QIcon('images/llbOrphee.png'))

        # Notre widget bar d'outils de la bibliothèque MatplotLib
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))
        
        # Definition des actions des boutons
        self.button_Fit.clicked.connect(self.button_Fit_click)

    
    # Fonction qui récupère les informations pour la lecture et l'affichage de données
    # data_filename : chemin du fichier de donnée à lire
    # column_x      : colonne des données dans notre fichier pour l'axe des x
    # column_y      : colonne des données dans notre fichier pour l'axe des y
    def set_data(self, data_filename, column_x, column_y):
        
        # Lecture du fichier de donnée CSV avec la bibliothèque PANDAS
        dataframe = pd.read_csv(data_filename, header=None)
        self.data = dataframe.values

        # Selection des colonnes
        x, y = self.data[:, column_x], self.data[:, column_y]
        
        # Création du module graphique MatplotLib et affichage des données 
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.scatter(x,y)
        self.MplWidget.canvas.axes.set_title('Data')
        self.MplWidget.canvas.draw()

    # function model pour le fit
    def modelfunc(self, x, a, b, c, d):
        return a * np.sin(b - x) + c * x**2 + d

    # Fonction de gestion du bouton click
    def button_Fit_click(self):
        # Selection des colonnes
        x, y = self.data[:, 4], self.data[:, -1]

        # fitting
        popt, _ = curve_fit(self.modelfunc, x, y)
        a, b, c, d = popt
        x_line = np.arange(min(x), max(x), 1)
        y_line = self.modelfunc(x_line, a, b, c, d)

        # Affichage de la courbe de fit
        self.MplWidget.canvas.axes.plot(x_line, y_line, '--', color='red')
        self.MplWidget.canvas.draw()
        
# AboutDialog est notre classe de gestion de la boite de dialogue About
class AboutDialog(QDialog):
    
    # Fonction d'initialisation de la class AboutDialog
    def __init__(self):
        
        # Initialisation nécessaire pour hériter des propriétaires de la classe parente QDialog
        super().__init__()

        # Chargement du design de notre dialogue
        loadUi("interfaces/about.ui",self)

        # on définit un titre
        self.setWindowTitle("About")

        # On définit une icône
        self.setWindowIcon(QtGui.QIcon('images/llbOrphee.png'))

        # On active le mode modal pour cette boite de dialogue
        # ce qui signifie qu'il faudra la fermer pour pouvoir interagir de nouveau avec l'application
        self.setModal(True)

        # Définition de l'action du bouton close
        self.button_Close.clicked.connect(self.button_Close_click)

    # Fonction de gestion du bouton click
    def button_Close_click(self):
        self.close()




#MainWindow est notre classe de gestion de la fenêtre principale
class MainWindow(QMainWindow):
    
    # Fonction d'initialisation de la class MainWindow
    def __init__(self):
        
        # Initialisation nécessaire pour hériter des propriétaires de la classe parente QMAinWindow
        super().__init__()

        # Chargement du design de notre fenêtre principale
        loadUi("interfaces/main.ui",self)

        # On définit la taille de notre fenêtre
        self.width = 677
        self.height = 287
        self.setGeometry(0, 0, self.width, self.height)
        # On fait en sorte que la taille soit fixe, on ne pourra pas redimmensionner la fenetre
        self.setMinimumSize(self.width,self.height)
        self.setMaximumSize(self.width,self.height)

        # on définit un titre pour notre fenêtre
        self.setWindowTitle("Mon application")

        # On définit une icône
        self.setWindowIcon(QtGui.QIcon('images/llbOrphee.png'))
        
        # Les fonctions du menu
        # Menu Open 
        self.actionOpen.setStatusTip('Open a configuration file for the application')
        self.actionOpen.setShortcut('Ctrl+O')
        self.actionOpen.triggered.connect(self.actionOpen_click)
        
        # Menu Exit
        self.actionExit.setStatusTip('Exit application')
        self.actionExit.setShortcut('Ctrl+E')
        self.actionExit.triggered.connect(self.actionExit_click)
        
            
        # Menu About
        self.actionAbout.setStatusTip('About')
        self.actionAbout.triggered.connect(self.actionAbout_click)

        # Valeur par défaut pour lineEdit_x
        self.lineEdit_x.setText("4")
        # Seul les valeurs entières de -1 à 6 seront acceptées. 
        self.lineEdit_x.setValidator(QtGui.QIntValidator(-1, 6) )
        
        # Valeur par défaut pour lineEdit_y
        self.lineEdit_y.setText("-1")
        # Seul les valeurs entières de 0 à 6 seront acceptées. 
        self.lineEdit_y.setValidator(QtGui.QIntValidator(-1, 6) )

        # Definition des actions des boutons
        self.button_Show.clicked.connect(self.button_Show_click)

        # Création de ma fenêtre d'affichage graphique
        self.display_window = GraphicWindow()

        # Création de la boite de dialogue About
        self.about_dialog = AboutDialog()

    # Fonction de gestion du menu Open
    def actionOpen_click(self):
        selected_filename, _ = QFileDialog.getOpenFileName(self, "Open data file", "", "CSV files (*.csv)")
        
        if(selected_filename):
            self.lineEdit_filename.setText(selected_filename)
            self.lineEdit_x.setEnabled(True)
            self.lineEdit_y.setEnabled(True)
            self.button_Show.setEnabled(True)
            self.log_textEdit.setEnabled(True)

            with open(selected_filename) as f:
                lines = f.read()

            self.log_textEdit.setText(lines)

 
    # Fonction de gestion du menu Exit
    def actionExit_click(self):
        self.exit_application()

    # Fonction de gestion du menu About
    def actionAbout_click(self):
        self.about_dialog.show()

    # Fonction de gestion du bouton Show
    def button_Show_click(self):
                  
        selected_filename = self.lineEdit_filename.text()
        column_x = int(self.lineEdit_x.text())
        column_y = int(self.lineEdit_y.text())

        # On crée le graphique
        self.display_window.set_data(selected_filename, column_x, column_y)

        # On affiche la fenêtre
        self.display_window.show()

    # Fonction de sortie d'application
    def exit_application(self):
            self.close()
        
    # Fonction qui récupère l'événement close, lors de la fermeture de l'application
    # pour effectuer quelques commande avant l'exécution finale de l'événement close
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'On est pas bien ensemble', 'Vous nous quittez déjà :( ?',
				QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                
        if reply == QMessageBox.Yes:
            event.accept()
            self.display_window.close()
        else:
            # On annule l'événement close
            event.ignore() 

# Programme principale
if __name__ == '__main__':
    # initialisation de application QT
    app = QApplication([])
    # Création de la fenêtre principale
    main_window = MainWindow()
    # Affichage de la fenêtre principale
    main_window.show()
    # Fin de l'application QT
    app.exec_()