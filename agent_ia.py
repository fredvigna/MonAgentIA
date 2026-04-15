import feedparser
import google.generativeai as genai
import os

# 1. Connexion
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Erreur : Clé API manquante.")
    exit(1)

genai.configure(api_key=api_key)

# Test de plusieurs noms de modèles pour éviter la 404
try:
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except:
    model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Sources
sources = [
    "https://tldr.tech/ai/rss",
    "https://www.therundown.ai/feed",
    "https://news.google.com/rss/search?q=artificial+intelligence+when:24h&hl=en-US&gl=US&ceid=US:en"
]

all_titles = ""
for url in sources:
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            all_titles += f"- {entry.title}\n"
    except:
        continue

# 3. Prompt
prompt = f"Résume en français les news IA suivantes de façon percutante :\n{all_titles}"

# 4. Exécution
try:
    response = model.generate_content(prompt)
    print(response.text)
except Exception as e:
    print(f"Nouvelle erreur rencontrée : {e}")
    exit(1)
