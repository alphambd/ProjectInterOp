-- Suppression des tables existantes (ordre inverse pour éviter les problèmes de clés étrangères)
DROP TABLE IF EXISTS Stock;
DROP TABLE IF EXISTS Fournisseur;
DROP TABLE IF EXISTS Medicament;

-- Création de la table Médicament
CREATE TABLE IF NOT EXISTS Medicament (
    id_medicament INT PRIMARY KEY AUTO_INCREMENT,
    nom_commercial VARCHAR(255) NOT NULL,
    nom_generique VARCHAR(255),
    dosage VARCHAR(50),
    forme VARCHAR(50),
    prix_unitaire DECIMAL(10, 2),
    date_peremption DATE,
    code_CIP VARCHAR(20),
    classification_ATC VARCHAR(20),
    prescription BOOLEAN,
    fabricant VARCHAR(255)
);

-- Création de la table Stock
CREATE TABLE IF NOT EXISTS Stock (
    id_stock INT PRIMARY KEY AUTO_INCREMENT,
    id_medicament INT,
    quantite_actuelle INT,
    seuil_alerte INT,
    localisation VARCHAR(255),
    date_entree DATE,
    FOREIGN KEY (id_medicament) REFERENCES Medicament(id_medicament)
);

-- Création de la table Fournisseur
CREATE TABLE IF NOT EXISTS Fournisseur (
    id_fournisseur INT PRIMARY KEY AUTO_INCREMENT,
    nom_fournisseur VARCHAR(255) NOT NULL,
    adresse VARCHAR(255),
    telephone VARCHAR(20),
    email VARCHAR(255),
    delai_livraison INT
);

-- Insertion de données dans la table Médicament
INSERT INTO Medicament (nom_commercial, nom_generique, dosage, forme, prix_unitaire, date_peremption, code_CIP, classification_ATC, prescription, fabricant)
VALUES 
('Paracétamol 500mg', 'Paracétamol', '500mg', 'Comprimé', 2.50, '2024-12-31', '3400931234567', 'N02BE01', FALSE, 'PharmaLab'),
('Ibuprofène 400mg', 'Ibuprofène', '400mg', 'Comprimé', 3.00, '2025-06-30', '3400936543210', 'M01AE01', FALSE, 'MediCorp'),
('Amoxicilline 1g', 'Amoxicilline', '1g', 'Gélule', 5.00, '2024-09-15', '3400939876543', 'J01CA04', TRUE, 'PharmaLab');

-- Insertion de données dans la table Stock
INSERT INTO Stock (id_medicament, quantite_actuelle, seuil_alerte, localisation, date_entree)
VALUES 
(1, 100, 50, 'Rayon A', '2023-10-01'),
(2, 75, 30, 'Rayon B', '2023-09-15'),
(3, 50, 20, 'Rayon C', '2023-08-20');

-- Insertion de données dans la table Fournisseur
INSERT INTO Fournisseur (nom_fournisseur, adresse, telephone, email, delai_livraison)
VALUES 
('PharmaSupply', '10 Rue des Fournisseurs', '0987654321', 'contact@pharmasupply.com', 5),
('MediCorp', '25 Avenue des Médicaments', '0123456789', 'info@medicorp.com', 7),
('HealthPlus', '15 Boulevard de la Santé', '0345678912', 'support@healthplus.com', 3);

-- Requête pour vérifier les données insérées
SELECT * FROM Medicament;
SELECT * FROM Stock;
SELECT * FROM Fournisseur;