from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QStackedWidget, QHBoxLayout, QListWidget, QListWidgetItem
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
from ui.widgets.site_blocker_widget import BlockSitesPage
from ui.widgets.app_blocker_widget import BlockAppsPage
from ui.widgets.screen_time_widget import ScreenTimeWidget
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Contrôle Parental")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: #f5f6fa;")  # Fond clair et moderne
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QHBoxLayout(central_widget)
        layout.setSpacing(0)  # Supprime l'espace entre la sidebar et le contenu
        layout.setContentsMargins(0, 0, 0, 0)  # Supprime les marges
        
        # Sidebar minimaliste
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(200)  # Largeur fixe pour la sidebar
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: #2c3e50;  # Fond sombre pour la sidebar
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
                background-color: #34495e;  # Couleur de fond pour l'élément sélectionné
                border-left: 4px solid #3498db;  # Bordure gauche bleue pour l'élément sélectionné
                color: white;
                font-weight: bold;
            }
            QListWidget::item:hover {
                background-color: #34495e;  # Couleur de fond au survol
            }
        """)
        
        # Pages disponibles dans la sidebar
        pages = [
            ("Accueil", "home"),
            ("Blocage de Sites", "block_sites"),
            ("Blocage d'Applications", "block_apps"),
            ("Temps d'Écran", "screen_time"),
            ("Rapports", "reports")
        ]
        
        for name, key in pages:
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, key)
            self.sidebar.addItem(item)
        
        self.sidebar.currentItemChanged.connect(self.change_page)
        
        # Zone principale avec StackedWidget
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: white; border-left: 1px solid #dfe6e9;")  # Fond blanc avec une bordure
        
        self.pages = {
            "home": self.create_home_page(),
            "block_sites": BlockSitesPage(),  # Couleur rouge
            "block_apps": BlockAppsPage(),  # Couleur violette
            "screen_time": ScreenTimeWidget(),  # Couleur verte
            "reports": self.create_page("Rapports", "#2980b9")  # Couleur bleue
        }
        
        for page in self.pages.values():
            self.stack.addWidget(page)
        
        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack, 1)  # Le contenu prend tout l'espace restant
        
        # Sélectionner la première page par défaut
        self.sidebar.setCurrentRow(0)
        self.stack.setCurrentWidget(self.pages["home"])
    
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
        
        # Exemple de contenu supplémentaire
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())