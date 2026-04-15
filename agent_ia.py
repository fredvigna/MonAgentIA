import feedparser
from google import genai
import os

# 1. Connexion avec votre clé API
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Erreur : Clé API manquante dans les Secrets GitHub.")
    exit(1)

client = genai.Client(api_key=api_key)

# 2. Collecte des news
sources = [
    "https://tldr.tech/ai/rss",
    "https://www.therundown.ai/feed",
    "https://news.google.com/rss/search?q=artificial+intelligence+when:24h&hl=en-US&gl=US&ceid=US:en"
]

all_titles = ""
print("Récupération des actualités...")
for url in sources:
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:4]:
            all_titles += f"- {entry.title}\n"
    except:
        continue

# 3. Appel au modèle spécifique Gemini 2.25 Flash
try:
    print("Génération du résumé avec Gemini 2.25 Flash...")
    response = client.models.generate_content(
        model="gemini-2.25-flash", # Nom exact affiché dans votre console
        contents=f"Tu es un expert en IA. Résume en français ces news de façon percutante :\n{all_titles}"
    )
    
    print("\n" + "="*40)
    print("✨ VOTRE VEILLE IA DU JOUR ✨")
    print("="*40 + "\n")
    print(response.text)
    
except Exception as e:
    print(f"Erreur avec le modèle 2.25 : {e}")
    # Si le nom exact échoue encore, on tente la version courte au cas où
    try:
        print("Nouvel essai avec le nom court...")
        response = client.models.generate_content(model="gemini-2.25", contents=all_titles)
        print(response.text)
    except:
        exit(1)
