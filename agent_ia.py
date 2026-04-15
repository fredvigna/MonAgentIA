import feedparser
from google import genai
import os

# 1. Connexion
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Erreur : Clé API manquante.")
    exit(1)

client = genai.Client(api_key=api_key)

# 2. Collecte des news
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
        for entry in feed.entries[:4]:
            all_titles += f"- {entry.title}\n"
    except:
        continue

# 3. Détection automatique du modèle disponible
print("Recherche du modèle disponible sur votre compte...")
try:
    available_models = [m.name for m in client.models.list() if 'generateContent' in m.supported_methods]
    # On cherche le modèle le plus récent qui contient "flash"
    target_model = next((m for m in available_models if "flash" in m), available_models[0])
    print(f"Modèle trouvé et utilisé : {target_model}")
except Exception as e:
    print(f"Impossible de lister les modèles : {e}")
    target_model = "gemini-1.5-flash" # Repli par défaut

# 4. Génération
try:
    response = client.models.generate_content(
        model=target_model,
        contents=f"Résume en français les news IA suivantes :\n{all_titles}"
    )
    
    print("\n" + "="*40)
    print("✨ VOTRE VEILLE IA DU JOUR ✨")
    print("="*40 + "\n")
    print(response.text)
    
except Exception as e:
    print(f"Échec final : {e}")
    exit(1)
