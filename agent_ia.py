import os
import google.generativeai as genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("ERREUR : Secret non trouvé dans GitHub")
    exit(1)

try:
    genai.configure(api_key=api_key)
    # On essaie le nom standard, sinon on utilise la version générique
    model_name = 'gemini-1.5-flash-latest' 
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Dis bonjour en français")
    print(f"L'IA répond : {response.text}")
except Exception as e:
    print(f"ERREUR TECHNIQUE : {e}")
    exit(1)
