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
    "https://news.google.com/rss/search?q=artificial+intelligence+when:24h&hl=en-US&gl=US&ceid=US:en",
    "https://www.usine-digitale.fr/intelligence-artificielle/rss",
    "https://www.lemonde.fr/pixels/rss_full.xml",
    "https://www.journaldunet.com/rss/technologies/intelligence-artificielle/",
    "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
    "https://rss.arxiv.org/rss/cs.AI",
    "https://venturebeat.com/category/ai/feed/"
]

all_titles = ""
print("Récupération des news...")
for url in sources:
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]:
            all_titles += f"- {entry.title}\n"
    except:
        continue

# 3. Détection automatique corrigée
print("Recherche des modèles disponibles...")
target_model = None
try:
    # On liste les modèles et on affiche leurs noms pour débugger
    for m in client.models.list():
        # Dans la nouvelle lib, on vérifie les méthodes supportées comme ceci :
        if 'generateContent' in m.supported_actions:
            print(f"Modèle compatible trouvé : {m.name}")
            # On cherche de préférence un modèle "flash"
            if "flash" in m.name.lower():
                target_model = m.name
                break
    
    if not target_model:
        # Si aucun flash n'est trouvé, on prend le tout premier disponible
        models = list(client.models.list())
        target_model = models[0].name
        
except Exception as e:
    print(f"Erreur lors de la liste : {e}")
    # Si tout échoue, on tente le nom technique complet
    target_model = "models/gemini-1.5-flash"

print(f"Tentative finale avec : {target_model}")

# 4. Génération
try:
    response = client.models.generate_content(
        model=target_model,
        contents=f"Résume en français les news IA suivantes :\n{all_titles}"
    )
    
    print("\n" + "="*40)
    print("✨ VOTRE VEILLE IA DU MATIN ✨")
    print("="*40 + "\n")
    print(response.text)
    
except Exception as e:
    print(f"Échec critique : {e}")
    exit(1)
