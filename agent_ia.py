import feedparser
from google import genai
import os

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
        for entry in feed.entries[:5]:
            all_titles += f"- {entry.title}\n"
    except:
        continue

if not all_titles:
    all_titles = "Aucune news trouvée, fais un point général sur l'IA."

# 3. Génération avec Gemini 2.0 Flash
try:
    # On force le modèle 2.0 qui est souvent plus disponible sur les nouveaux projets
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=f"Résume en français les news IA suivantes :\n{all_titles}"
    )
    
    print("\n" + "="*40)
    print("✨ VOTRE VEILLE IA DU JOUR ✨")
    print("="*40 + "\n")
    print(response.text)
    
except Exception as e:
    print(f"Échec avec Gemini 2.0 : {e}")
    # Dernier recours : si 2.0 échoue, on tente le modèle "pro"
    try:
        response = client.models.generate_content(model="gemini-1.5-pro", contents=all_titles)
        print(response.text)
    except:
        print("Tous les modèles ont échoué. Vérifiez votre accès sur Google AI Studio.")
        exit(1)
