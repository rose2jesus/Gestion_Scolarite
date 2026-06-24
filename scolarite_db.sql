-- ============================================================
-- SIGS - Système d'Information de Gestion de Scolarité
-- Script SQL : Création de la base et insertion des données
-- USSEIN | L3 Informatique | 2024-2025
-- ============================================================

-- Création et sélection de la base
DROP DATABASE IF EXISTS scolarite_db;
CREATE DATABASE scolarite_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE scolarite_db;

-- ============================================================
-- TABLE : enseignants
-- ============================================================
CREATE TABLE enseignants (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    matricule   VARCHAR(20)  UNIQUE NOT NULL,
    nom         VARCHAR(100) NOT NULL,
    prenom      VARCHAR(100) NOT NULL,
    email       VARCHAR(150) UNIQUE,
    telephone   VARCHAR(20),
    specialite  VARCHAR(100),
    grade       VARCHAR(50),
    statut      ENUM('Permanent','Vacataire') DEFAULT 'Permanent'
);

-- ============================================================
-- TABLE : etudiants
-- ============================================================
CREATE TABLE etudiants (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    matricule        VARCHAR(20)  UNIQUE NOT NULL,
    nom              VARCHAR(100) NOT NULL,
    prenom           VARCHAR(100) NOT NULL,
    date_naissance   DATE,
    email            VARCHAR(150) UNIQUE,
    telephone        VARCHAR(20),
    filiere          VARCHAR(50),
    niveau           VARCHAR(20),
    annee_inscription YEAR
);

-- ============================================================
-- TABLE : modules
-- ============================================================
CREATE TABLE modules (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    code            VARCHAR(20)  UNIQUE NOT NULL,
    intitule        VARCHAR(200) NOT NULL,
    credits         INT          DEFAULT 3,
    volume_horaire  INT          DEFAULT 30,
    filiere         VARCHAR(50),
    niveau          VARCHAR(20),
    semestre        VARCHAR(10),
    enseignant_id   INT,
    FOREIGN KEY (enseignant_id) REFERENCES enseignants(id)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- ============================================================
-- TABLE : evaluations
-- ============================================================
CREATE TABLE evaluations (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    etudiant_id      INT NOT NULL,
    module_id        INT NOT NULL,
    type_eval        ENUM('CC','TP','Examen','Rattrapage') NOT NULL,
    note             DECIMAL(5,2) CHECK (note >= 0 AND note <= 20),
    coefficient      DECIMAL(3,1) DEFAULT 1.0,
    date_eval        DATE,
    semestre         VARCHAR(10),
    annee_academique VARCHAR(10),
    FOREIGN KEY (etudiant_id) REFERENCES etudiants(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (module_id) REFERENCES modules(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================================
-- INSERTION DES DONNÉES DE TEST
-- ============================================================

-- Enseignants (3 avec grades différents)
INSERT INTO enseignants (matricule, nom, prenom, email, telephone, specialite, grade, statut) VALUES
('ENS001', 'DIALLO',  'Mamadou',   'mdiallo@ussein.sn',  '771234567', 'Informatique',        'Maître de Conférences', 'Permanent'),
('ENS002', 'SARR',    'Fatou',     'fsarr@ussein.sn',    '772345678', 'Mathématiques',       'Professeur Titulaire',  'Permanent'),
('ENS003', 'NDIAYE',  'Ibrahima',  'indiaye@ussein.sn',  '773456789', 'Réseaux & Systèmes', 'Assistant',             'Vacataire');

-- Étudiants (5 de filières et niveaux différents)
INSERT INTO etudiants (matricule, nom, prenom, date_naissance, email, telephone, filiere, niveau, annee_inscription) VALUES
('ETU2024001', 'BA',       'Aminata',  '2002-03-15', 'aba@etud.ussein.sn',   '774111111', 'Informatique', 'L3', 2022),
('ETU2024002', 'FALL',     'Ousmane',  '2001-07-22', 'ofall@etud.ussein.sn', '774222222', 'MPI',          'L2', 2023),
('ETU2024003', 'GUEYE',    'Mariama',  '2003-01-10', 'mgueye@etud.ussein.sn','774333333', 'AgroTIC',      'L1', 2024),
('ETU2024004', 'DIOP',     'Cheikh',   '2000-11-05', 'cdiop@etud.ussein.sn', '774444444', 'Informatique', 'L3', 2022),
('ETU2024005', 'MBAYE',    'Rokhaya',  '2002-06-28', 'rmbaye@etud.ussein.sn','774555555', 'MPI',          'L2', 2023);

-- Modules (5 couvrant 2 semestres)
INSERT INTO modules (code, intitule, credits, volume_horaire, filiere, niveau, semestre, enseignant_id) VALUES
('INF301', 'Programmation Python 2',          4, 45, 'Informatique', 'L3', 'S5', 1),
('INF302', 'Base de Données Avancées',        3, 30, 'Informatique', 'L3', 'S5', 1),
('MAT201', 'Algèbre Linéaire',               3, 30, 'MPI',          'L2', 'S3', 2),
('INF303', 'Réseaux Informatiques',           3, 30, 'Informatique', 'L3', 'S6', 3),
('AGR101', 'Introduction à l\'Agriculture Numérique', 2, 20, 'AgroTIC', 'L1', 'S1', 2);

-- Évaluations (10 de types variés)
INSERT INTO evaluations (etudiant_id, module_id, type_eval, note, coefficient, date_eval, semestre, annee_academique) VALUES
(1, 1, 'CC',     14.50, 1.0, '2025-01-15', 'S5', '2024-2025'),
(1, 1, 'Examen', 16.00, 2.0, '2025-02-10', 'S5', '2024-2025'),
(1, 2, 'CC',      8.50, 1.0, '2025-01-20', 'S5', '2024-2025'),
(2, 3, 'CC',     12.00, 1.0, '2025-01-18', 'S3', '2024-2025'),
(2, 3, 'Examen', 11.00, 2.0, '2025-02-12', 'S3', '2024-2025'),
(3, 5, 'TP',     15.00, 1.0, '2025-01-25', 'S1', '2024-2025'),
(4, 1, 'CC',      7.00, 1.0, '2025-01-15', 'S5', '2024-2025'),
(4, 1, 'Examen',  9.50, 2.0, '2025-02-10', 'S5', '2024-2025'),
(4, 2, 'TP',     13.00, 1.0, '2025-01-22', 'S5', '2024-2025'),
(5, 3, 'CC',     18.00, 1.0, '2025-01-18', 'S3', '2024-2025');

-- ============================================================
-- REQUÊTES SQL DE VALIDATION (Partie A3)
-- ============================================================

-- 1. Lister tous les étudiants d'une filière donnée triés par nom
-- SELECT * FROM etudiants WHERE filiere = 'Informatique' ORDER BY nom ASC;

-- 2. Afficher la liste des modules avec le nom de l'enseignant responsable
-- SELECT m.code, m.intitule, m.credits, m.semestre,
--        CONCAT(e.nom, ' ', e.prenom) AS enseignant
-- FROM modules m
-- LEFT JOIN enseignants e ON m.enseignant_id = e.id
-- ORDER BY m.code;

-- 3. Calculer la moyenne générale d'un étudiant donné (pondérée par coefficient)
-- SELECT et.nom, et.prenom,
--        ROUND(SUM(ev.note * ev.coefficient) / SUM(ev.coefficient), 2) AS moyenne_generale
-- FROM evaluations ev
-- JOIN etudiants et ON ev.etudiant_id = et.id
-- WHERE ev.etudiant_id = 1
-- GROUP BY et.id, et.nom, et.prenom;

-- 4. Lister les étudiants ayant une note inférieure à 10 dans au moins un module
-- SELECT DISTINCT et.matricule, et.nom, et.prenom, et.filiere
-- FROM evaluations ev
-- JOIN etudiants et ON ev.etudiant_id = et.id
-- WHERE ev.note < 10
-- ORDER BY et.nom;

-- 5. Afficher le taux de réussite (notes >= 10) par module
-- SELECT m.code, m.intitule,
--        COUNT(ev.id) AS total_notes,
--        SUM(CASE WHEN ev.note >= 10 THEN 1 ELSE 0 END) AS reussites,
--        ROUND(100.0 * SUM(CASE WHEN ev.note >= 10 THEN 1 ELSE 0 END) / COUNT(ev.id), 1) AS taux_reussite
-- FROM evaluations ev
-- JOIN modules m ON ev.module_id = m.id
-- GROUP BY m.id, m.code, m.intitule
-- ORDER BY taux_reussite DESC;

SELECT 'Base de données scolarite_db créée avec succès !' AS message;
