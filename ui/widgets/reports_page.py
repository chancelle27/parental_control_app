from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
import pyqtgraph as pg
import numpy as np

class ReportPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_animations()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Titre du rapport
        title = QLabel("Rapport d'Activité")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Description du rapport
        description = QLabel(
            "Ce rapport fournit une analyse détaillée de l'activité sur l'appareil, incluant l'utilisation des applications et le temps d'écran."
        )
        description.setFont(QFont("Arial", 14))
        description.setStyleSheet("color: #7f8c8d;")
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignCenter)
        layout.addWidget(description)

        # Section des graphiques
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(20)
        
        # Graphique linéaire : Évolution du temps d'écran sur 7 jours
        self.line_chart = pg.PlotWidget(title="Evolution du Temps d'Écran (min)")
        self.line_chart.setBackground('#ecf0f1')
        days = np.arange(1, 8)  # Jours 1 à 7
        screen_time = np.array([120, 150, 100, 180, 200, 90, 130])
        pen = pg.mkPen(color='#3498db', width=2)
        self.line_chart.plot(days, screen_time, pen=pen, symbol='o', symbolSize=8, symbolBrush=('#3498db'))
        self.line_chart.setLabel('left', 'Temps (min)')
        self.line_chart.setLabel('bottom', 'Jour')
        charts_layout.addWidget(self.line_chart)
        
        # Graphique à barres : Utilisation par application
        self.bar_chart = pg.PlotWidget(title="Utilisation par Application")
        self.bar_chart.setBackground('#ecf0f1')
        apps = ['YouTube', 'Chrome', 'Games', 'Messenger']
        usage = np.array([50, 80, 30, 60])
        indices = np.arange(len(apps))
        bg = pg.BarGraphItem(x=indices, height=usage, width=0.6, brush='#e74c3c')
        self.bar_chart.addItem(bg)
        # Configuration de l'axe horizontal avec les noms des applications
        self.bar_chart.getAxis('bottom').setTicks([list(zip(indices, apps))])
        self.bar_chart.setLabel('left', 'Utilisations')
        self.bar_chart.setLabel('bottom', 'Applications')
        charts_layout.addWidget(self.bar_chart)
        
        layout.addLayout(charts_layout)

        # Tableau récapitulatif des données
        summary_title = QLabel("Détails de l'Activité")
        summary_title.setFont(QFont("Arial", 18, QFont.Bold))
        summary_title.setStyleSheet("color: #2c3e50;")
        summary_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(summary_title)

        self.summary_table = QTableWidget(4, 3)
        self.summary_table.setHorizontalHeaderLabels(["Application", "Temps Utilisé (min)", "Nombre de Lancements"])
        data = [
            ["YouTube", "120", "15"],
            ["Chrome", "80", "10"],
            ["Games", "60", "5"],
            ["Messenger", "40", "20"]
        ]
        for row, rowData in enumerate(data):
            for col, value in enumerate(rowData):
                item = QTableWidgetItem(value)
                self.summary_table.setItem(row, col, item)
        self.summary_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.summary_table)

        # Bouton pour exporter le rapport
        export_button = QPushButton("Exporter le Rapport")
        export_button.setFont(QFont("Arial", 14))
        export_button.setStyleSheet("""
            QPushButton {
                background-color: #1abc9c;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #16a085;
            }
        """)
        export_button.clicked.connect(self.export_report)
        layout.addWidget(export_button, alignment=Qt.AlignCenter)

    def setup_animations(self):
        # Vous pouvez ajouter ici des animations pour les graphiques ou autres éléments si besoin.
        # Par exemple, une animation de fondu pour le tableau :
        animation = QPropertyAnimation(self.summary_table, b"windowOpacity")
        animation.setDuration(1000)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()

    def export_report(self):
        # Fonction simulée pour l'export du rapport (CSV, PDF, etc.)
        print("Export du rapport vers CSV ou PDF (fonctionnalité à implémenter)")
        
