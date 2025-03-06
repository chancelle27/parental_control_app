import sys
import time
import json
import os
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox,
    QMessageBox, QHBoxLayout, QLineEdit, QFormLayout,
    QTableWidget, QTableWidgetItem, QTabWidget, QHeaderView
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
import winapps
import psutil

class ScreenTimePage(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.current_app = None
        self.start_time = None
        self.elapsed_time = 0
        self.time_limit = 0  # Temps limite en secondes
        self.usage_data = {}  # Stockage des données d'utilisation
        self.tracked_processes = {}  # Processus actuellement suivis
        
        # Créer le dossier de données s'il n'existe pas
        os.makedirs("data", exist_ok=True)
        
        # Charger les données d'utilisation précédentes
        self.load_usage_data()
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Titre du widget
        title = QLabel("Gestion du Temps d'Écran")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)

        # Créer des onglets
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 10px;
            }
            QTabBar::tab {
                background: #ecf0f1;
                border: 1px solid #bdc3c7;
                padding: 10px 15px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #3498db;
                color: white;
            }
        """)

        # Onglet pour le suivi manuel
        manual_tracking_tab = QWidget()
        self.setup_manual_tracking_tab(manual_tracking_tab)
        tabs.addTab(manual_tracking_tab, "Suivi Manuel")

        # Onglet pour le suivi automatique
        auto_tracking_tab = QWidget()
        self.setup_auto_tracking_tab(auto_tracking_tab)
        tabs.addTab(auto_tracking_tab, "Suivi Automatique")

        # Onglet pour les statistiques
        stats_tab = QWidget()
        self.setup_stats_tab(stats_tab)
        tabs.addTab(stats_tab, "Statistiques")

        layout.addWidget(tabs)

    def setup_manual_tracking_tab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)

        # Sélecteur d'application
        self.app_selector = QComboBox()
        self.app_selector.setFont(QFont("Arial", 12))
        self.app_selector.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #bdc3c7;")
        self.app_selector.currentIndexChanged.connect(self.select_app)
        layout.addWidget(QLabel("Sélectionnez une application :"))
        layout.addWidget(self.app_selector)

        # Charger les applications installées
        self.load_installed_apps()

        # Affichage du temps passé
        self.time_label = QLabel("Temps passé : 0 secondes")
        self.time_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.time_label)

        # Champ pour définir la limite de temps
        self.time_limit_input = QLineEdit()
        self.time_limit_input.setPlaceholderText("Entrez la limite de temps en minutes")
        self.time_limit_input.setFont(QFont("Arial", 12))
        self.time_limit_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #bdc3c7;")
        layout.addWidget(QLabel("Définir une limite de temps (en minutes) :"))
        layout.addWidget(self.time_limit_input)

        # Bouton pour appliquer la limite
        self.set_limit_button = QPushButton("Appliquer la limite")
        self.set_limit_button.setStyleSheet(self.get_button_style("#27ae60"))
        self.set_limit_button.clicked.connect(self.set_time_limit)
        layout.addWidget(self.set_limit_button)

        # Bouton pour démarrer/arrêter le suivi
        self.toggle_tracking_button = QPushButton("Démarrer le suivi")
        self.toggle_tracking_button.setStyleSheet(self.get_button_style("#3498db"))
        self.toggle_tracking_button.clicked.connect(self.toggle_tracking)
        layout.addWidget(self.toggle_tracking_button)

    def setup_auto_tracking_tab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)

        # Explication
        info_label = QLabel("Le suivi automatique surveille toutes les applications en cours d'exécution.")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        # Affichage des applications en cours d'exécution
        layout.addWidget(QLabel("Applications actuellement suivies :"))
        
        self.active_apps_table = QTableWidget(0, 3)
        self.active_apps_table.setHorizontalHeaderLabels(["Application", "Temps aujourd'hui", "Limite"])
        self.active_apps_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.active_apps_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 0px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #ecf0f1;
                padding: 5px;
                border: 1px solid #bdc3c7;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.active_apps_table)

        # Boutons pour démarrer/arrêter le suivi automatique
        self.auto_track_button = QPushButton("Démarrer le suivi automatique")
        self.auto_track_button.setStyleSheet(self.get_button_style("#3498db"))
        self.auto_track_button.clicked.connect(self.toggle_auto_tracking)
        layout.addWidget(self.auto_track_button)

        # Timer pour le suivi automatique
        self.auto_timer = QTimer()
        self.auto_timer.timeout.connect(self.update_running_apps)
        self.auto_tracking_active = False

    def setup_stats_tab(self, tab):
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)

        # Table des statistiques
        self.stats_table = QTableWidget(0, 3)
        self.stats_table.setHorizontalHeaderLabels(["Application", "Temps total", "Dernière utilisation"])
        self.stats_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.stats_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 0px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #ecf0f1;
                padding: 5px;
                border: 1px solid #bdc3c7;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.stats_table)

        # Bouton pour actualiser les statistiques
        refresh_button = QPushButton("Actualiser les statistiques")
        refresh_button.setStyleSheet(self.get_button_style("#9b59b6"))
        refresh_button.clicked.connect(self.update_stats)
        layout.addWidget(refresh_button)

        # Bouton pour réinitialiser les statistiques
        reset_button = QPushButton("Réinitialiser les statistiques")
        reset_button.setStyleSheet(self.get_button_style("#e74c3c"))
        reset_button.clicked.connect(self.reset_stats)
        layout.addWidget(reset_button)

        # Initialiser les statistiques
        self.update_stats()

    def load_installed_apps(self):
        """Charge les applications installées dans le sélecteur."""
        self.app_selector.clear()
        self.app_selector.addItem("-- Sélectionnez une application --")
        
        try:
            # Ajouter les applications installées
            for app in winapps.search_installed():
                self.app_selector.addItem(app.name)
            
            # Ajouter également les processus en cours d'exécution
            for proc in psutil.process_iter(['name']):
                try:
                    proc_name = proc.info['name']
                    if proc_name and proc_name not in [self.app_selector.itemText(i) for i in range(self.app_selector.count())]:
                        self.app_selector.addItem(proc_name)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Impossible de charger les applications : {str(e)}")

    def select_app(self):
        """Met à jour l'application sélectionnée."""
        if self.app_selector.currentIndex() > 0:
            self.current_app = self.app_selector.currentText()
            self.elapsed_time = self.get_app_time_today(self.current_app)
            self.update_time_label()
        else:
            self.current_app = None
            self.elapsed_time = 0
            self.update_time_label()

    def update_time_label(self):
        """Met à jour l'affichage du temps passé."""
        if self.elapsed_time < 60:
            pass   # self.time_label.setText(f"Temps passé : {self.elapsed_time} secondes")
        elif self.elapsed_time < 3600:
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60
            self.time_label.setText(f"Temps passé : {minutes} min {seconds} sec")
        else:
            hours = self.elapsed_time // 3600
            minutes = (self.elapsed_time % 3600) // 60
            seconds = self.elapsed_time % 60
            self.time_label.setText(f"Temps passé : {hours} h {minutes} min {seconds} sec")

    def set_time_limit(self):
        """Définit la limite de temps."""
        try:
            if not self.current_app:
                QMessageBox.warning(self, "Erreur", "Sélectionnez d'abord une application.")
                return
                
            limit_minutes = int(self.time_limit_input.text())
            if limit_minutes < 0:
                raise ValueError("La limite doit être positive")
                
            self.time_limit = limit_minutes * 60  # Convertir en secondes
            
            # Mettre à jour la limite dans les données d'utilisation
            today = datetime.now().strftime("%Y-%m-%d")
            if self.current_app not in self.usage_data:
                self.usage_data[self.current_app] = {"days": {}, "limit": self.time_limit}
            else:
                self.usage_data[self.current_app]["limit"] = self.time_limit
            
            # Sauvegarder les données
            self.save_usage_data()
            
            QMessageBox.information(self, "Succès", f"Limite de temps définie à {limit_minutes} minutes pour {self.current_app}.")
            
            # Mettre à jour l'affichage des statistiques
            self.update_stats()
        except ValueError as e:
            QMessageBox.warning(self, "Erreur", f"Veuillez entrer un nombre valide : {str(e)}")

    def toggle_tracking(self):
        """Démarre ou arrête le suivi du temps."""
        if not self.current_app or self.app_selector.currentIndex() == 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une application.")
            return

        if self.timer.isActive():
            # Arrêter le suivi
            elapsed = int(time.time() - self.start_time)
            self.update_app_usage(self.current_app, elapsed)
            self.timer.stop()
            self.toggle_tracking_button.setText("Démarrer le suivi")
            self.toggle_tracking_button.setStyleSheet(self.get_button_style("#3498db"))
        else:
            # Démarrer le suivi
            self.start_time = time.time()
            self.timer.start(1000)  # Mettre à jour toutes les secondes
            self.toggle_tracking_button.setText("Arrêter le suivi")
            self.toggle_tracking_button.setStyleSheet(self.get_button_style("#e74c3c"))

    def toggle_auto_tracking(self):
        """Démarre ou arrête le suivi automatique."""
        if self.auto_tracking_active:
            self.auto_timer.stop()
            self.auto_track_button.setText("Démarrer le suivi automatique")
            self.auto_track_button.setStyleSheet(self.get_button_style("#3498db"))
            self.auto_tracking_active = False
            
            # Enregistrer le temps d'utilisation pour toutes les applications suivies
            current_time = time.time()
            for app, start_time in self.tracked_processes.items():
                elapsed = int(current_time - start_time)
                self.update_app_usage(app, elapsed)
            
            # Réinitialiser les processus suivis
            self.tracked_processes = {}
        else:
            self.auto_timer.start(5000)  # Mettre à jour toutes les 5 secondes
            self.auto_track_button.setText("Arrêter le suivi automatique")
            self.auto_track_button.setStyleSheet(self.get_button_style("#e74c3c"))
            self.auto_tracking_active = True
            self.update_running_apps()  # Initialiser le suivi

    def update_running_apps(self):
        """Met à jour la liste des applications en cours d'exécution et leur temps d'utilisation."""
        current_time = time.time()
        current_apps = {}
        
        # Obtenir les processus en cours d'exécution
        try:
            for proc in psutil.process_iter(['name', 'pid']):
                try:
                    proc_info = proc.info
                    proc_name = proc_info['name']
                    
                    # Ne suivre que les processus avec une interface graphique
                    if proc_name.endswith('.exe') and proc_name != 'python.exe':
                        current_apps[proc_name] = proc_info['pid']
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
                    
            # Mettre à jour le temps pour les processus déjà suivis
            for app in list(self.tracked_processes.keys()):
                if app not in current_apps:
                    # L'application n'est plus en cours d'exécution
                    elapsed = int(current_time - self.tracked_processes[app])
                    self.update_app_usage(app, elapsed)
                    del self.tracked_processes[app]
            
            # Ajouter les nouveaux processus
            for app in current_apps:
                if app not in self.tracked_processes:
                    self.tracked_processes[app] = current_time
            
            # Mettre à jour la table
            self.active_apps_table.setRowCount(len(self.tracked_processes))
            
            row = 0
            for app in self.tracked_processes:
                # Colonne 1: Nom de l'application
                self.active_apps_table.setItem(row, 0, QTableWidgetItem(app))
                
                # Colonne 2: Temps aujourd'hui
                app_time = self.get_app_time_today(app)
                time_text = self.format_time(app_time)
                self.active_apps_table.setItem(row, 1, QTableWidgetItem(time_text))
                
                # Colonne 3: Limite
                limit = self.get_app_limit(app)
                limit_text = self.format_time(limit) if limit > 0 else "Pas de limite"
                self.active_apps_table.setItem(row, 2, QTableWidgetItem(limit_text))
                
                row += 1
            
            # Vérifier si les limites sont dépassées
            self.check_time_limits()
                
        except Exception as e:
            print(f"Erreur lors de la mise à jour des applications en cours d'exécution : {str(e)}")

    def update_time(self):
        """Met à jour le temps écoulé pour l'application suivie manuellement."""
        if self.start_time:
            self.elapsed_time = int(time.time() - self.start_time) + self.get_app_time_today(self.current_app)
            self.update_time_label()
            
            # Vérifier si la limite est dépassée
            if self.time_limit > 0 and self.elapsed_time >= self.time_limit:
                self.show_time_limit_warning(self.current_app)

    def update_app_usage(self, app_name, elapsed_seconds):
        """Met à jour les données d'utilisation pour une application."""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if app_name not in self.usage_data:
            self.usage_data[app_name] = {"days": {}, "limit": 0}
            
        if today not in self.usage_data[app_name]["days"]:
            self.usage_data[app_name]["days"][today] = elapsed_seconds
        else:
            self.usage_data[app_name]["days"][today] += elapsed_seconds
            
        # Sauvegarder les données
        self.save_usage_data()
        
        # Mettre à jour les statistiques
        self.update_stats()

    def get_app_time_today(self, app_name):
        """Retourne le temps d'utilisation aujourd'hui pour une application."""
        if not app_name:
            return 0
            
        today = datetime.now().strftime("%Y-%m-%d")
        
        if app_name in self.usage_data and today in self.usage_data[app_name]["days"]:
            return self.usage_data[app_name]["days"][today]
        return 0

    def get_app_limit(self, app_name):
        """Retourne la limite de temps pour une application."""
        if app_name in self.usage_data:
            return self.usage_data[app_name].get("limit", 0)
        return 0

    def check_time_limits(self):
        """Vérifie si les limites de temps sont dépassées pour les applications suivies."""
        today = datetime.now().strftime("%Y-%m-%d")
        
        for app in self.tracked_processes:
            limit = self.get_app_limit(app)
            if limit > 0:
                time_today = self.get_app_time_today(app)
                if time_today >= limit:
                    self.show_time_limit_warning(app)

    def show_time_limit_warning(self, app_name):
        """Affiche un avertissement lorsque la limite de temps est dépassée."""
        limit_minutes = self.get_app_limit(app_name) // 60
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Limite de temps dépassée")
        msg.setText(f"Vous avez dépassé votre limite de temps de {limit_minutes} minutes pour {app_name}.")
        msg.setInformativeText("Il est recommandé de faire une pause.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def update_stats(self):
        """Met à jour le tableau des statistiques."""
        self.stats_table.setRowCount(len(self.usage_data))
        
        row = 0
        for app, data in self.usage_data.items():
            # Colonne 1: Nom de l'application
            self.stats_table.setItem(row, 0, QTableWidgetItem(app))
            
            # Colonne 2: Temps total
            total_time = sum(data["days"].values())
            time_text = self.format_time(total_time)
            self.stats_table.setItem(row, 1, QTableWidgetItem(time_text))
            
            # Colonne 3: Dernière utilisation
            if data["days"]:
                last_date = max(data["days"].keys())
                last_date_obj = datetime.strptime(last_date, "%Y-%m-%d")
                last_date_text = last_date_obj.strftime("%d/%m/%Y")
                self.stats_table.setItem(row, 2, QTableWidgetItem(last_date_text))
            else:
                self.stats_table.setItem(row, 2, QTableWidgetItem("Jamais"))
            
            row += 1

    def reset_stats(self):
        """Réinitialise les statistiques."""
        reply = QMessageBox.question(
            self, 'Confirmation',
            "Voulez-vous vraiment réinitialiser toutes les statistiques ?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.usage_data = {}
            self.save_usage_data()
            self.update_stats()
            QMessageBox.information(self, "Succès", "Les statistiques ont été réinitialisées.")

    def format_time(self, seconds):
        """Formate un temps en secondes en un format lisible."""
        if seconds < 60:
            return f"{seconds} sec"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes} min"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours} h {minutes} min"

    def load_usage_data(self):
        """Charge les données d'utilisation à partir du fichier."""
        try:
            if os.path.exists("data/usage_data.json"):
                with open("data/usage_data.json", "r") as f:
                    self.usage_data = json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement des données : {str(e)}")
            self.usage_data = {}

    def save_usage_data(self):
        """Sauvegarde les données d'utilisation dans un fichier."""
        try:
            with open("data/usage_data.json", "w") as f:
                json.dump(self.usage_data, f)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des données : {str(e)}")

    def get_button_style(self, color):
        """Retourne le style pour un bouton."""
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {color}99;
            }}
            QPushButton:pressed {{
                background-color: {color}70;
            }}
        """
