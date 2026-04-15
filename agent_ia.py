import feedparser
import google.generativeai as genai
import os

# 1. Connexion sécurisée à l'IA
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Erreur : La clé API GEMINI_API_KEY est manquante dans les Secrets GitHub.")
    exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Vos sources de news (TLDR, The Rundown, Google News)
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
        # On récupère les 5 titres les plus récents de chaque source
        for entry in feed.entries[:5]:
            all_titles += f"- {entry.title}\n"
    except Exception as e:
        print(f"Erreur sur la source {url}: {e}")
        continue

if not all_titles:
    print("Aucune actualité trouvée. Vérifiez les flux RSS.")
    exit(1)

# 3. Préparation du prompt pour l'IA
prompt = f"""
Tu es un expert en veille technologique spécialisé en Intelligence Artificielle. 
Voici une liste de titres d'actualités récents en anglais :
{all_titles}

Mission : 
1. Sélectionne les 5 news les plus importantes.
2. Traduis et rédige un résumé court (2 phrases max par news) en français.
3. Utilise un ton professionnel avec des emojis.
"""

# 4. Génération et affichage
try:
    response = model.generate_content(prompt)
    print("\n" + "="*40)
    print("✨ VOTRE VEILLE IA DU MATIN ✨")
    print("="*40 + "\n")
    print(response.text)
except Exception as e:
    print(f"Erreur lors de la génération par l'IA : {e}")
    exit(1)
