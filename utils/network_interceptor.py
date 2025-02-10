from mitmproxy.tools.main import mitmdump
from utils.keyword_filter import addons

def start_interceptor():
    """Démarre l'interception réseau avec mitmproxy."""
    mitmdump(["-s", __file__, "--mode", "transparent"] + addons)

if __name__ == "__main__":
    start_interceptor()