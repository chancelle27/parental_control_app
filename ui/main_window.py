from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QApplication, QFrame, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        self.setWindowTitle("Parental Control App")
        self.setGeometry(100, 100, 500, 350)

        # Définir une couleur de fond
        self.setStyleSheet("background-color: #f0f0f0;")

        # Widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout pour organiser les boutons
        layout = QVBoxLayout(central_widget)

        # Titre avec un joli style
        self.title_label = QLabel("Contrôle Parental", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; margin-bottom: 20px;")
        layout.addWidget(self.title_label)

        # Création d'un cadre avec une bordure pour chaque section
        self.create_button(layout, "Bloquer Sites", "site_icon.png", self.block_sites)
        self.create_button(layout, "Bloquer Applications", "app_icon.png", self.block_apps)
        self.create_button(layout, "Gérer Temps d'écran", "time_icon.png", self.manage_screen_time)
        self.create_button(layout, "Afficher Rapports", "report_icon.png", self.show_reports)

    def create_button(self, layout, text, icon_path, callback):
        # Créer un cadre avec un bouton à l'intérieur
        frame = QFrame(self)
        frame.setStyleSheet("background-color: white; border-radius: 10px; margin: 10px; padding: 10px;")
        button = QPushButton(text, frame)
        button.setIcon(QIcon(icon_path))  # Ajout d'une icône
        button.setIconSize(button.sizeHint())  # Ajustement de la taille de l'icône
        button.clicked.connect(callback)

        # Style du bouton
        button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # Ajouter le bouton dans le cadre, puis le cadre dans le layout
        frame_layout = QVBoxLayout(frame)
        frame_layout.addWidget(button)
        layout.addWidget(frame)

    def block_sites(self):
        print("Bloquage des sites activé...")

    def block_apps(self):
        print("Blocage des applications activé...")

    def manage_screen_time(self):
        print("Gestion du temps d'écran activée...")

    def show_reports(self):
        print("Affichage des rapports activé...")
