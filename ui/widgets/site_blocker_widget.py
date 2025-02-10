import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QMessageBox, QHBoxLayout, QTabWidget
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Importer les fonctions des modules utils
from utils.site_blocker import block_site, unblock_site, is_site_blocked
from utils.keyword_filter import load_blocked_keywords, KeywordFilter

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
        title = QLabel("Blocage de Sites et Mots-Clés")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #e74c3c; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Onglets pour les sites et les mots-clés
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 10px;
            }
            QTabBar::tab {
                padding: 10px;
                font-size: 16px;
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                margin-right: 5px;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        
        # Onglet pour les sites bloqués
        self.site_tab = QWidget()
        self.init_site_tab()
        self.tabs.addTab(self.site_tab, "Sites Bloqués")
        
        # Onglet pour les mots-clés bloqués
        self.keyword_tab = QWidget()
        self.init_keyword_tab()
        self.tabs.addTab(self.keyword_tab, "Mots-Clés Bloqués")
        
        layout.addWidget(self.tabs)
        
        # Charger les sites et mots-clés bloqués
        self.load_blocked_sites()
        self.load_blocked_keywords()

    def init_site_tab(self):
        """Initialise l'onglet pour les sites bloqués."""
        layout = QVBoxLayout(self.site_tab)
        
        # Champ de saisie pour les sites
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
        
        # Boutons "Ajouter" et "Supprimer" pour les sites
        button_layout = QHBoxLayout()
        
        self.add_site_button = QPushButton("Ajouter le site")
        self.add_site_button.setStyleSheet("""
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
        self.add_site_button.clicked.connect(self.add_blocked_site)
        button_layout.addWidget(self.add_site_button)
        
        self.remove_site_button = QPushButton("Supprimer le site")
        self.remove_site_button.setStyleSheet("""
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
        self.remove_site_button.clicked.connect(self.remove_blocked_site)
        button_layout.addWidget(self.remove_site_button)
        
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

    def init_keyword_tab(self):
        """Initialise l'onglet pour les mots-clés bloqués."""
        layout = QVBoxLayout(self.keyword_tab)
        
        # Champ de saisie pour les mots-clés
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("Entrez un mot-clé à bloquer")
        self.keyword_input.setStyleSheet(""" 
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
        layout.addWidget(self.keyword_input)
        
        # Boutons "Ajouter" et "Supprimer" pour les mots-clés
        button_layout = QHBoxLayout()
        
        self.add_keyword_button = QPushButton("Ajouter le mot-clé")
        self.add_keyword_button.setStyleSheet("""
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
        self.add_keyword_button.clicked.connect(self.add_blocked_keyword)
        button_layout.addWidget(self.add_keyword_button)
        
        self.remove_keyword_button = QPushButton("Supprimer le mot-clé")
        self.remove_keyword_button.setStyleSheet("""
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
        self.remove_keyword_button.clicked.connect(self.remove_blocked_keyword)
        button_layout.addWidget(self.remove_keyword_button)
        
        layout.addLayout(button_layout)
        
        # Liste des mots-clés bloqués
        self.blocked_keywords_list = QListWidget()
        self.blocked_keywords_list.setStyleSheet("""
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
        layout.addWidget(self.blocked_keywords_list)

    def add_blocked_site(self):
        site_url = self.site_input.text().strip()
        if site_url:
            if is_site_blocked(site_url):
                QMessageBox.warning(self, "Erreur", "Ce site est déjà bloqué.")
                return
            
            block_site(site_url)
            self.blocked_sites_list.addItem(site_url)
            self.site_input.clear()
            self.send_email_notification(site_url)
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer une URL valide.")
    
    def add_blocked_keyword(self):
        keyword = self.keyword_input.text().strip()
        if keyword:
            if keyword in load_blocked_keywords():
                QMessageBox.warning(self, "Erreur", "Ce mot-clé est déjà bloqué.")
                return
            
            with open("data/blocked_keywords.txt", "a") as file:
                file.write(f"{keyword}\n")
            
            self.blocked_keywords_list.addItem(keyword)
            self.keyword_input.clear()
            self.send_email_notification(f"Mot-clé : {keyword}")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un mot-clé valide.")

    def remove_blocked_site(self):
        selected_item = self.blocked_sites_list.currentItem()
        if selected_item:
            site_url = selected_item.text()
            unblock_site(site_url)
            self.blocked_sites_list.takeItem(self.blocked_sites_list.row(selected_item))
        else:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un site à supprimer.")

    def remove_blocked_keyword(self):
        selected_item = self.blocked_keywords_list.currentItem()
        if selected_item:
            keyword = selected_item.text()
            with open("data/blocked_keywords.txt", "r") as file:
                keywords = file.readlines()
            
            with open("data/blocked_keywords.txt", "w") as file:
                for kw in keywords:
                    if kw.strip() != keyword:
                        file.write(kw)
            
            self.blocked_keywords_list.takeItem(self.blocked_keywords_list.row(selected_item))
        else:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un mot-clé à supprimer.")

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
    
    def load_blocked_keywords(self):
        """Charge les mots-clés bloqués depuis un fichier."""
        if not os.path.exists("data/blocked_keywords.txt"):
            return
        
        with open("data/blocked_keywords.txt", "r") as file:
            keywords = file.readlines()
        
        for keyword in keywords:
            self.blocked_keywords_list.addItem(keyword.strip())

    def send_email_notification(self, content):
        """Envoie un e-mail de notification via MailHog."""
        subject = f"Tentative d'accès à un contenu bloqué : {content}"
        body = f"Une tentative d'accès au contenu bloqué {content} a été détectée."

        msg = MIMEMultipart()
        msg["From"] = MAILHOG_FROM_EMAIL
        msg["To"] = MAILHOG_TO_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP(MAILHOG_SMTP_SERVER, MAILHOG_SMTP_PORT) as server:
                server.sendmail(msg["From"], msg["To"], msg.as_string())
            print(f"Email envoyé pour {content}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur d'envoi du mail : {e}")