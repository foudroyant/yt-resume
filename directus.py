import requests
from dotenv import load_dotenv
import os
import json
load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
DIRECTUS_URL = os.getenv("BAESE_URL_DIRECTUS")
TOKEN_FILE = os.getenv("TOKEN_FILE")

# === GÉNÉRATION DES TOKENS ===
def login():
    response = requests.post(f"{DIRECTUS_URL}/auth/login", json={
        "email": EMAIL,
        "password": PASSWORD
    })
    response.raise_for_status()
    #print("Réponse :", response.status_code, response.json())
    tokens = response.json()["data"]
    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f)
    return tokens


# === RAFRAÎCHIR ACCESS TOKEN ===
def refresh_token(refresh_token):
    response = requests.post(f"{DIRECTUS_URL}/auth/refresh", json={
        "refresh_token": refresh_token
    })
    response.raise_for_status()
    tokens = response.json()["data"]
    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f)
    return tokens

# === CHARGER LE TOKEN ===
def get_tokens():
    try:
        with open(TOKEN_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return login()


def get_headers():
    tokens = get_tokens()
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    # Test si le token est encore bon
    test = requests.get(f"{DIRECTUS_URL}/users/me", headers=headers)
    if test.status_code == 401:
        tokens = refresh_token(tokens["refresh_token"])
        headers["Authorization"] = f"Bearer {tokens['access_token']}"
    return headers


# 🟢 Create
def create_article(collection, data ):
    headers = get_headers()
    r = requests.post(f"{DIRECTUS_URL}/items/{collection}", headers=headers, json=data)
    r.raise_for_status()
    return r.json()


# 🔵 Read
def get_articles(collection):
    headers = get_headers()
    r = requests.get(f"{DIRECTUS_URL}/items/{collection}", headers=headers)
    r.raise_for_status()
    return r.json()


# 🟡 Update
def update_article(collection, article_id, data):
    headers = get_headers()
    r = requests.patch(f"{DIRECTUS_URL}/items/{collection}/{article_id}", headers=headers, json=data)
    r.raise_for_status()
    return r.json()

# 🔴 Delete
def delete_article(collection, article_id):
    headers = get_headers()
    r = requests.delete(f"{DIRECTUS_URL}/items/{collection}/{article_id}", headers=headers)
    r.raise_for_status()
    return {"status": "deleted"}


def get_user_by_telegram(account_telegram: str):
    try:
        
        """tokens = get_tokens()
        headers = {
            "Authorization": f"Bearer {tokens['access_token']}",
        }
        params = {
            "filter[account_telegram][_eq]": account_telegram
        }"""

        headers = get_headers()

        #response = requests.get(f"{DIRECTUS_URL}/items/users", headers=headers, params=params)
        response = requests.get(f"{DIRECTUS_URL}/items/users", headers=headers)
        response.raise_for_status()

        data = response.json()
        if data.get("data"):
            _user = [u for u in data["data"] if u.get("account_telegram") == account_telegram][0]
            return _user  # Retourne le premier utilisateur trouvé
        return None
    except Exception as e:
        print("Erreur lors de la récupération de l'utilisateur :", e)
        return None



# === REQUÊTE AUTHENTIFIÉE AVEC GESTION DU RENOUVELLEMENT ===
def directus_get(endpoint):
    tokens = get_tokens()
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    response = requests.get(f"{DIRECTUS_URL}/{endpoint}", headers=headers)

    if response.status_code == 401:
        # Access token expiré → on utilise le refresh token
        tokens = refresh_token(tokens["refresh_token"])
        headers["Authorization"] = f"Bearer {tokens['access_token']}"
        response = requests.get(f"{DIRECTUS_URL}/{endpoint}", headers=headers)

    response.raise_for_status()
    return response.json()




# ▶️ Exécution
if __name__ == "__main__":
    h = get_headers()
    print(h)
