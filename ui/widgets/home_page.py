from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Titre de la page d'accueil
        title = QLabel("Bienvenue dans le Contrôle Parental")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        # Description de l'application
        description = QLabel(
            "Cette application vous permet de gérer et de surveiller les activités de vos enfants sur leur appareil. "
            "Utilisez les fonctionnalités ci-dessous pour commencer."
        )
        description.setFont(QFont("Arial", 14))
        description.setStyleSheet("color: #7f8c8d; margin-bottom: 30px;")
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignCenter)
        layout.addWidget(description)

        # Statistiques ou informations rapides
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)

        # Exemple de statistiques (à adapter selon vos besoins)
        self.add_stat_card(stats_layout, "Applications bloquées", "0", "#e74c3c")
        self.add_stat_card(stats_layout, "Temps d'écran total", "0h 0m", "#3498db")
        self.add_stat_card(stats_layout, "Sites bloqués", "0", "#2ecc71")

        layout.addLayout(stats_layout)

        # Boutons de raccourci vers les fonctionnalités principales
        shortcuts_layout = QHBoxLayout()
        shortcuts_layout.setSpacing(15)

        self.add_shortcut_button(shortcuts_layout, "Blocage de Sites", "#9b59b6", self.open_block_sites)
        self.add_shortcut_button(shortcuts_layout, "Blocage d'Apps", "#e67e22", self.open_block_apps)
        self.add_shortcut_button(shortcuts_layout, "Temps d'Écran", "#1abc9c", self.open_screen_time)

        layout.addLayout(shortcuts_layout)

    def add_stat_card(self, layout, title, value, color):
        """Ajoute une carte de statistique."""
        card = QWidget()
        card.setStyleSheet(f"""
            background-color: {color};
            border-radius: 10px;
            padding: 20px;
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignCenter)

        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 18, QFont.Bold))
        value_label.setStyleSheet("color: white;")
        card_layout.addWidget(value_label)

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12))
        title_label.setStyleSheet("color: white;")
        card_layout.addWidget(title_label)

        layout.addWidget(card)

    def add_shortcut_button(self, layout, text, color, callback):
        """Ajoute un bouton de raccourci."""
        button = QPushButton(text)
        button.setFont(QFont("Arial", 14))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                padding: 15px;
                border-radius: 10px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
        """)
        button.clicked.connect(callback)
        layout.addWidget(button)

    def darken_color(self, color):
        """Assombrit légèrement une couleur hexadécimale."""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darkened_rgb = tuple(max(0, min(255, int(c * 0.85))) for c in rgb)
        return f'#{darkened_rgb[0]:02x}{darkened_rgb[1]:02x}{darkened_rgb[2]:02x}'

    def open_block_sites(self):
        """Ouvre la page de blocage de sites."""
        print("Ouvrir la page de blocage de sites")

    def open_block_apps(self):
        """Ouvre la page de blocage d'applications."""
        print("Ouvrir la page de blocage d'applications")

    def open_screen_time(self):
        """Ouvre la page de gestion du temps d'écran."""
        print("Ouvrir la page de gestion du temps d'écran")