import requests

post_url = input("Colle ici l'URL de la publication Facebook : ").strip()
access_token = input("Colle ici ton token d'accès Facebook : ").strip()

def get_post_id_from_url(url):
    parts = url.strip().split("/")
    for part in reversed(parts):
        if part.isdigit():
            return part
    raise ValueError("Impossible d'extraire l'ID du post.")

try:
    post_id = get_post_id_from_url(post_url)
except ValueError as e:
    print(e)
    exit(1)

post_api = f'https://graph.facebook.com/v18.0/{post_id}?fields=message&access_token={access_token}'
post_response = requests.get(post_api).json()
message = post_response.get('message', '[Pas de texte]')

comments_api = f'https://graph.facebook.com/v18.0/{post_id}/comments?fields=from,message&limit=100&access_token={access_token}'
comments_response = requests.get(comments_api).json()
comments = comments_response.get('data', [])

with open("resultat.txt", "w", encoding="utf-8") as f:
    f.write("Texte de la publication:\n")
    f.write(message + "\n\n")
    f.write("Commentaires:\n")
    for c in comments:
        auteur = c['from']['name']
        contenu = c['message']
        f.write(f"- {auteur} : {contenu}\n")

print("\n✅ Fichier 'resultat.txt' généré avec succès.")
