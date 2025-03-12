from decimal import Decimal

class User:
    def __init__(self, id_user, nom, prenom, email, telephone):
        self.id_user = id_user
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.telephone = telephone

class Client(User):
    def __init__(self, id_client, nom, prenom, email, telephone, numero_secu, adresse):
        super().__init__(id_client, nom, prenom, email, telephone)
        self.id_client = id_client  # Ajout explicite de l'attribut
        self.numero_secu = numero_secu
        self.adresse = adresse

class Medicament:
    def __init__(self, id_medicament, nom_commercial, nom_generique, dosage, forme, prix_unitaire, date_peremption, code_CIP, classification_ATC, prescription, fabricant):
        self.id_medicament = id_medicament
        self.nom_commercial = nom_commercial
        self.nom_generique = nom_generique
        self.dosage = dosage
        self.forme = forme
        self.prix_unitaire = float(prix_unitaire) if isinstance(prix_unitaire, Decimal) else prix_unitaire
        self.date_peremption = date_peremption
        self.code_CIP = code_CIP
        self.classification_ATC = classification_ATC
        self.prescription = prescription
        self.fabricant = fabricant

class Stock:
    def __init__(self, id_stock, id_medicament, quantite_actuelle, seuil_alerte, localisation, date_entree):
        self.id_stock = id_stock
        self.id_medicament = id_medicament
        self.quantite_actuelle = quantite_actuelle
        self.seuil_alerte = seuil_alerte
        self.localisation = localisation
        self.date_entree = date_entree

class Vente:
    def __init__(self, id_vente, date_vente, heure_vente, quantite_vendue, methode_paiement, id_client):
        self.id_vente = id_vente
        self.date_vente = date_vente
        self.heure_vente = heure_vente
        self.quantite_vendue = quantite_vendue
        self.methode_paiement = methode_paiement
        self.id_client = id_client

class Facture:
    def __init__(self, id_facture, montant_total, date_emission, statut_facture, reduction_appliquee, id_vente):
        self.id_facture = id_facture
        self.montant_total = montant_total
        self.date_emission = date_emission
        self.statut_facture = statut_facture
        self.reduction_appliquee = reduction_appliquee
        self.id_vente = id_vente

class Commande:
    def __init__(self, id_commande, date_commande, statut, quantite_commandee, urgence, id_medicament, id_fournisseur):
        self.id_commande = id_commande
        self.date_commande = date_commande
        self.statut = statut
        self.quantite_commandee = quantite_commandee
        self.urgence = urgence
        self.id_medicament = id_medicament
        self.id_fournisseur = id_fournisseur

class Fournisseur:
    def __init__(self, id_fournisseur, nom_fournisseur, adresse, telephone, email, delai_livraison):
        self.id_fournisseur = id_fournisseur
        self.nom_fournisseur = nom_fournisseur
        self.adresse = adresse
        self.telephone = telephone
        self.email = email
        self.delai_livraison = delai_livraison