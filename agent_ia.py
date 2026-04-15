import feedparser
from google import genai
import os

# 1. Connexion avec la nouvelle bibliothèque
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Erreur : Clé API manquante.")
    exit(1)

client = genai.Client(api_key=api_key)

# 2. Vos sources
sources = [
    "https://tldr.tech/ai/rss",
    "https://www.therundown.ai/feed",
    "https://news.google.com/rss/search?q=artificial+intelligence+when:24h&hl=en-US&gl=US&ceid=US:en"
]

all_titles = ""
print("Récupération des news...")
for url in sources:
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            all_titles += f"- {entry.title}\n"
    except:
        continue

# 3. Génération avec le modèle universel
try:
    # On utilise "gemini-1.5-flash" tout court, la nouvelle lib gère le reste
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=f"Résume en français les news IA suivantes :\n{all_titles}"
    )
    
    print("\n" + "="*40)
    print("✨ VOTRE VEILLE IA DU JOUR ✨")
    print("="*40 + "\n")
    print(response.text)
    
except Exception as e:
    print(f"Erreur avec la nouvelle API : {e}")
    exit(1)
