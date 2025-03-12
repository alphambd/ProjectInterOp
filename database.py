import mysql.connector
from neo4j import GraphDatabase
import json
import xml.etree.ElementTree as ET
import os
from models import Medicament, Stock, Client, Vente, Facture, Commande, Fournisseur

# Connexion à MySQL
class MySQLDatabase:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def fetch_medicaments(self):
        self.cursor.execute("SELECT * FROM Medicament")
        return [Medicament(*row) for row in self.cursor.fetchall()]

    def fetch_stocks(self):
        self.cursor.execute("SELECT * FROM Stock")
        return [Stock(*row) for row in self.cursor.fetchall()]

# Connexion à Neo4J
class Neo4JDatabase:
    def __init__(self, uri, auth):
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def close(self):
        self.driver.close()

    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return result.data()

    def check_stock(self, nom_medicament):
        query = """
        MATCH (m:Medicament {nom_generique: $nom_medicament})-[:STOCK]->(s:Stock)
        RETURN m.nom_generique AS nom, s.quantite_actuelle AS quantite, s.seuil_alerte AS seuil
        """
        return self.run_query(query, {"nom_medicament": nom_medicament})
    
    def update_stock(self, medicament_id, quantite_ajoutee):
        query = """
        MATCH (m:Medicament {id_medicament: $medicament_id})-[:STOCK]->(s:Stock)
        SET s.quantite_actuelle = s.quantite_actuelle + $quantite_ajoutee
        RETURN s.quantite_actuelle AS nouvelle_quantite
        """
        return self.run_query(query, {
            "medicament_id": int(medicament_id),
            "quantite_ajoutee": int(quantite_ajoutee)
        })

    def check_stock_by_id(self, medicament_id):
        query = """
        MATCH (m:Medicament {id_medicament: $medicament_id})-[:STOCK]->(s:Stock)
        RETURN m.nom_generique AS nom, s.quantite_actuelle AS quantite, s.seuil_alerte AS seuil
        """
        return self.run_query(query, {"medicament_id": int(medicament_id)})

    def get_sales(self):
        query = """
        MATCH (v:Vente)-[:ACHETE_PAR]->(c:Client)
        RETURN v.id_vente AS id, v.date_vente AS date, v.quantite_vendue AS quantite, c.nom AS client
        """
        return self.run_query(query)

    def check_low_stock(self):
        query = """
        MATCH (m:Medicament)-[:STOCK]->(s:Stock)
        WHERE s.quantite_actuelle <= s.seuil_alerte
        RETURN m.nom_generique AS nom, s.quantite_actuelle AS quantite, s.seuil_alerte AS seuil
        """
        return self.run_query(query)

    def trigger_order(self, medicament_id, quantite_commandee, fournisseur_id):
        # Créer la commande
        query = """
        MATCH (m:Medicament {id_medicament: $medicament_id}), (f:Fournisseur {id_fournisseur: $fournisseur_id})
        CREATE (c:Commande {id_commande: randomUUID(), date_commande: date(), quantite_commandee: $quantite_commandee, statut: 'En cours'})
        CREATE (c)-[:COMMANDE]->(m)
        CREATE (c)-[:LIVRE_PAR]->(f)
        RETURN c
        """
        result = self.run_query(query, {
            "medicament_id": int(medicament_id),
            "quantite_commandee": int(quantite_commandee),
            "fournisseur_id": int(fournisseur_id)
        })

        # Mettre à jour le stock
        if result:
            self.update_stock(medicament_id, quantite_commandee)
        
        return result

# Gestion des fichiers JSON
class JSONDatabase:
    def __init__(self, base_dir="data/json"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def save_vente(self, vente):
        vente_dir = os.path.join(self.base_dir, "ventes")
        os.makedirs(vente_dir, exist_ok=True)
        file_path = os.path.join(vente_dir, f"vente_{vente.id_vente}.json")
        with open(file_path, "w") as f:
            json.dump(vente.__dict__, f, indent=4)

    def save_facture(self, facture):
        facture_dir = os.path.join(self.base_dir, "factures")
        os.makedirs(facture_dir, exist_ok=True)
        file_path = os.path.join(facture_dir, f"facture_{facture.id_facture}.json")
        with open(file_path, "w") as f:
            json.dump(facture.__dict__, f, indent=4)

    def save_client(self, client):
        client_dir = os.path.join(self.base_dir, "clients")
        os.makedirs(client_dir, exist_ok=True)
        file_path = os.path.join(client_dir, f"client_{client.id_client}.json")
        with open(file_path, "w") as f:
            json.dump(client.__dict__, f, indent=4)

    def load_ventes(self):
        vente_dir = os.path.join(self.base_dir, "ventes")
        ventes = []
        for filename in os.listdir(vente_dir):
            if filename.endswith(".json"):
                with open(os.path.join(vente_dir, filename), "r") as f:
                    data = json.load(f)
                    ventes.append(Vente(**data))
        return ventes

    def load_factures(self):
        facture_dir = os.path.join(self.base_dir, "factures")
        factures = []
        for filename in os.listdir(facture_dir):
            if filename.endswith(".json"):
                with open(os.path.join(facture_dir, filename), "r") as f:
                    data = json.load(f)
                    factures.append(Facture(**data))
        return factures

    def load_clients(self):
        client_dir = os.path.join(self.base_dir, "clients")
        clients = []
        for filename in os.listdir(client_dir):
            if filename.endswith(".json"):
                with open(os.path.join(client_dir, filename), "r") as f:
                    data = json.load(f)
                    clients.append(Client(**data))
        return clients

# Gestion des fichiers XML
class XMLDatabase:
    def __init__(self, base_dir="data/xml"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def save_commande(self, commande):
        commande_dir = os.path.join(self.base_dir, "commandes")
        os.makedirs(commande_dir, exist_ok=True)
        file_path = os.path.join(commande_dir, f"commande_{commande.id_commande}.xml")
        root = ET.Element("Commande")
        for key, value in commande.__dict__.items():
            ET.SubElement(root, key).text = str(value)
        tree = ET.ElementTree(root)
        tree.write(file_path, encoding="utf-8", xml_declaration=True)

    def save_fournisseur(self, fournisseur):
        fournisseur_dir = os.path.join(self.base_dir, "fournisseurs")
        os.makedirs(fournisseur_dir, exist_ok=True)
        file_path = os.path.join(fournisseur_dir, f"fournisseur_{fournisseur.id_fournisseur}.xml")
        root = ET.Element("Fournisseur")
        for key, value in fournisseur.__dict__.items():
            ET.SubElement(root, key).text = str(value)
        tree = ET.ElementTree(root)
        tree.write(file_path, encoding="utf-8", xml_declaration=True)

    def load_commandes(self):
        commande_dir = os.path.join(self.base_dir, "commandes")
        commandes = []
        for filename in os.listdir(commande_dir):
            if filename.endswith(".xml"):
                tree = ET.parse(os.path.join(commande_dir, filename))
                root = tree.getroot()
                data = {elem.tag: elem.text for elem in root}
                commandes.append(Commande(**data))
        return commandes

    def load_fournisseurs(self):
        fournisseur_dir = os.path.join(self.base_dir, "fournisseurs")
        fournisseurs = []
        for filename in os.listdir(fournisseur_dir):
            if filename.endswith(".xml"):
                tree = ET.parse(os.path.join(fournisseur_dir, filename))
                root = tree.getroot()
                data = {elem.tag: elem.text for elem in root}
                fournisseurs.append(Fournisseur(**data))
        return fournisseurs