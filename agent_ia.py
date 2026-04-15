import feedparser
from google import genai
import os
import time

# 1. Connexion
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Erreur : Clé API manquante.")
    exit(1)

client = genai.Client(api_key=api_key)

# 2. Sources
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
        for entry in feed.entries[:3]: # On réduit à 3 news pour économiser les jetons (tokens)
            all_titles += f"- {entry.title}\n"
    except:
        continue

# 3. Génération avec sécurité anti-quota
try:
    # On revient sur le 1.5-flash qui est plus souvent ouvert en gratuit que le 2.0
    response = client.models.generate_content(
        model="gemini-1.5-flash", 
        contents=f"Résume en français les news IA suivantes :\n{all_titles}"
    )
    
    print("\n" + "="*40)
    print("✨ VOTRE VEILLE IA DU JOUR ✨")
    print("="*40 + "\n")
    print(response.text)
    
except Exception as e:
    print(f"Erreur rencontrée : {e}")
    print("Astuce : Allez sur Google AI Studio, créez une NOUVELLE clé API dans un NOUVEAU projet.")
    exit(1)
