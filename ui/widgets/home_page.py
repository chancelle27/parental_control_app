from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QProgressBar, QFrame
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
import pyqtgraph as pg
import numpy as np

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_animations()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Titre et description
        title = QLabel("Bienvenue dans le Contrôle Parental")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        description = QLabel(
            "Cette application vous permet de gérer et de surveiller les activités de vos enfants sur leur appareil. "
            "Utilisez les fonctionnalités ci-dessous pour commencer."
        )
        description.setFont(QFont("Arial", 14))
        description.setStyleSheet("color: #7f8c8d; margin-bottom: 30px;")
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignCenter)
        layout.addWidget(description)

        # Statistiques (cartes)
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        self.add_stat_card(stats_layout, "Applications bloquées", "12", "#e74c3c")
        self.add_stat_card(stats_layout, "Temps d'écran total", "3h 45m", "#3498db")
        self.add_stat_card(stats_layout, "Sites bloqués", "8", "#2ecc71")
        layout.addLayout(stats_layout)

        # Barre de progression pour le temps d'écran
        self.screen_time_progress = QProgressBar()
        self.screen_time_progress.setRange(0, 100)
        self.screen_time_progress.setValue(45)  # 45% du temps d'écran utilisé
        self.screen_time_progress.setFormat("Temps d'écran utilisé: %p%")
        self.screen_time_progress.setStyleSheet("""
            QProgressBar {
                background-color: #ecf0f1;
                border-radius: 10px;
                text-align: center;
                font-size: 14px;
                color: #2c3e50;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 10px;
            }
        """)
        layout.addWidget(self.screen_time_progress)



        # Section des graphiques
        graph_section = QHBoxLayout()
        graph_section.setSpacing(20)
        
        # Graphique linéaire : évolution du temps d'écran sur la semaine
        self.line_chart = pg.PlotWidget(title="Évolution du Temps d'Écran (min)")
        self.line_chart.setBackground('#ecf0f1')
        days = np.arange(1, 8)  # Jours 1 à 7
        screen_time = np.array([120, 150, 100, 180, 200, 90, 130])
        pen = pg.mkPen(color='#3498db', width=2)
        self.line_chart.plot(days, screen_time, pen=pen, symbol='o', symbolSize=8, symbolBrush=('#3498db'))
        self.line_chart.setLabel('left', 'Temps (min)')
        self.line_chart.setLabel('bottom', 'Jour')
        graph_section.addWidget(self.line_chart)
        
        # Graphique à barres : utilisation des applications
        self.bar_chart = pg.PlotWidget(title="Utilisation des Applications")
        self.bar_chart.setBackground('#ecf0f1')
        apps = ['YouTube', 'Chrome', 'Games', 'Messenger']
        usage = np.array([50, 80, 30, 60])
        indices = np.arange(len(apps))
        bg = pg.BarGraphItem(x=indices, height=usage, width=0.6, brush='#e74c3c')
        self.bar_chart.addItem(bg)
        # Personnalisation de l'axe bas avec les noms des applications
        self.bar_chart.getAxis('bottom').setTicks([list(zip(indices, apps))])
        self.bar_chart.setLabel('left', 'Utilisations')
        self.bar_chart.setLabel('bottom', 'Applications')
        graph_section.addWidget(self.bar_chart)
        
        layout.addLayout(graph_section)

    def add_stat_card(self, layout, title, value, color):
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

        # Animation de fondu pour la carte
        self.animate_card(card)
        layout.addWidget(card)

    def add_shortcut_button(self, layout, text, color, callback):
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
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darkened_rgb = tuple(max(0, min(255, int(c * 0.85))) for c in rgb)
        return f'#{darkened_rgb[0]:02x}{darkened_rgb[1]:02x}{darkened_rgb[2]:02x}'

    def animate_card(self, card):
        animation = QPropertyAnimation(card, b"windowOpacity")
        animation.setDuration(1000)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()

    def setup_animations(self):
        self.progress_animation = QPropertyAnimation(self.screen_time_progress, b"value")
        self.progress_animation.setDuration(2000)
        self.progress_animation.setStartValue(0)
        self.progress_animation.setEndValue(45)
        self.progress_animation.setEasingCurve(QEasingCurve.OutQuad)
        self.progress_animation.start()

    def open_block_sites(self):
        print("Ouvrir la page de blocage de sites")

    def open_block_apps(self):
        print("Ouvrir la page de blocage d'applications")

    def open_screen_time(self):
        print("Ouvrir la page de gestion du temps d'écran")
