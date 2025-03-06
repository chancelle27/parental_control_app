from mitmproxy import http
import re

# Liste des sites bloqués
BLOCKED_SITES = {"facebook.com", "youtube.com", "tiktok.com"}

# Liste des mots-clés interdits
BLOCKED_KEYWORDS = {"casino", "porno", "betting"}

# URL de redirection vers la page de blocage
REDIRECT_PAGE = "http://127.0.0.1:5000/block_page"


def request(flow: http.HTTPFlow):
    """ Intercepte les requêtes et bloque les sites interdits """
    url = flow.request.pretty_url

    # Vérifier si le site est bloqué
    if any(blocked in url for blocked in BLOCKED_SITES):
        flow.response = http.Response.make(
            302,  # Redirection
            b"",  # Pas de contenu
            {"Location": REDIRECT_PAGE}
        )
        flow.kill()  # Stoppe immédiatement la requête


def response(flow: http.HTTPFlow):
    """ Intercepte les réponses et filtre le contenu """
    if flow.response and flow.response.content:
        try:
            content = flow.response.content.decode("utf-8", errors="ignore")

            # Vérifier si des mots-clés bloqués sont présents
            if any(re.search(r"\b" + re.escape(keyword) + r"\b", content, re.IGNORECASE) for keyword in BLOCKED_KEYWORDS):
                flow.response = http.Response.make(
                    302,
                    b"",
                    {"Location": REDIRECT_PAGE}
                )
        except Exception as e:
            print(f"Erreur lors du traitement du contenu : {e}")
