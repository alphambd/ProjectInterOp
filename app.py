import streamlit as st
import pandas as pd
from database import Neo4JDatabase

# Connexion à Neo4J
neo4j_db = Neo4JDatabase(uri="bolt://localhost:7687", auth=("neo4j", "PhPlus2425"))

# Titre de l'application
st.title("PharmaciePlus - Suivi des Stocks et des Ventes")

# Sidebar pour la navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio(
    "Choisissez une option",
    ["Vérifier le stock", "Commandes automatiques"]
)

# Fonction pour vérifier le stock d'un médicament
if option == "Vérifier le stock":
    st.header("Vérifier la disponibilité d'un médicament")
    nom_medicament = st.text_input("Entrez le nom du médicament", value="Ibuprofène")
    
    if st.button("Vérifier le stock"):
        result = neo4j_db.check_stock(nom_medicament)
        if result:
            st.write("### Résultat :")
            df = pd.DataFrame(result)
            st.dataframe(df)
        else:
            st.error(f"Aucun résultat trouvé pour le médicament : {nom_medicament}")

# Fonction pour suivre les ventes
elif option == "Suivi des ventes":
    st.header("Suivi des ventes en temps réel")
    
    if st.button("Rafraîchir les données"):
        result = neo4j_db.get_sales()
        if result:
            st.write("### Dernières ventes :")
            df = pd.DataFrame(result)
            st.dataframe(df)
        else:
            st.warning("Aucune vente trouvée.")

# Fonction pour déclencher des commandes automatiques
elif option == "Commandes automatiques":
    st.header("Commandes automatiques en cas de rupture de stock")
    
    if st.button("Vérifier les stocks faibles"):
        result = neo4j_db.check_low_stock()
        if result:
            st.write("### Médicaments en rupture de stock :")
            df = pd.DataFrame(result)
            st.dataframe(df)

            # Formulaire pour déclencher une commande
            with st.form("Commande"):
                medicament_id = st.number_input("ID du médicament", min_value=1, value=1)
                quantite_commandee = st.number_input("Quantité à commander", min_value=1, value=10)
                fournisseur_id = st.number_input("ID du fournisseur", min_value=1, value=1)
                if st.form_submit_button("Déclencher la commande"):
                    order_result = neo4j_db.trigger_order(medicament_id, quantite_commandee, fournisseur_id)
                    if order_result:
                        st.success("Commande déclenchée avec succès !")
                        # Rafraîchir les données après la commande
                        updated_stock = neo4j_db.check_stock_by_id(medicament_id)
                        if updated_stock:
                            st.write("### Stock mis à jour :")
                            st.dataframe(pd.DataFrame(updated_stock))
                    else:
                        st.error("Erreur lors de la création de la commande.")
        else:
            st.success("Aucun médicament en rupture de stock.")