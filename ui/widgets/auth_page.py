import sqlite3
import hashlib
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QMessageBox, QGraphicsDropShadowEffect, 
                             QGraphicsBlurEffect)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint
from PyQt5.QtGui import QColor, QLinearGradient, QPalette, QPainter, QBrush

class AnimatedLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            AnimatedLineEdit {
                background-color: rgba(240, 245, 255, 0.7);
                border: 2px solid rgba(100, 149, 237, 0.3);
                border-radius: 12px;
                color: #1e3a8a;
                padding: 10px 15px;
                font-size: 16px;
                transition: all 0.3s ease;
            }
            AnimatedLineEdit:focus {
                border-color: #3b82f6;
                background-color: white;
                box-shadow: 0 0 15px rgba(59, 130, 246, 0.3);
            }
        """)
        
        # Shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(59, 130, 246, 100))
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)

class BlueGlassBackground(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            BlueGlassBackground {
                background: qlineargradient(
                    spread:pad, 
                    x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(100, 149, 237, 0.1), 
                    stop:1 rgba(65, 105, 225, 0.1)
                );
            }
        """)

class AuthPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.db_path = 'user_credentials.db'
        self.init_database()
        self.initUI()
    
    def init_database(self):
        """
        Initialize the SQLite database and create the users table if it doesn't exist.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create users table with username and password_hash columns
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password_hash TEXT NOT NULL
                )
            ''')
            
            conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur de base de données", 
                                 f"Impossible de créer la base de données : {str(e)}")
        finally:
            if conn:
                conn.close()
    
        
    def initUI(self):
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Fond bleu glass
        background = BlueGlassBackground()
        main_layout.addWidget(background)
        
        # Layout principal du contenu
        content_layout = QVBoxLayout(background)
        content_layout.setAlignment(Qt.AlignCenter)
        
        # Carte de connexion ultra moderne
        auth_card = QWidget()
        auth_card.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 25px;
                border: 1px solid rgba(100, 149, 237, 0.2);
                box-shadow: 0 20px 40px rgba(65, 105, 225, 0.15);
                padding: 40px;
                max-width: 500px;
            }
        """)
        
        # Effet de miroir subtil
        mirror_effect = QWidget(auth_card)
        mirror_effect.setStyleSheet("""
            background: qlineargradient(
                spread:pad, 
                x1:0, y1:0, x2:1, y2:1, 
                stop:0 rgba(100, 149, 237, 0.05), 
                stop:1 rgba(65, 105, 225, 0.05)
            );
            border-radius: 25px;
            opacity: 0.5;
        """)
        mirror_effect.setGeometry(10, 10, auth_card.width() - 20, auth_card.height() - 20)
        
        card_layout = QVBoxLayout(auth_card)
        card_layout.setSpacing(25)
        
        # Titre avec dégradé bleu moderne
        title = QLabel("Connexion")
        title.setStyleSheet("""
            QLabel {
                color: transparent;
                background-image: linear-gradient(to right, #1e3a8a, #3b82f6);
                -webkit-background-clip: text;
                background-clip: text;
                font-size: 36px;
                font-weight: bold;
                text-align: center;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        
        # Sous-titre
        subtitle = QLabel("Accédez à votre espace personnel")
        subtitle.setStyleSheet("""
            QLabel {
                color: #4a5568;
                font-size: 16px;
                text-align: center;
            }
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        
        # Champs de saisie
        self.username_input = AnimatedLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        
        self.password_input = AnimatedLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        # Bouton de connexion hyper moderne
        login_button = QPushButton("Se connecter")
        login_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    spread:pad, 
                    x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #1e3a8a, 
                    stop:1 #3b82f6
                );
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                transition: all 0.3s ease;
                box-shadow: 0 10px 20px rgba(30, 58, 138, 0.2);
            }
            QPushButton:hover {
                background: qlineargradient(
                    spread:pad, 
                    x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #2563eb, 
                    stop:1 #3b82f6
                );
                transform: scale(1.05);
                box-shadow: 0 15px 25px rgba(30, 58, 138, 0.3);
            }
            QPushButton:pressed {
                transform: scale(0.95);
                box-shadow: 0 5px 10px rgba(30, 58, 138, 0.2);
            }
        """)
        login_button.clicked.connect(self.handle_authentication)
        
        # Ajouter les widgets
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(self.password_input)
        card_layout.addWidget(login_button)
        
        content_layout.addWidget(auth_card)
        
        # Animation d'entrée
        self.setup_entry_animation(auth_card)
    
    def setup_entry_animation(self, widget):
        # Animation de translation et de fondu
        widget.setWindowOpacity(0)
        
        # Animation de translation verticale
        self.pos_animation = QPropertyAnimation(widget, b"pos")
        self.pos_animation.setStartValue(QPoint(widget.x(), widget.y() + 50))
        self.pos_animation.setEndValue(QPoint(widget.x(), widget.y()))
        self.pos_animation.setEasingCurve(QEasingCurve.OutBack)
        self.pos_animation.setDuration(800)
        
        # Animation d'opacité
        self.opacity_animation = QPropertyAnimation(widget, b"windowOpacity")
        self.opacity_animation.setStartValue(0)
        self.opacity_animation.setEndValue(1)
        self.opacity_animation.setDuration(800)
        
        # Groupe d'animations
        self.pos_animation.start()
        self.opacity_animation.start()
    
    # Les autres méthodes restent identiques à l'implémentation précédente
    # (hash_password, save_credentials, is_first_login, verify_credentials, handle_authentication)
    # Voir l'implémentation précédente
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def save_credentials(self, username, password_hash):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO users (username, password_hash) 
                VALUES (?, ?)
            ''', (username, password_hash))
            
            conn.commit()
            return True
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur de base de données", 
                                 f"Impossible de sauvegarder les identifiants : {str(e)}")
            return False
        finally:
            if conn:
                conn.close()
    
    def is_first_login(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM users')
            count = cursor.fetchone()[0]
            
            return count == 0
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur de base de données", 
                                 f"Impossible de vérifier les utilisateurs : {str(e)}")
            return True
        finally:
            if conn:
                conn.close()
    
    def verify_credentials(self, username, password_hash):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM users 
                WHERE username = ? AND password_hash = ?
            ''', (username, password_hash))
            
            return cursor.fetchone() is not None
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur de base de données", 
                                 f"Impossible de vérifier les identifiants : {str(e)}")
            return False
        finally:
            if conn:
                conn.close()
    
    def handle_authentication(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs")
            return
        
        password_hash = self.hash_password(password)
        
        if self.is_first_login():
            confirmation = QMessageBox.question(
                self,
                "Première connexion",
                "Voulez-vous enregistrer ces identifiants pour les futures connexions ?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if confirmation == QMessageBox.Yes:
                if self.save_credentials(username, password_hash):
                    QMessageBox.information(self, "Succès", "Identifiants enregistrés avec succès!")
                    self.main_window.show_dashboard()
                
        else:
            if self.verify_credentials(username, password_hash):
                self.username_input.clear()
                self.password_input.clear()
                self.main_window.show_dashboard()
            else:
                QMessageBox.warning(self, "Erreur", "Identifiants incorrects")