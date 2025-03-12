import streamlit as st
from py2neo import Graph

# Connexion à Neo4J
graph = Graph("bolt://localhost:7687", auth=("neo4j", "PhPlus2425"))

# Titre de l'application
st.title("Application Transverse - PharmaciePlusDB")

# Menu de navigation
option = st.sidebar.selectbox(
    "Choisissez une option",
    ["Vérifier la disponibilité", "Suivre les ventes", "Déclencher des commandes"]
)

if option == "Vérifier la disponibilité":
    st.header("Vérifier la disponibilité d'un médicament")
    nom_medicament = st.text_input("Entrez le nom du médicament:")
    if st.button("Vérifier"):
        query = """
        MATCH (m:Medicament {nom_commercial: $nom_medicament})-[:STOCK]->(s:Stock)
        RETURN m.nom_commercial, s.quantite_actuelle, s.seuil_alerte;
        """
        result = graph.run(query, nom_medicament=nom_medicament).data()
        if result:
            st.write(f"Disponibilité du médicament {nom_medicament}:")
            for row in result:
                st.write(f"  Quantité en stock: {row['s.quantite_actuelle']}")
                st.write(f"  Seuil d'alerte: {row['s.seuil_alerte']}")
        else:
            st.write(f"Aucun médicament trouvé avec le nom {nom_medicament}.")

elif option == "Suivre les ventes":
    st.header("Suivre les ventes en temps réel")
    if st.button("Afficher les ventes"):
        query = """
        MATCH (v:Vente)-[:FACTURE]->(f:Facture)
        RETURN v.id_vente, v.date_vente, v.quantite_vendue, f.montant_total, f.statut_facture;
        """
        result = graph.run(query).data()
        if result:
            st.write("Ventes récentes:")
            for row in result:
                st.write(f"  ID Vente: {row['v.id_vente']}")
                st.write(f"  Date: {row['v.date_vente']}")
                st.write(f"  Quantité vendue: {row['v.quantite_vendue']}")
                st.write(f"  Montant total: {row['f.montant_total']}")
                st.write(f"  Statut facture: {row['f.statut_facture']}")
                st.write("-" * 30)
        else:
            st.write("Aucune vente trouvée.")

elif option == "Déclencher des commandes":
    st.header("Déclencher des commandes automatiques")
    if st.button("Vérifier les ruptures de stock"):
        query = """
        MATCH (m:Medicament)-[:STOCK]->(s:Stock)
        WHERE s.quantite_actuelle < s.seuil_alerte
        RETURN m.nom_commercial, s.quantite_actuelle, s.seuil_alerte;
        """
        result = graph.run(query).data()
        if result:
            st.write("Medicaments en rupture de stock:")
            for row in result:
                st.write(f"  Medicament: {row['m.nom_commercial']}")
                st.write(f"  Quantité en stock: {row['s.quantite_actuelle']}")
                st.write(f"  Seuil d'alerte: {row['s.seuil_alerte']}")
                st.write("-" * 30)
        else:
            st.write("Aucun médicament en rupture de stock.")