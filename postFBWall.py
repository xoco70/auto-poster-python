import facebook
import os
from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
PAGE_ID = os.getenv('PAGE_ID')

def post_to_facebook(page_id, access_token, message, link=None, image_url=None):
    graph = facebook.GraphAPI(access_token)

    post_data = {
        'message': message,
    }

    if link:
        post_data['link'] = link

    if image_url:
        post_data['picture'] = image_url

    try:
        post_id = graph.put_object(page_id, "feed", **post_data)
        print(f"Post créé avec succès. ID du post : {post_id['id']}")
    except facebook.GraphAPIError as e:
        print(f"Une erreur s'est produite : {e}")

if __name__ == "__main__":
    # Exemple de message à publier
    message = """🍇 Après les vendanges, voici le remède miracle de nos ancêtres ! 🌿
Cette pub vintage de Ricqlès (1924) nous rappelle que l'alcool de menthe était le secret des vignerons fatigués. Un verre d'eau, une goutte de Ricqlès, et hop ! 💪
Vos astuces post-vendanges ? Partagez en commentaire ! 😉
#Ricqles #Vendanges2024 #PubVintage #RemèdeDeGrandMère"""

    link = "https://catalogue.cappiello.fr/produit/ricqles-2/"
  #  image_url = "https://catalogue.cappiello.fr/wp-content/uploads/2024/07/ab4783c4831a1117017267597a6e0635-1.jpg"

    post_to_facebook(PAGE_ID, ACCESS_TOKEN, message, link=link)