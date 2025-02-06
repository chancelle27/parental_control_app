from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox
)
from PyQt5.QtCore import Qt
import json
import os
import hashlib

class AuthPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        # Style commun pour les widgets
        self.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 16px;
                margin-bottom: 5px;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
                margin-bottom: 15px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        # Titre
        title = QLabel("Authentification")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Champs de saisie
        self.username_label = QLabel("Nom d'utilisateur:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Entrez votre nom d'utilisateur")
        
        self.password_label = QLabel("Mot de passe:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Entrez votre mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        # Bouton de connexion
        self.login_button = QPushButton("Se connecter")
        self.login_button.clicked.connect(self.handle_authentication)
        
        # Ajout des widgets au layout
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        
        # Centrer les widgets et ajouter des marges
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(10)
    
    def hash_password(self, password):
        """Hash le mot de passe avec SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def save_credentials(self, username, password_hash):
        """Sauvegarde les identifiants dans un fichier JSON"""
        credentials = {
            'username': username,
            'password': password_hash
        }
        with open('credentials.json', 'w') as f:
            json.dump(credentials, f)
    
    def load_credentials(self):
        """Charge les identifiants depuis le fichier JSON"""
        try:
            with open('credentials.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def is_first_login(self):
        """Vérifie s'il s'agit de la première connexion"""
        return not os.path.exists('credentials.json')
    
    def handle_authentication(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs")
            return
        
        if self.is_first_login():
            # Première connexion : enregistrement des identifiants
            confirmation = QMessageBox.question(
                self,
                "Première connexion",
                "Voulez-vous enregistrer ces identifiants pour les futures connexions ?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if confirmation == QMessageBox.Yes:
                self.save_credentials(username, self.hash_password(password))
                QMessageBox.information(self, "Succès", "Identifiants enregistrés avec succès!")
                self.main_window.show_main_content()
        else:
            # Connexion normale : vérification des identifiants
            stored_credentials = self.load_credentials()
            if (stored_credentials and
                stored_credentials['username'] == username and
                stored_credentials['password'] == self.hash_password(password)):
                self.main_window.show_main_content()
            else:
                QMessageBox.warning(self, "Erreur", "Identifiants incorrects")