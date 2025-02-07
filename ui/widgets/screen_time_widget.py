import sys
import time
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox,
    QMessageBox, QHBoxLayout, QLineEdit, QFormLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
import winapps
import psutil

class ScreenTimePage(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.current_app = None
        self.start_time = None
        self.elapsed_time = 0
        self.time_limit = 0  # Temps limite en secondes
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Titre du widget
        title = QLabel("Gestion du Temps d'Écran")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)

        # Sélecteur d'application
        self.app_selector = QComboBox()
        self.app_selector.setFont(QFont("Arial", 12))
        self.app_selector.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #bdc3c7;")
        self.app_selector.currentIndexChanged.connect(self.select_app)
        layout.addWidget(QLabel("Sélectionnez une application :"))
        layout.addWidget(self.app_selector)

        # Charger les applications installées
        self.load_installed_apps()

        # Affichage du temps passé
        self.time_label = QLabel("Temps passé : 0 secondes")
        self.time_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.time_label)

        # Champ pour définir la limite de temps
        self.time_limit_input = QLineEdit()
        self.time_limit_input.setPlaceholderText("Entrez la limite de temps en minutes")
        self.time_limit_input.setFont(QFont("Arial", 12))
        self.time_limit_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #bdc3c7;")
        layout.addWidget(QLabel("Définir une limite de temps (en minutes) :"))
        layout.addWidget(self.time_limit_input)

        # Bouton pour appliquer la limite
        self.set_limit_button = QPushButton("Appliquer la limite")
        self.set_limit_button.setStyleSheet(self.get_button_style("#27ae60"))
        self.set_limit_button.clicked.connect(self.set_time_limit)
        layout.addWidget(self.set_limit_button)

        # Bouton pour démarrer/arrêter le suivi
        self.toggle_tracking_button = QPushButton("Démarrer le suivi")
        self.toggle_tracking_button.setStyleSheet(self.get_button_style("#3498db"))
        self.toggle_tracking_button.clicked.connect(self.toggle_tracking)
        layout.addWidget(self.toggle_tracking_button)

    def load_installed_apps(self):
        """Charge les applications installées dans le sélecteur."""
        self.app_selector.clear()
        for app in winapps.search_installed():
            self.app_selector.addItem(app.name)

    def select_app(self):
        """Met à jour l'application sélectionnée."""
        self.current_app = self.app_selector.currentText()
        self.elapsed_time = 0
        self.update_time_label()

    def update_time_label(self):
        """Met à jour l'affichage du temps passé."""
        # self.time_label.setText(f"Temps passé : {self.elapsed_time} secondes")

    def set_time_limit(self):
        """Définit la limite de temps."""
        try:
            limit_minutes = int(self.time_limit_input.text())
            self.time_limit = limit_minutes * 60  # Convertir en secondes
            QMessageBox.information(self, "Succès", f"Limite de temps définie à {limit_minutes} minutes.")
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un nombre valide.")

    def toggle_tracking(self):
        """Démarre ou arrête le suivi du temps."""
        if not self.current_app:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une application.")
            return

        if self.timer.isActive():
            self.timer.stop()
            self.toggle_tracking_button.setText("Démarrer le suivi")
            self.toggle_tracking_button.setStyleSheet(self.get_button_style("#3498db"))
        else:
            self.start_time = time.time()
            self.timer.start(1000)  # Mettre à jour toutes les secondes
            self.toggle_tracking_button.setText("Arrêter le suivi")
            self.toggle_tracking_button.setStyleSheet(self.get_button_style("#e74c3c"))

    def update_time(self):
        """Met à jour le temps passé et vérifie la limite."""
        if self.current_app:
            self.elapsed_time = int(time.time() - self.start_time)
            self.update_time_label()

            # Vérifier si la limite de temps est atteinte
            if self.time_limit > 0 and self.elapsed_time >= self.time_limit:
                self.timer.stop()
                self.toggle_tracking_button.setText("Démarrer le suivi")
                self.toggle_tracking_button.setStyleSheet(self.get_button_style("#3498db"))
                self.block_application(self.current_app)
                QMessageBox.warning(self, "Limite atteinte", f"La limite de temps pour {self.current_app} a été atteinte.")

    def block_application(self, name):
        """Bloque l'application en tuant ses processus."""
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == name:
                try:
                    p = psutil.Process(proc.info['pid'])
                    p.terminate()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

    def get_button_style(self, color):
        return f'''
            QPushButton {{
                background-color: {color};
                color: white;
                font-size: 14px;
                padding: 8px;
                border-radius: 5px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
        '''

    def darken_color(self, color):
        """Assombrit légèrement une couleur hexadécimale."""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darkened_rgb = tuple(max(0, min(255, int(c * 0.85))) for c in rgb)
        return f'#{darkened_rgb[0]:02x}{darkened_rgb[1]:02x}{darkened_rgb[2]:02x}'
