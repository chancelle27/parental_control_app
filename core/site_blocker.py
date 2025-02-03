import os

HOSTS_FILE = "/etc/hosts"  # Modifier selon le système d'exploitation
REDIRECT_IP = "127.0.0.1"

class SiteBlocker:
    def __init__(self, blocked_sites_file):
        self.blocked_sites_file = blocked_sites_file

    def block_sites(self):
        with open(self.blocked_sites_file, "r") as file:
            sites = file.readlines()
        
        with open(HOSTS_FILE, "a") as hosts:
            for site in sites:
                hosts.write(f"{REDIRECT_IP} {site.strip()}\n")

    def unblock_sites(self):
        with open(HOSTS_FILE, "r") as file:
            lines = file.readlines()
        
        with open(HOSTS_FILE, "w") as file:
            for line in lines:
                if not any(site.strip() in line for site in open(self.blocked_sites_file)):
                    file.write(line)
