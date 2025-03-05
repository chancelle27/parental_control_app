from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,QLineEdit,QCheckBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Page des paramètres
class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(30, 30, 30, 30)

        # Titre de la page
        title = QLabel("Paramètres de l'utilisateur")
        title.setStyleSheet("font-size: 24px; color: #2c3e50; font-weight: bold;")
        layout.addWidget(title)

        # Formulaire de modification du mot de passe
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Nouveau mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(""" 
            QLineEdit {
                background-color: #f5f5f5;
                border: 2px solid #ccc;
                border-radius: 10px;
                font-size: 16px;
                padding: 10px;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #ffffff;
            }
        """)
        
        # Confirmer le mot de passe
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setPlaceholderText("Confirmer le mot de passe")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet("""
            QLineEdit {
                background-color: #f5f5f5;
                border: 2px solid #ccc;
                border-radius: 10px;
                font-size: 16px;
                padding: 10px;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #ffffff;
            }
        """)

        # Email pour notifications
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email pour les notifications")
        self.email_input.setStyleSheet("""
            QLineEdit {
                background-color: #f5f5f5;
                border: 2px solid #ccc;
                border-radius: 10px;
                font-size: 16px;
                padding: 10px;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #ffffff;
            }
        """)

        # Checkbox pour activer ou désactiver les notifications
        self.notifications_checkbox = QCheckBox("Activer les notifications", self)
        self.notifications_checkbox.setStyleSheet("font-size: 16px;")

        # Ajouter les champs au layout
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.notifications_checkbox)

        # Bouton de sauvegarde des paramètres
        self.save_button = QPushButton("Sauvegarder les paramètres", self)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 16px;
                padding: 12px;
                border-radius: 20px;
                border: none;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #2980b9;
                cursor: pointer;
            }
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
        """)
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

    def save_settings(self):
        # Validation des informations
        new_password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        email = self.email_input.text()

        if new_password and confirm_password and email:
            if new_password != confirm_password:
                QMessageBox.warning(self, "Erreur", "Les mots de passe ne correspondent pas")
                return

            # Ici, ajouter la logique pour mettre à jour le mot de passe et l'email
            # Exemple simple: stockage dans une variable ou base de données
            self.update_user_settings(new_password, email)
            
            QMessageBox.information(self, "Succès", "Les paramètres ont été enregistrés avec succès")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs")

    def update_user_settings(self, new_password, email):
        # Logique pour mettre à jour les paramètres de l'utilisateur
        # Par exemple, dans une base de données ou un fichier de configuration.
        print(f"Mot de passe mis à jour: {new_password}, Email des notifications: {email}")
