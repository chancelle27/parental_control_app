import sys
import os
import psutil
import winapps
import winreg
import ctypes
import json
import subprocess
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget,
    QMessageBox, QHBoxLayout, QListWidgetItem, QFrame,
    QSystemTrayIcon, QMenu, QAction, QApplication
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QTimer, pyqtSignal

# Vérifier si le programme a les droits d'administrateur
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

# Relancer le programme avec des droits administrateur si nécessaire
def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

class AppBlocker:
    """Classe responsable du blocage des applications"""

    CONFIG_FILE = os.path.join(os.path.expanduser('~'), 'appblocker_config.json')
    STARTUP_REG_PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

    def __init__(self):
        self.blocked_apps = self.load_config()
        self.executable_paths = {}  # Stocke les chemins complets des exécutables

    def load_config(self):
        """Charge la configuration sauvegardée"""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_config(self):
        """Sauvegarde la configuration"""
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(self.blocked_apps, f)

    def find_executable_path(self, app_name):
        """Trouve le chemin complet de l'exécutable à partir du nom de l'application"""
        if app_name in self.executable_paths:
            return self.executable_paths[app_name]

        for app in winapps.search_installed():
            if app.name == app_name and app.install_location:
                for root, dirs, files in os.walk(app.install_location):
                    for file in files:
                        if file.lower().endswith('.exe'):
                            path = os.path.join(root, file)
                            self.executable_paths[app_name] = path
                            return path
        return None

    def apply_block_permissions(self, exe_path):
        """
        Applique des restrictions sur l'exécutable pour empêcher son exécution.
        Ici, on utilise icacls pour refuser les droits de lecture et d'exécution à l'utilisateur courant.
        """
        try:
            username = os.getlogin()
            cmd = f'icacls "{exe_path}" /deny {username}:(RX)'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return True
            else:
                print(f"Erreur icacls: {result.stderr}")
                return False
        except Exception as e:
            print(f"Erreur lors de l'application des permissions: {e}")
            return False

    def remove_block_permissions(self, exe_path):
        """
        Restaure les permissions sur l'exécutable en supprimant le refus d'accès appliqué précédemment.
        """
        try:
            username = os.getlogin()
            cmd = f'icacls "{exe_path}" /remove:d {username}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return True
            else:
                print(f"Erreur icacls: {result.stderr}")
                return False
        except Exception as e:
            print(f"Erreur lors de la restauration des permissions: {e}")
            return False

    def block_app(self, app_name):
        """
        Bloque une application :
          - Recherche son exécutable complet.
          - Applique des restrictions via icacls pour interdire son exécution.
          - Sauvegarde l'information dans la configuration.
        """
        exe_path = self.find_executable_path(app_name)
        if exe_path:
            if self.apply_block_permissions(exe_path):
                self.blocked_apps[app_name] = {
                    'path': exe_path  # On stocke le chemin complet
                }
                self.save_config()
                return True
            else:
                return False
        return False

    def unblock_app(self, app_name):
        """
        Débloque une application :
          - Restaure les permissions sur l'exécutable.
          - Retire l'application de la configuration.
        """
        if app_name in self.blocked_apps:
            exe_path = self.blocked_apps[app_name]['path']
            if self.remove_block_permissions(exe_path):
                del self.blocked_apps[app_name]
                self.save_config()
                return True
            else:
                return False
        return False

    def kill_blocked_apps(self):
        """
        Tue les processus dont le chemin complet de l'exécutable correspond à celui d'une application bloquée.
        Cela permet d'être sûr que c'est bien l'application bloquée qui est terminée, même si le nom du
        processus diffère.
        """
        killed_apps = []
        for app_name, info in self.blocked_apps.items():
            blocked_path = info.get('path')
            for proc in psutil.process_iter(['pid']):
                try:
                    proc_path = proc.exe()
                    if os.path.normcase(proc_path) == os.path.normcase(blocked_path):
                        proc.terminate()
                        killed_apps.append(app_name)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        return set(killed_apps)

    def is_app_blocked(self, app_name):
        """Vérifie si une application est bloquée."""
        return app_name in self.blocked_apps

    def add_to_startup(self):
        """Ajoute l'application au démarrage de Windows."""
        if is_admin():
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    self.STARTUP_REG_PATH,
                    0,
                    winreg.KEY_WRITE
                )
                winreg.SetValueEx(
                    key,
                    "AppBlocker",
                    0,
                    winreg.REG_SZ,
                    f'"{sys.executable}" "{os.path.abspath(sys.argv[0])}" --background'
                )
                winreg.CloseKey(key)
                return True
            except Exception as e:
                print(f"Erreur lors de l'ajout au démarrage: {e}")
                return False
        return False

    def remove_from_startup(self):
        """Retire l'application du démarrage de Windows."""
        if is_admin():
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    self.STARTUP_REG_PATH,
                    0,
                    winreg.KEY_WRITE
                )
                winreg.DeleteValue(key, "AppBlocker")
                winreg.CloseKey(key)
                return True
            except Exception as e:
                print(f"Erreur lors du retrait du démarrage: {e}")
                return False
        return False

class BlockAppsPage(QWidget):
    update_status_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.app_blocker = AppBlocker()
        self.init_ui()
        self.setup_monitor()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("Blocage d'Applications")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("color: #e74c3c; margin-bottom: 15px;")
        layout.addWidget(title)

        self.refresh_button = QPushButton("Rafraîchir la liste")
        self.refresh_button.setStyleSheet(self.get_button_style("#27ae60"))
        self.refresh_button.clicked.connect(self.load_installed_apps)
        layout.addWidget(self.refresh_button)

        self.status_label = QLabel("Surveillance active: Aucune application bloquée pour le moment")
        self.status_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        layout.addWidget(self.status_label)

        startup_layout = QHBoxLayout()
        self.startup_button = QPushButton("Activer au démarrage de Windows")
        self.startup_button.setStyleSheet(self.get_button_style("#9b59b6"))
        self.startup_button.clicked.connect(self.toggle_startup)
        startup_layout.addWidget(self.startup_button)
        layout.addLayout(startup_layout)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #bdc3c7;")
        layout.addWidget(separator)

        self.apps_list = QListWidget()
        self.apps_list.setStyleSheet(self.get_list_style())
        layout.addWidget(self.apps_list)

        self.update_startup_button()
        self.load_installed_apps()
        self.update_status_signal.connect(self.update_status)

    def setup_monitor(self):
        self.monitor_timer = QTimer(self)
        self.monitor_timer.timeout.connect(self.check_blocked_apps)
        self.monitor_timer.start(2000)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon.fromTheme("security-high"))
        tray_menu = QMenu()
        show_action = QAction("Afficher", self)
        show_action.triggered.connect(self.show)
        exit_action = QAction("Quitter", self)
        exit_action.triggered.connect(self.exit_app)
        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(exit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def exit_app(self):
        self.monitor_timer.stop()
        QApplication.quit()

    def check_blocked_apps(self):
        killed_apps = self.app_blocker.kill_blocked_apps()
        if killed_apps:
            apps_list = ", ".join(killed_apps)
            self.update_status_signal.emit(f"Applications bloquées: {apps_list}")
            self.tray_icon.showMessage(
                "Applications bloquées",
                f"Les applications suivantes ont été bloquées: {apps_list}",
                QSystemTrayIcon.Warning
            )

    def update_status(self, text):
        self.status_label.setText(text)

    def toggle_startup(self):
        if not is_admin():
            response = QMessageBox.question(
                self,
                "Droits administrateur requis",
                "Cette fonctionnalité nécessite des droits administrateur. Voulez-vous relancer l'application en tant qu'administrateur ?",
                QMessageBox.Yes | QMessageBox.No
            )
            if response == QMessageBox.Yes:
                run_as_admin()
            return

        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            AppBlocker.STARTUP_REG_PATH,
            0,
            winreg.KEY_READ
        )
        try:
            winreg.QueryValueEx(key, "AppBlocker")
            is_in_startup = True
        except:
            is_in_startup = False
        winreg.CloseKey(key)

        if is_in_startup:
            success = self.app_blocker.remove_from_startup()
            if success:
                QMessageBox.information(self, "Succès", "L'application ne démarrera plus automatiquement avec Windows.")
        else:
            success = self.app_blocker.add_to_startup()
            if success:
                QMessageBox.information(self, "Succès", "L'application démarrera automatiquement avec Windows.")
        self.update_startup_button()

    def update_startup_button(self):
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            AppBlocker.STARTUP_REG_PATH,
            0,
            winreg.KEY_READ
        )
        try:
            winreg.QueryValueEx(key, "AppBlocker")
            self.startup_button.setText("Désactiver le démarrage automatique")
        except:
            self.startup_button.setText("Activer au démarrage de Windows")
        winreg.CloseKey(key)

    def load_installed_apps(self):
        self.apps_list.clear()
        for app in winapps.search_installed():
            if app.name and len(app.name.strip()) > 0:
                self.add_app_to_list(app.name)

    def add_app_to_list(self, name):
        item = QListWidgetItem(self.apps_list)
        row_widget = QWidget()
        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(5, 5, 5, 5)
        label = QLabel(name)
        label.setFont(QFont("Arial", 14))
        row_layout.addWidget(label)
        is_blocked = self.app_blocker.is_app_blocked(name)
        status_label = QLabel("BLOQUÉE" if is_blocked else "")
        if is_blocked:
            status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
        row_layout.addWidget(status_label)
        row_layout.addStretch()
        button = QPushButton("Débloquer" if is_blocked else "Bloquer")
        button.setStyleSheet(self.get_button_style("#3498db" if is_blocked else "#e74c3c"))
        button.clicked.connect(lambda _, n=name, b=button, s=status_label: self.toggle_block_app(n, b, s))
        row_layout.addWidget(button)
        row_widget.setLayout(row_layout)
        item.setSizeHint(row_widget.sizeHint())
        self.apps_list.setItemWidget(item, row_widget)

    def toggle_block_app(self, app_name, button, status_label):
        if self.app_blocker.is_app_blocked(app_name):
            success = self.app_blocker.unblock_app(app_name)
            if success:
                QMessageBox.information(self, "Succès", f"{app_name} a été débloquée.")
                button.setText("Bloquer")
                status_label.setText("")
                status_label.setStyleSheet("")
            else:
                QMessageBox.warning(self, "Erreur", f"Impossible de débloquer {app_name}.")
        else:
            success = self.app_blocker.block_app(app_name)
            if success:
                QMessageBox.information(self, "Succès", f"{app_name} a été bloquée.")
                button.setText("Débloquer")
                status_label.setText("BLOQUÉE")
                status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
            else:
                QMessageBox.warning(self, "Erreur", f"Impossible de bloquer {app_name}. L'exécutable n'a pas été trouvé ou les permissions n'ont pas pu être modifiées.")

    def get_button_style(self, color):
        return f"""
        QPushButton {{
            background-color: {color};
            color: white;
            border-radius: 5px;
            padding: 8px 16px;
            font-weight: bold;
            font-size: 12px;
        }}
        QPushButton:hover {{
            background-color: {color}99;
        }}
        QPushButton:pressed {{
            background-color: {color}70;
        }}
        """.strip()

    def get_list_style(self):
        return """
        QListWidget {
            background-color: white;
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            padding: 5px;
        }
        QListWidget::item {
            padding: 5px;
            border-bottom: 1px solid #bdc3c7;
        }
        QListWidget::item:selected {
            background-color: #3498db;
            color: white;
        }
        """.strip()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BlockAppsPage()
    window.setWindowTitle("App Blocker")
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
