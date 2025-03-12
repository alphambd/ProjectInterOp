import mysql.connector  # Importation ajoutée
from py2neo import Graph, Node, Relationship
from neo4j import GraphDatabase
import json
import xml.etree.ElementTree as ET
import os
from models import Medicament, Stock, Client, Vente, Facture, Commande, Fournisseur

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

class Neo4JDatabase:
    def __init__(self, uri, auth):
        self.graph = Graph(uri, auth=auth)

    def create_node(self, label, **properties):
        node = Node(label, **properties)
        self.graph.create(node)
        return node

    def create_relationship(self, start_node, relationship_type, end_node, **properties):
        relationship = Relationship(start_node, relationship_type, end_node, **properties)
        self.graph.create(relationship)
        return relationship    


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