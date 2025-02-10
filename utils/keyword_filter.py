from mitmproxy import http
from bs4 import BeautifulSoup

class KeywordFilter:
    def __init__(self, blocked_keywords):
        self.blocked_keywords = blocked_keywords

    def request(self, flow: http.HTTPFlow):
        # Vérifier si l'URL contient un mot-clé bloqué
        print(f"Intercepting request to: {flow.request.pretty_url}")
        
        if any(keyword in flow.request.pretty_url for keyword in self.blocked_keywords):
            print(f"Blocked URL: {flow.request.pretty_url} (contains blocked keyword)")
            flow.response = http.Response.make(
                403,  # Code de statut HTTP "Interdit"
                b"Acces bloque : mot-cle interdit detecte dans l'URL",
                {"Content-Type": "text/plain"}
            )

    def response(self, flow: http.HTTPFlow):
        # Vérifier si le contenu de la réponse contient un mot-clé bloqué
        print(f"Intercepting response from: {flow.request.pretty_url}")
        
        if self.analyze_content(flow.response.text):
            print(f"Blocked content from: {flow.request.pretty_url} (contains blocked keyword)")
            flow.response = http.Response.make(
                403,  # Code de statut HTTP "Interdit"
                b"Acces bloque : contenu interdit detecte",
                {"Content-Type": "text/plain"}
            )

    def analyze_content(self, content):
        """Analyse le contenu pour détecter les mots-clés bloqués."""
        soup = BeautifulSoup(content, "html.parser")
        text = soup.get_text().lower()
        
        for keyword in self.blocked_keywords:
            if keyword in text:
                print(f"Found blocked keyword: {keyword}")
                return True
        return False

def load_blocked_keywords():
    """Charge les mots-clés bloqués depuis le fichier."""
    try:
        with open("data/blocked_keywords.txt", "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print("Aucun fichier de mots-clés bloqués trouvé.")
        return []

# Charger les mots-clés bloqués
blocked_keywords = load_blocked_keywords()
print(f"Loaded blocked keywords: {blocked_keywords}")
addons = [KeywordFilter(blocked_keywords)]