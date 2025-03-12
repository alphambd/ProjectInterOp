from database import MySQLDatabase, Neo4JDatabase
from injection import inject_m1_data, inject_m2_data, inject_m3_data

# Connexion à MySQL
mysql_db = MySQLDatabase(host="localhost", user="root", password="root", database="pharmacie_plus_db")
mysql_db.connect()

# Connexion à Neo4J
neo4j_db = Neo4JDatabase(uri="bolt://localhost:7687", auth=("neo4j", "PhPlus2425"))

# Injection des données
try:
    # Injection des données M1 (MySQL)
    print("Début de l'injection des données M1...")
    inject_m1_data(mysql_db, neo4j_db)
    print("Injection des données M1 terminée.")
    
    # Injection des données M2 (JSON)
    print("Début de l'injection des données M2...")
    inject_m2_data(neo4j_db)
    print("Injection des données M2 terminée.")

    test_node = neo4j_db.graph.nodes.match("Medicament", id_medicament=1).first()
    print(f"🔍 Test récupération Médicament ID 1 : {test_node}\n\n")


    # Injection des données M3 (XML)
    print("Début de l'injection des données M3...")
    inject_m3_data(neo4j_db)
    print("Injection des données M3 terminée.")

except Exception as e:
    print(f"Une erreur s'est produite lors de l'injection des données : {e}")

finally:
    # Déconnexion de MySQL
    mysql_db.disconnect()
    print("Connexion à MySQL fermée.")