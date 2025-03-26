import sqlite3
import hashlib
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, 
    QCheckBox, QFrame, QMessageBox, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.db_path = 'user_credentials.db'
        self.admin_username = "admin"  # Nom d'utilisateur fixe
        self.init_db()
        self.initUI()

    def init_db(self):
        """Initialise la base de données avec l'utilisateur admin si nécessaire"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password_hash TEXT NOT NULL
                )
            """)
            # Créer l'admin avec mot de passe par défaut 'admin' si non existant
            cursor.execute("""
                INSERT OR IGNORE INTO users (username, password_hash)
                VALUES (?, ?)
            """, (self.admin_username, hashlib.sha256("admin".encode()).hexdigest()))
            conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur DB", f"Erreur base de données : {str(e)}")
        finally:
            if conn:
                conn.close()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Titre
        title = QLabel("Paramètres Administrateur")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Carte Mot de passe
        password_card = self.create_card("Modifier le mot de passe admin", self.create_password_form())
        layout.addWidget(password_card)

        # Carte Notifications
        notification_card = self.create_card("Paramètres de notification", self.create_notification_form())
        layout.addWidget(notification_card)

    def create_card(self, title, content):
        """Crée une carte stylisée"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        layout = QVBoxLayout(card)
        
        # Titre de la carte
        lbl_title = QLabel(title)
        lbl_title.setFont(QFont("Arial", 16, QFont.Bold))
        lbl_title.setStyleSheet("color: #34495e; margin-bottom: 15px;")
        layout.addWidget(lbl_title)
        
        # Contenu
        layout.addWidget(content)
        
        # Ombre
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 60))
        card.setGraphicsEffect(shadow)
        
        return card

    def create_password_form(self):
        """Formulaire de changement de mot de passe"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(15)

        self.txt_new_pass = QLineEdit()
        self.txt_new_pass.setPlaceholderText("Nouveau mot de passe")
        self.txt_new_pass.setEchoMode(QLineEdit.Password)
        self.style_input(self.txt_new_pass)
        
        self.txt_confirm_pass = QLineEdit()
        self.txt_confirm_pass.setPlaceholderText("Confirmer le mot de passe")
        self.txt_confirm_pass.setEchoMode(QLineEdit.Password)
        self.style_input(self.txt_confirm_pass)

        btn_save = QPushButton("Enregistrer le mot de passe")
        btn_save.clicked.connect(self.update_admin_password)
        self.style_button(btn_save, "#3498db", "#2980b9")

        layout.addWidget(self.txt_new_pass)
        layout.addWidget(self.txt_confirm_pass)
        layout.addWidget(btn_save)
        
        return container

    def create_notification_form(self):
        """Formulaire de notifications"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(15)

        self.txt_email = QLineEdit()
        self.txt_email.setPlaceholderText("Email de notification")
        self.style_input(self.txt_email)
        
        self.chk_notifications = QCheckBox("Activer les notifications par email")
        self.chk_notifications.setStyleSheet("font-size: 14px; color: #2c3e50;")

        btn_save = QPushButton("Enregistrer les préférences")
        btn_save.clicked.connect(self.save_notification_settings)
        self.style_button(btn_save, "#1abc9c", "#16a085")

        layout.addWidget(self.txt_email)
        layout.addWidget(self.chk_notifications)
        layout.addWidget(btn_save)
        
        return container

    def style_input(self, widget):
        """Style commun pour les champs de saisie"""
        widget.setStyleSheet("""
            QLineEdit {
                background: #f8f9fa;
                border: 1px solid #ced4da;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
        """)

    def style_button(self, button, normal_color, hover_color):
        """Style commun pour les boutons"""
        button.setStyleSheet(f"""
            QPushButton {{
                background: {normal_color};
                color: white;
                border: none;
                padding: 12px;
                border-radius: 8px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background: {hover_color};
            }}
        """)

    def update_admin_password(self):
        """Met à jour le mot de passe admin"""
        new_pass = self.txt_new_pass.text().strip()
        confirm_pass = self.txt_confirm_pass.text().strip()

        if not new_pass or not confirm_pass:
            QMessageBox.warning(self, "Champs vides", "Veuillez remplir tous les champs")
            return
            
        if new_pass != confirm_pass:
            QMessageBox.warning(self, "Erreur", "Les mots de passe ne correspondent pas")
            return

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            new_hash = hashlib.sha256(new_pass.encode()).hexdigest()
            
            cursor.execute("""
                UPDATE users 
                SET password_hash = ?
                WHERE username = ?
            """, (new_hash, self.admin_username))
            
            conn.commit()
            QMessageBox.information(self, "Succès", "Mot de passe mis à jour avec succès")
            
            # Vider les champs
            self.txt_new_pass.clear()
            self.txt_confirm_pass.clear()
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur DB", f"Erreur de mise à jour : {str(e)}")
        finally:
            if conn:
                conn.close()

    def save_notification_settings(self):
        """Enregistre les paramètres de notification"""
        email = self.txt_email.text().strip()
        
        if not email:
            QMessageBox.warning(self, "Email manquant", "Veuillez saisir un email")
            return

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Créer la table si nécessaire
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notifications (
                    username TEXT PRIMARY KEY,
                    email TEXT,
                    enabled INTEGER DEFAULT 0
                )
            """)
            
            # Mettre à jour les paramètres
            cursor.execute("""
                INSERT OR REPLACE INTO notifications 
                (username, email, enabled)
                VALUES (?, ?, ?)
            """, (self.admin_username, email, int(self.chk_notifications.isChecked())))
            
            conn.commit()
            QMessageBox.information(self, "Succès", "Paramètres enregistrés")
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur DB", f"Erreur d'enregistrement : {str(e)}")
        finally:
            if conn:
                conn.close()
