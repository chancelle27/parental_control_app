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
from ui.widgets.settings_page import SettingsPage
from ui.widgets.reports_page import ReportPage

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
        self.auth_page = AuthPage(self)  # Utilisation de la classe AuthPage importée
        self.stack.addWidget(self.auth_page)

        # Initialiser les pages du tableau de bord
        self.init_dashboard_pages()

        # Suivi de l'état de connexion
        self.is_logged_in = False
        
        

    def init_dashboard_pages(self):
        # Créer les pages du tableau de bord
        self.pages = {
            "home": HomePage(),
            "block_sites": BlockSitesPage(),
            "block_apps": BlockAppsPage(),
            "screen_time": ScreenTimePage(),
            "reports": ReportPage(),
            "settings": SettingsPage()
        }

        # Ajouter les pages au stacked widget
        for page in self.pages.values():
            self.stack.addWidget(page)

    def show_dashboard(self):
        self.is_logged_in = True
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