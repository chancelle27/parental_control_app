from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, 
    QCheckBox, QFrame, QMessageBox, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Titre principal
        title = QLabel("Paramètres de l'utilisateur")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # ----- Carte : Modification du mot de passe ----- #
        account_card = QFrame()
        account_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        account_layout = QVBoxLayout(account_card)
        account_layout.setSpacing(15)

        account_title = QLabel("Modifier le mot de passe")
        account_title.setFont(QFont("Arial", 18, QFont.Bold))
        account_title.setStyleSheet("color: #34495e;")
        account_layout.addWidget(account_title)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Nouveau mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #f5f5f5;
                border: 1px solid #bdc3c7;
                border-radius: 10px;
                font-size: 16px;
                padding: 10px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
                background-color: white;
            }
        """)
        account_layout.addWidget(self.password_input)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirmer le mot de passe")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet("""
            QLineEdit {
                background-color: #f5f5f5;
                border: 1px solid #bdc3c7;
                border-radius: 10px;
                font-size: 16px;
                padding: 10px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
                background-color: white;
            }
        """)
        account_layout.addWidget(self.confirm_password_input)

        save_account_button = QPushButton("Sauvegarder le mot de passe")
        save_account_button.setFont(QFont("Arial", 16))
        save_account_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
        """)
        save_account_button.clicked.connect(self.save_account_settings)
        account_layout.addWidget(save_account_button)

        # Ajout d'une ombre portée pour la carte
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 80))
        account_card.setGraphicsEffect(shadow)

        main_layout.addWidget(account_card)

        # ----- Carte : Paramètres de Notification ----- #
        notification_card = QFrame()
        notification_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        notif_layout = QVBoxLayout(notification_card)
        notif_layout.setSpacing(15)

        notif_title = QLabel("Paramètres de Notification")
        notif_title.setFont(QFont("Arial", 18, QFont.Bold))
        notif_title.setStyleSheet("color: #34495e;")
        notif_layout.addWidget(notif_title)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email pour les notifications")
        self.email_input.setStyleSheet("""
            QLineEdit {
                background-color: #f5f5f5;
                border: 1px solid #bdc3c7;
                border-radius: 10px;
                font-size: 16px;
                padding: 10px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
                background-color: white;
            }
        """)
        notif_layout.addWidget(self.email_input)

        self.notifications_checkbox = QCheckBox("Activer les notifications")
        self.notifications_checkbox.setStyleSheet("font-size: 16px; color: #2c3e50;")
        notif_layout.addWidget(self.notifications_checkbox)

        save_notif_button = QPushButton("Sauvegarder les notifications")
        save_notif_button.setFont(QFont("Arial", 16))
        save_notif_button.setStyleSheet("""
            QPushButton {
                background-color: #1abc9c;
                color: white;
                padding: 10px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #16a085;
            }
            QPushButton:pressed {
                background-color: #149174;
            }
        """)
        save_notif_button.clicked.connect(self.save_notification_settings)
        notif_layout.addWidget(save_notif_button)

        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(15)
        shadow2.setXOffset(0)
        shadow2.setYOffset(2)
        shadow2.setColor(QColor(0, 0, 0, 80))
        notification_card.setGraphicsEffect(shadow2)

        main_layout.addWidget(notification_card)

    def save_account_settings(self):
        new_password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()

        if not new_password or not confirm_password:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs du mot de passe.")
            return
        if new_password != confirm_password:
            QMessageBox.warning(self, "Erreur", "Les mots de passe ne correspondent pas.")
            return

        # Logique pour mettre à jour le mot de passe (exemple : mise à jour dans une base de données)
        self.update_account_settings(new_password)
        QMessageBox.information(self, "Succès", "Le mot de passe a été mis à jour.")

    def save_notification_settings(self):
        email = self.email_input.text().strip()
        notifications_enabled = self.notifications_checkbox.isChecked()

        if not email:
            QMessageBox.warning(self, "Erreur", "Veuillez renseigner un email pour les notifications.")
            return

        # Logique pour mettre à jour les paramètres de notification
        self.update_notification_settings(email, notifications_enabled)
        QMessageBox.information(self, "Succès", "Les paramètres de notification ont été mis à jour.")

    def update_account_settings(self, new_password):
        # Exemple : mise à jour dans une base de données ou fichier de configuration
        print(f"Nouveau mot de passe enregistré : {new_password}")

    def update_notification_settings(self, email, notifications_enabled):
        # Exemple : sauvegarde des paramètres de notification
        print(f"Email : {email}, Notifications activées : {notifications_enabled}")
