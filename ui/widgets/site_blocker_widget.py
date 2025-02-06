import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Détection du fichier hosts selon l'OS
HOSTS_PATH = "C:\\Windows\\System32\\drivers\\etc\\hosts" if sys.platform == "win32" else "/etc/hosts"

# Configuration de MailHog
MAILHOG_SMTP_SERVER = "localhost"
MAILHOG_SMTP_PORT = 1025
MAILHOG_FROM_EMAIL = "no-reply@example.com"
MAILHOG_TO_EMAIL = "admin@example.com"

class BlockSitesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Titre de la page
        title = QLabel("Blocage de Sites")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #e74c3c; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Champ de saisie
        self.site_input = QLineEdit()
        self.site_input.setPlaceholderText("Entrez l'URL du site à bloquer (ex: facebook.com)")
        self.site_input.setStyleSheet(""" 
            QLineEdit {
                padding: 10px;
                font-size: 16px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        layout.addWidget(self.site_input)
        
        # Boutons "Ajouter" et "Supprimer"
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Ajouter le site")
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.add_button.clicked.connect(self.add_blocked_site)
        button_layout.addWidget(self.add_button)
        
        self.remove_button = QPushButton("Supprimer le site")
        self.remove_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.remove_button.clicked.connect(self.remove_blocked_site)
        button_layout.addWidget(self.remove_button)
        
        layout.addLayout(button_layout)
        
        # Liste des sites bloqués
        self.blocked_sites_list = QListWidget()
        self.blocked_sites_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #bdc3c7;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        layout.addWidget(self.blocked_sites_list)
        
        # Charger les sites bloqués
        self.load_blocked_sites()

    def add_blocked_site(self):
        site_url = self.site_input.text().strip()
        if site_url:
            if self.is_site_blocked(site_url):
                QMessageBox.warning(self, "Erreur", "Ce site est déjà bloqué.")
                return
            
            self.blocked_sites_list.addItem(site_url)
            self.block_site_in_hosts(site_url)
            self.site_input.clear()
            # Envoyer un mail de notification
            self.send_email_notification(site_url)
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer une URL valide.")
    
    def send_email_notification(self, site_url):
        """Envoie un e-mail de notification via MailHog"""
        subject = f"Tentative d'accès à un site bloqué : {site_url}"
        body = f"Une tentative d'accès au site bloqué {site_url} a été détectée."

        msg = MIMEMultipart()
        msg["From"] = MAILHOG_FROM_EMAIL
        msg["To"] = MAILHOG_TO_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(MAILHOG_SMTP_SERVER, MAILHOG_SMTP_PORT) as server:
                server.sendmail(msg["From"], msg["To"], msg.as_string())
            print(f"Email envoyé pour {site_url}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur d'envoi du mail : {e}")

    def remove_blocked_site(self):
        selected_item = self.blocked_sites_list.currentItem()
        if selected_item:
            site_url = selected_item.text()
            self.unblock_site_in_hosts(site_url)
            self.blocked_sites_list.takeItem(self.blocked_sites_list.row(selected_item))
        else:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un site à supprimer.")

    def load_blocked_sites(self):
        """Charge les sites bloqués depuis le fichier hosts."""
        if not os.path.exists(HOSTS_PATH):
            return
        
        with open(HOSTS_PATH, "r") as file:
            lines = file.readlines()
        
        for line in lines:
            if line.startswith("127.0.0.1") and len(line.split()) > 1:
                site = line.split()[1].strip()
                self.blocked_sites_list.addItem(site)
    
    def block_site_in_hosts(self, site_url):
        """Ajoute le site au fichier hosts pour le bloquer."""
        try:
            with open(HOSTS_PATH, "a") as file:
                file.write(f"\n127.0.0.1 {site_url}\n127.0.0.1 www.{site_url}\n")
            
            QMessageBox.information(self, "Succès", f"Le site {site_url} a été bloqué.")
        except PermissionError:
            QMessageBox.critical(self, "Erreur", "Permission refusée. Exécutez l'application en mode administrateur.")

    def unblock_site_in_hosts(self, site_url):
        """Supprime le site du fichier hosts pour le débloquer."""
        if not os.path.exists(HOSTS_PATH):
            return
        
        try:
            with open(HOSTS_PATH, "r") as file:
                lines = file.readlines()
            
            with open(HOSTS_PATH, "w") as file:
                for line in lines:
                    if site_url not in line:
                        file.write(line)
            
            QMessageBox.information(self, "Succès", f"Le site {site_url} a été débloqué.")
        except PermissionError:
            QMessageBox.critical(self, "Erreur", "Permission refusée. Exécutez l'application en mode administrateur.")
    
    def is_site_blocked(self, site_url):
        """Vérifie si un site est déjà bloqué."""
        if not os.path.exists(HOSTS_PATH):
            return False
        
        with open(HOSTS_PATH, "r") as file:
            lines = file.readlines()
        
        return any(site_url in line for line in lines)
