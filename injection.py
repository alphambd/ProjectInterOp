from database import MySQLDatabase, Neo4JDatabase, JSONDatabase, XMLDatabase
from models import Medicament, Stock, Client, Vente, Facture, Commande, Fournisseur


def inject_m1_data(mysql_db, neo4j_db):
    # Récupérer les médicaments et les stocks depuis MySQL
    medicaments = mysql_db.fetch_medicaments()
    stocks = mysql_db.fetch_stocks()

    # Injecter les médicaments dans Neo4J
    for med in medicaments:
        medicament_node = neo4j_db.create_node("Medicament", **med.__dict__)
        print(f"✅ Médicament inséré id_medicament : {med.id_medicament} - {med.nom_generique}")  # Vérification

        # Vérifier immédiatement s'il est bien stocké
        check_node = neo4j_db.graph.nodes.match("Medicament", id_medicament=med.id_medicament).first()
        if check_node:
            print(f"🔎 Vérification : Médicament ID {med.id_medicament} trouvé dans Neo4J ✅")
        else:
            print(f"⚠️ Médicament ID {med.id_medicament} introuvable dans Neo4J ❌")

        # Injecter les stocks associés
        for stock in stocks:
            if stock.id_medicament == med.id_medicament:
                stock_node = neo4j_db.create_node("Stock", **stock.__dict__)
                print(f"  📦 Stock ajouté pour Médicament ID {stock.id_medicament} | Quantité : {stock.quantite_actuelle}")  # Vérification

                neo4j_db.create_relationship(
                    medicament_node, "STOCK", stock_node,
                    quantite_disponible=stock.quantite_actuelle,
                    date_derniere_mise_a_jour="2023-10-01"
                )

def inject_m2_data(neo4j_db):
    json_db = JSONDatabase()
    clients = json_db.load_clients()
    ventes = json_db.load_ventes()
    factures = json_db.load_factures()

    # Injecter les clients dans Neo4J
    for client in clients:
        client_node = neo4j_db.create_node("Client", **client.__dict__)
        print(f"Client inséré id_client : {client.id_client}")  # Vérification

    # Injecter les ventes dans Neo4J
    for vente in ventes:
        vente_node = neo4j_db.create_node("Vente", **vente.__dict__)

        # Vérifier si le client existe
        client_node = neo4j_db.graph.nodes.match("Client", id_client=vente.id_client).first()
        if client_node is None:
            print(f"⚠️ Attention : Le client avec l'ID {vente.id_client} n'existe pas dans Neo4J.")
            continue

        neo4j_db.create_relationship(client_node, "ACHETE_PAR", vente_node, date_achat=vente.date_vente, mode_paiement=vente.methode_paiement)

    # Injecter les factures dans Neo4J
    for facture in factures:
        facture_node = neo4j_db.create_node("Facture", **facture.__dict__)

        # Vérifier si la vente existe
        vente_node = neo4j_db.graph.nodes.match("Vente", id_vente=facture.id_vente).first()
        if vente_node is None:
            print(f"⚠️ Attention : La vente avec l'ID {facture.id_vente} n'existe pas dans Neo4J.")
            continue

        neo4j_db.create_relationship(vente_node, "FACTURE", facture_node, date_facturation=facture.date_emission, montant_facture=facture.montant_total)



def inject_m3_data(neo4j_db):
    xml_db = XMLDatabase()
    commandes = xml_db.load_commandes()
    fournisseurs = xml_db.load_fournisseurs()

    # Injecter les fournisseurs dans Neo4J
    for fournisseur in fournisseurs:
        fournisseur_node = neo4j_db.create_node("Fournisseur", **fournisseur.__dict__)
        print(f"Fournisseur inséré id_fournisseur : {fournisseur.id_fournisseur}")  # Vérification

    # Injecter les commandes dans Neo4J
    for commande in commandes:
        commande_node = neo4j_db.create_node("Commande", **commande.__dict__)

        # Vérifier si le médicament existe
        #medicament_node = neo4j_db.graph.nodes.match("Medicament", id_medicament=commande.id_medicament).first()
        #medicament_node = neo4j_db.graph.nodes.match("Medicament", id_medicament=str(commande.id_medicament)).first()
        medicament_node = neo4j_db.graph.nodes.match("Medicament", id_medicament=int(commande.id_medicament)).first()
        if medicament_node is None:
            print(f"⚠️ Attention : Le médicament avec l'ID {commande.id_medicament} n'existe pas dans Neo4J.")
            continue

        # Vérifier si le fournisseur existe
        fournisseur_node = neo4j_db.graph.nodes.match("Fournisseur", id_fournisseur=commande.id_fournisseur).first()
        if fournisseur_node is None:
            print(f"⚠️ Attention : Le fournisseur avec l'ID {commande.id_fournisseur} n'existe pas dans Neo4J.")
            continue

        neo4j_db.create_relationship(commande_node, "COMMANDE", medicament_node, quantite_commandee=commande.quantite_commandee)
        neo4j_db.create_relationship(commande_node, "LIVRE_PAR", fournisseur_node, date_livraison="2023-10-10", statut_livraison="Livré")
