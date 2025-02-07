from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QStackedWidget, QHBoxLayout, QListWidget, QListWidgetItem,
    QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
from ui.widgets.auth_page import AuthPage
from ui.widgets.home_page import HomePage
from ui.widgets.app_blocker_widget import BlockAppsPage
from ui.widgets.screen_time_widget import ScreenTimePage
from ui.widgets.site_blocker_widget import BlockSitesPage
from ui.widgets.home_page import HomePage
# Page d'authentification
class AuthPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(30, 30, 30, 30)

        # Username input
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        self.username_input.setStyleSheet("""
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
        layout.addWidget(self.username_input)

        # Password input
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Mot de passe")
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
        layout.addWidget(self.password_input)

        # Login button
        self.login_button = QPushButton("Se connecter", self)
        self.login_button.setStyleSheet("""
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
        self.login_button.setFixedHeight(45)
        self.login_button.clicked.connect(self.authenticate)
        layout.addWidget(self.login_button)


    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Validation simple (à remplacer par une logique plus sécurisée)
        if username == "admin" and password == "password":  # Exemple simple
            self.parent.show_dashboard()  # Basculer vers le tableau de bord
        else:
            QMessageBox.warning(self, "Erreur", "Nom d'utilisateur ou mot de passe incorrect")

# Fenêtre principale
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Contrôle Parental")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: #f5f6fa;")
        
        # Widget central et layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.layout = QHBoxLayout(central_widget)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # StackedWidget pour gérer les pages
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)
        
        # Page d'authentification
        self.auth_page = AuthPage(self)
        self.stack.addWidget(self.auth_page)
        
        # Initialiser les pages du tableau de bord
        self.init_dashboard_pages()
    
    def init_dashboard_pages(self):
        # Créer les pages du tableau de bord
        self.pages = {
            "home": HomePage(),
            "block_sites": BlockSitesPage(),
            "block_apps": BlockAppsPage(),
            "screen_time": ScreenTimePage(),
            "reports": self.create_page("Rapports", "#2980b9")
        }
        
        # Ajouter les pages au stacked widget
        for page in self.pages.values():
            self.stack.addWidget(page)
    
    def show_dashboard(self):
        # Basculer vers le tableau de bord
        self.stack.setCurrentWidget(self.pages["home"])
        
        # Ajouter la sidebar
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: #2c3e50;
                color: white;
                font-size: 16px;
                border: none;
                padding: 10px 0;
            }
            QListWidget::item {
                padding: 15px 20px;
                border-radius: 0;
                border-left: 4px solid transparent;
            }
            QListWidget::item:selected {
                background-color: #34495e;
                border-left: 4px solid #3498db;
                color: white;
                font-weight: bold;
            }
            QListWidget::item:hover {
                background-color: #34495e;
            }
        """)
        
        # Pages disponibles dans la sidebar
        pages = [
            ("Accueil", "home"),
            ("Blocage de Sites", "block_sites"),
            ("Blocage d'Applications", "block_apps"),
            ("Temps d'Écran", "screen_time"),
            ("Rapports", "reports"),
            ("Paramètres", "settings"),
            
        ]
        
        for name, key in pages:
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, key)
            self.sidebar.addItem(item)
        
        self.sidebar.currentItemChanged.connect(self.change_page)
        
        # Ajouter la sidebar au layout
        self.layout.insertWidget(0, self.sidebar)
        self.sidebar.setCurrentRow(0)
    
    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("Bienvenue dans le Contrôle Parental")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(title)
        
        description = QLabel("Utilisez la barre latérale pour naviguer entre les différentes fonctionnalités.")
        description.setFont(QFont("Arial", 14))
        description.setAlignment(Qt.AlignCenter)
        description.setStyleSheet("color: #7f8c8d;")
        layout.addWidget(description)
        
        return page
    
    def create_page(self, title_text, color):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel(title_text)
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {color}; margin-bottom: 20px;")
        layout.addWidget(title)
        
        content = QLabel(f"Page dédiée à la fonctionnalité : {title_text}")
        content.setFont(QFont("Arial", 14))
        content.setAlignment(Qt.AlignCenter)
        content.setStyleSheet("color: #7f8c8d;")
        layout.addWidget(content)
        
        return page
    
    def change_page(self, current_item):
        if current_item:
            page_key = current_item.data(Qt.UserRole)
            self.stack.setCurrentWidget(self.pages[page_key])

# Point d'entrée de l'application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())