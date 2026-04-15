import feedparser
import google.generativeai as genai
import os

# Configuration de l'IA avec votre clé cachée
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Vos 3 sources
sources = [
    "https://tldr.tech/ai/rss",
    "https://www.therundown.ai/feed",
    "https://news.google.com/rss/search?q=artificial+intelligence+when:24h&hl=en-US&gl=US&ceid=US:en"
]

all_titles = ""

# On récupère les titres des news
for url in sources:
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            all_titles += f"- {entry.title}\n"
    except:
        continue

# Le message pour l'IA
prompt = f"Tu es un expert en technologie. Voici les actualités IA du jour :\n{all_titles}\n\nFais-moi un résumé en français des 5 news les plus importantes sous forme de liste à puces. Sois bref et percutant."

# Génération du résumé
response = model.generate_content(prompt)

print("--- VEILLE IA DU JOUR ---")
print(response.text)
