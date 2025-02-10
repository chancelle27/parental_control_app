import os

# Chemin du fichier hosts
HOSTS_PATH = "C:\\Windows\\System32\\drivers\\etc\\hosts" if os.name == "nt" else "/etc/hosts"

def block_site(site_url):
    """Ajoute un site au fichier hosts pour le bloquer."""
    try:
        with open(HOSTS_PATH, "a") as file:
            file.write(f"\n127.0.0.1 {site_url}\n127.0.0.1 www.{site_url}\n")
        print(f"Site bloque : {site_url}")
    except PermissionError:
        print("Erreur : Permission refusee. Executez en mode administrateur.")

def unblock_site(site_url):
    """Supprime un site du fichier hosts pour le débloquer."""
    try:
        with open(HOSTS_PATH, "r") as file:
            lines = file.readlines()
        
        with open(HOSTS_PATH, "w") as file:
            for line in lines:
                if site_url not in line:
                    file.write(line)
        print(f"Site debloque : {site_url}")
    except PermissionError:
        print("Erreur : Permission refusee. Executez en mode administrateur.")

def is_site_blocked(site_url):
    """Vérifie si un site est déjà bloqué."""
    if not os.path.exists(HOSTS_PATH):
        return False
    
    with open(HOSTS_PATH, "r") as file:
        return any(site_url in line for line in file.readlines())