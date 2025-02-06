from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QGridLayout, QFrame
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

class HomePage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Titre de bienvenue
        title = QLabel("Tableau de Bord - Contrôle Parental")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Sous-titre
        subtitle = QLabel("Gérez facilement la sécurité en ligne de votre famille")
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setStyleSheet("color: #7f8c8d; margin-bottom: 30px;")
        layout.addWidget(subtitle)
        
        # Grille de fonctionnalités
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        
        # Fonctionnalité 1: Blocage de sites
        sites_card = self.create_feature_card(
            "Blocage de Sites",
            "Contrôlez l'accès aux sites web",
            "#e74c3c",
            lambda: self.main_window.sidebar.setCurrentRow(1)
        )
        grid_layout.addWidget(sites_card, 0, 0)
        
        # Fonctionnalité 2: Blocage d'applications
        apps_card = self.create_feature_card(
            "Blocage d'Applications",
            "Gérez l'utilisation des applications",
            "#9b59b6",
            lambda: self.main_window.sidebar.setCurrentRow(2)
        )
        grid_layout.addWidget(apps_card, 0, 1)
        
        # Fonctionnalité 3: Temps d'écran
        screen_card = self.create_feature_card(
            "Temps d'Écran",
            "Définissez des limites de temps",
            "#27ae60",
            lambda: self.main_window.sidebar.setCurrentRow(3)
        )
        grid_layout.addWidget(screen_card, 1, 0)
        
        # Fonctionnalité 4: Rapports
        reports_card = self.create_feature_card(
            "Rapports",
            "Suivez l'activité en ligne",
            "#2980b9",
            lambda: self.main_window.sidebar.setCurrentRow(4)
        )
        grid_layout.addWidget(reports_card, 1, 1)
        
        layout.addLayout(grid_layout)
        
        # Information de sécurité
        security_note = QLabel("Tous les contrôles sont actifs et fonctionnent correctement")
        security_note.setFont(QFont("Arial", 12))
        security_note.setStyleSheet("""
            color: #27ae60;
            padding: 15px;
            background-color: #f0f9f4;
            border-radius: 5px;
            margin-top: 20px;
        """)
        security_note.setAlignment(Qt.AlignCenter)
        layout.addWidget(security_note)
        
    def create_feature_card(self, title, description, color, on_click):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                border: 1px solid #e0e0e0;
            }}
            QFrame:hover {{
                border: 1px solid {color};
                background-color: #f8f9fa;
            }}
        """)
        
        card_layout = QVBoxLayout(card)
        
        # Titre de la carte
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet(f"color: {color};")
        card_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Arial", 12))
        desc_label.setStyleSheet("color: #7f8c8d;")
        desc_label.setWordWrap(True)
        card_layout.addWidget(desc_label)
        
        # Bouton d'accès
        access_button = QPushButton("Accéder")
        access_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 10px;
            }}
            QPushButton:hover {{
                background-color: {color}dd;
            }}
        """)
        access_button.clicked.connect(on_click)
        card_layout.addWidget(access_button)
        
        return card