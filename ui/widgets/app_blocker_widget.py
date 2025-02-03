import sys
import psutil
import winapps
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget,
    QMessageBox, QHBoxLayout, QListWidgetItem, QFrame
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class BlockAppsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.blocked_apps = set()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Titre de la page
        title = QLabel("Blocage d'Applications")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("color: #e74c3c; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Bouton pour rafraîchir la liste
        self.refresh_button = QPushButton("Rafraîchir la liste")
        self.refresh_button.setStyleSheet(self.get_button_style("#27ae60"))
        self.refresh_button.clicked.connect(self.load_installed_apps)
        layout.addWidget(self.refresh_button)
        
        # Liste des applications installées
        self.apps_list = QListWidget()
        self.apps_list.setStyleSheet(self.get_list_style())
        layout.addWidget(self.apps_list)
        
        # Charger les applications installées
        self.load_installed_apps()
    
    def load_installed_apps(self):
        """Charge les applications installées."""
        self.apps_list.clear()
        for app in winapps.search_installed():
            self.add_app_to_list(app.name)

    def add_app_to_list(self, name):
        """Ajoute une application avec un bouton à la liste."""
        item = QListWidgetItem(self.apps_list)

        # Conteneur horizontal (ligne)
        row_widget = QWidget()
        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(5, 5, 5, 5)

        # Nom de l'application
        label = QLabel(name)
        label.setFont(QFont("Arial", 14))
        row_layout.addWidget(label)

        # Bouton Bloquer / Débloquer
        button = QPushButton("Bloquer" if name not in self.blocked_apps else "Débloquer")
        button.setStyleSheet(self.get_button_style("#e74c3c" if name not in self.blocked_apps else "#3498db"))
        button.clicked.connect(lambda _, n=name, b=button: self.toggle_block_app(n, b))
        row_layout.addWidget(button)

        row_widget.setLayout(row_layout)
        item.setSizeHint(row_widget.sizeHint())

        self.apps_list.addItem(item)
        self.apps_list.setItemWidget(item, row_widget)

    def toggle_block_app(self, name, button):
        """Bloque ou débloque une application."""
        if name in self.blocked_apps:
            self.blocked_apps.remove(name)
            button.setText("Bloquer")
            button.setStyleSheet(self.get_button_style("#e74c3c"))
        else:
            self.blocked_apps.add(name)
            button.setText("Débloquer")
            button.setStyleSheet(self.get_button_style("#3498db"))
            self.block_application(name)
        
        self.load_installed_apps()  # Recharger la liste pour mettre à jour l'affichage

    def block_application(self, name):
        """Tente de bloquer une application en tuant ses processus."""
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == name:
                try:
                    p = psutil.Process(proc.info['pid'])
                    p.terminate()
                    QMessageBox.information(self, "Succès", f"L'application {name} a été bloquée.")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    QMessageBox.warning(self, "Erreur", f"Impossible de bloquer l'application {name}. Essayez en mode administrateur.")

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

    def get_list_style(self):
        return '''
            QListWidget {
                background-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        '''

    def darken_color(self, color):
        """Assombrit légèrement une couleur hexadécimale."""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darkened_rgb = tuple(max(0, min(255, int(c * 0.85))) for c in rgb)
        return f'#{darkened_rgb[0]:02x}{darkened_rgb[1]:02x}{darkened_rgb[2]:02x}'

