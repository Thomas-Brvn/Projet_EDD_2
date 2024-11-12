import requests
from dotenv import load_dotenv
import os
from pymongo import MongoClient

# Récupérer l'API_KEY et le QUERY depuis les variables d'environnement
api_key = os.getenv('API_KEY_fin')
query = os.getenv('QUERY_fin')
api_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={query}&apikey={api_key}&outputsize=compact'

'''
class BelibAPIClient:
    def __init__(self, api_url):
        self.api_url = api_url
 
    def fetch_data(self, limit=20):
        try:
            # Afficher l'URL de l'API et la limite des enregistrements
            print(f"Récupération des données depuis l'API : {self.api_url} avec une limite : {limit}")
            response = requests.get(self.api_url, params={'limit': limit})
            # Afficher le code de statut de la réponse
            print(f"Code de statut de la réponse : {response.status_code}")
            # Afficher le contenu de la réponse
            print(f"Contenu de la réponse : {response.text}")
            if response.status_code == 200:
                json_data = response.json()
                total_records = json_data.get('total_count', None)  # Obtenir le nombre total d'enregistrements
                records = json_data.get('results', [])  # Obtenir les résultats
                return records, total_records
            else:
                print(f"Échec de la récupération des données. Code de statut : {response.status_code}, Réponse : {response.text}")
                return None, None
        except Exception as e:
            print(f"Une erreur s'est produite lors de la récupération des données de l'API : {e}")
            return None, None
 
class MongoDBPipeline:
    def __init__(self):
        # Charger les variables d'environnement
        load_dotenv()
 
        # Récupérer les informations de connexion depuis les variables d'environnement
        self.username = os.getenv('MONGO_USERNAME')
        self.password = os.getenv('MONGO_PASSWORD')
        self.dbname = os.getenv('MONGO_DBNAME')
        self.mongodb_uri = os.getenv('MONGO_URI')
 
        # Vérifier si les informations de connexion sont disponibles
        if not self.username or not self.password or not self.dbname or not self.mongodb_uri:
            raise ValueError("Les informations de connexion MongoDB sont manquantes dans les variables d'environnement.")
 
        # Initialiser la connexion à MongoDB
        self.client = MongoClient(self.mongodb_uri)
        self.db = self.client[self.dbname]
        self.collection = self.db['belib']  # Nom de la collection
 
    def insert_data_to_mongodb(self, data):
        try:
            if data:
                # Insérer les données dans MongoDB
                result = self.collection.insert_many(data)
                print(f"{len(result.inserted_ids)} documents insérés dans MongoDB.")
            else:
                print("Aucune donnée à insérer.")
        except Exception as e:
            print(f"Erreur lors de l'insertion des données dans MongoDB : {e}")
 
    def close_connection(self):
        # Fermer la connexion MongoDB
        self.client.close()
        print("Connexion à MongoDB fermée.")
 
def main():
    # Charger les variables d'environnement
    load_dotenv()
 
    # Récupérer l'URL de l'API depuis le fichier .env
    api_url = os.getenv("API_URL")
    if not api_url:
        print("L'API_URL n'est pas définie dans le fichier .env.")
        return
 
    # Créer une instance du client API
    api_client = BelibAPIClient(api_url)
 
    # Récupérer les données depuis l'API
    data, total_records = api_client.fetch_data(limit=50)  # Exemple avec une limite de 50 enregistrements
    if data:
        print(f"{len(data)} enregistrements récupérés avec succès depuis l'API.")
        if total_records is not None:
            print(f"Total des enregistrements dans l'API : {total_records}")
        else:
            print("Le nombre total d'enregistrements n'est pas disponible.")
        # Initialiser le pipeline MongoDB
        mongo_pipeline = MongoDBPipeline()
 
        # Insérer les données dans MongoDB
        mongo_pipeline.insert_data_to_mongodb(data)
 
        # Fermer la connexion MongoDB
        mongo_pipeline.close_connection()
    else:
        print("Échec de la récupération des données depuis l'API.")
 
if __name__ == "__main__":
    main()
'''

class BelibAPIClient:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self, limit=20):
        try:
            # Afficher l'URL de l'API et la limite des enregistrements
            print(f"Récupération des données depuis l'API : {self.api_url} avec une limite : {limit}")
            response = requests.get(self.api_url)
            # Afficher le code de statut de la réponse
            print(f"Code de statut de la réponse : {response.status_code}")
            # Afficher le contenu de la réponse
            print(f"Contenu de la réponse : {response.text}")
            if response.status_code == 200:
                json_data = response.json()
                records = json_data.get('Time Series (Daily)', [])  # Obtenir les articles depuis l'API
                return records
            else:
                print(f"Échec de la récupération des données. Code de statut : {response.status_code}, Réponse : {response.text}")
                return None
        except Exception as e:
            print(f"Une erreur s'est produite lors de la récupération des données de l'API : {e}")
            return None

class MongoDBPipeline:
    def __init__(self):
        # Charger les variables d'environnement
        load_dotenv()

        # Récupérer les informations de connexion depuis les variables d'environnement
        self.username = os.getenv('MONGO_USERNAME')
        self.password = os.getenv('MONGO_PASSWORD')
        self.dbname = os.getenv('MONGO_DBNAME')
        self.mongodb_uri = os.getenv('MONGO_URI')

        # Vérifier si les informations de connexion sont disponibles
        if not self.username or not self.password or not self.dbname or not self.mongodb_uri:
            raise ValueError("Les informations de connexion MongoDB sont manquantes dans les variables d'environnement.")

        # Initialiser la connexion à MongoDB
        self.client = MongoClient(self.mongodb_uri)
        self.db = self.client[self.dbname]
        self.collection = self.db['data_finance']  # Nom de la collection

    def insert_data_to_mongodb(self, data):
        try:
            if data:
                # Trouver la dernière date dans la base de données
                last_date = self.collection.find_one(sort=[("date", -1)])
                if last_date:
                    last_date = last_date["date"]

                # Transformer chaque élément de la liste data en un document MongoDB
                documents = []
                for date, values in data.items():
                    if date > last_date:
                        document = {
                            "symbol": os.getenv('QUERY_fin'),
                            "date": date,
                            "open": values["1. open"],
                            "high": values["2. high"],
                            "low": values["3. low"],
                            "close": values["4. close"],
                            "volume": values["5. volume"]
                        }
                        documents.append(document)

                # Insérer les documents dans MongoDB
                if documents:
                    result = self.collection.insert_many(documents)
                    print(f"{len(result.inserted_ids)} documents insérés dans MongoDB.")
                else:
                    print("Aucune nouvelle donnée à insérer.")
            else:
                print("Aucune donnée à insérer.")
        except Exception as e:
            print(f"Erreur lors de l'insertion des données dans MongoDB : {e}")

    def close_connection(self):
        # Fermer la connexion MongoDB
        self.client.close()
        print("Connexion à MongoDB fermée.")

def main():
    # Charger les variables d'environnement
    load_dotenv()

    # Récupérer l'API_KEY et QUERY depuis le fichier .env
    api_key = os.getenv('API_KEY_fin')
    query = os.getenv('QUERY_fin')
    if not api_key or not query:
        print("L'API_KEY ou QUERY n'est pas définie dans le fichier .env.")
        return

    # Construire l'URL de l'API
    api_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={query}&apikey={api_key}&outputsize=compact'

    # Créer une instance du client API
    api_client = BelibAPIClient(api_url)

    # Récupérer les données depuis l'API
    data = api_client.fetch_data(limit=50)  # Exemple avec une limite de 50 enregistrements
    if data:
        print(f"{len(data)} enregistrements récupérés avec succès depuis l'API.")

        # Initialiser le pipeline MongoDB
        mongo_pipeline = MongoDBPipeline()

        # Insérer les données dans MongoDB
        mongo_pipeline.insert_data_to_mongodb(data)

        # Fermer la connexion MongoDB
        mongo_pipeline.close_connection()
    else:
        print("Échec de la récupération des données depuis l'API.")

if __name__ == "__main__":
    main()
