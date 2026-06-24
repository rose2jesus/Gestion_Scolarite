import mysql.connector
from mysql.connector import Error


try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="scolarite_db"
    )
    if db.is_connected():
        print("Connexion à la base de données réussie !")
except Error as e:
    print("Échec de la connexion :", e)


curseur = db.cursor()



curseur.execute("""
    CREATE TABLE IF NOT EXISTS etudiants (
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
    )
""")

curseur.execute("""
    CREATE TABLE IF NOT EXISTS enseignants (
        id          INT AUTO_INCREMENT PRIMARY KEY,
        matricule   VARCHAR(20)  UNIQUE NOT NULL,
        nom         VARCHAR(100) NOT NULL,
        prenom      VARCHAR(100) NOT NULL,
        email       VARCHAR(150) UNIQUE,
        telephone   VARCHAR(20),
        specialite  VARCHAR(100),
        grade       VARCHAR(50),
        statut      ENUM('Permanent','Vacataire') DEFAULT 'Permanent'
    )
""")

curseur.execute("""
    CREATE TABLE IF NOT EXISTS modules (
        id             INT AUTO_INCREMENT PRIMARY KEY,
        code           VARCHAR(20)  UNIQUE NOT NULL,
        intitule       VARCHAR(200) NOT NULL,
        credits        INT DEFAULT 3,
        volume_horaire INT DEFAULT 30,
        filiere        VARCHAR(50),
        niveau         VARCHAR(20),
        semestre       VARCHAR(10),
        enseignant_id  INT,
        FOREIGN KEY (enseignant_id) REFERENCES enseignants(id)
            ON DELETE SET NULL ON UPDATE CASCADE
    )
""")

curseur.execute("""
    CREATE TABLE IF NOT EXISTS evaluations (
        id               INT AUTO_INCREMENT PRIMARY KEY,
        etudiant_id      INT NOT NULL,
        module_id        INT NOT NULL,
        type_eval        ENUM('CC','TP','Examen','Rattrapage') NOT NULL,
        note             DECIMAL(5,2) CHECK (note >= 0 AND note <= 20),
        coefficient      DECIMAL(3,1) DEFAULT 1.0,
        date_eval        DATE,
        semestre         VARCHAR(10),
        annee_academique VARCHAR(10),
        FOREIGN KEY (etudiant_id) REFERENCES etudiants(id) ON DELETE CASCADE,
        FOREIGN KEY (module_id)   REFERENCES modules(id)   ON DELETE CASCADE
    )
""")

db.commit()
print("Tables créées avec succès !")




curseur.execute("SELECT COUNT(*) FROM enseignants")
if curseur.fetchone()[0] == 0:
    enseignants = [
        ("ENS001", "DIALLO",  "Mamadou",  "mdiallo@ussein.sn",  "771234567", "Informatique",       "Maître de Conférences", "Permanent"),
        ("ENS002", "SARR",    "Fatou",    "fsarr@ussein.sn",    "772345678", "Mathématiques",      "Professeur Titulaire",  "Permanent"),
        ("ENS003", "NDIAYE",  "Ibrahima", "indiaye@ussein.sn",  "773456789", "Réseaux & Systèmes", "Assistant",             "Vacataire"),
    ]
    for ens in enseignants:
        curseur.execute("""
            INSERT INTO enseignants (matricule, nom, prenom, email, telephone, specialite, grade, statut)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, ens)
    db.commit()
    print("Enseignants de test insérés.")

curseur.execute("SELECT COUNT(*) FROM etudiants")
if curseur.fetchone()[0] == 0:
    etudiants = [
        ("ETU2024001", "DIA",    "Khadidiatou", "2002-03-15", "kdia@etud.ussein.edu.sn",    "774111111", "Informatique", "L3", 2022),
        ("ETU2024002", "FALL",  "Ousmane", "2001-07-22", "ofall@etud.ussein.edu.sn",  "774222222", "MPI",          "L2", 2023),
        ("ETU2024003", "GUEYE", "Mariama", "2003-01-10", "mgueye@etud.ussein.ed.sn", "774333333", "AgroTIC",      "L1", 2024),
        ("ETU2024004", "SYLVA",  "Rose",  "2000-11-05", "cdiop@etud.ussein.edu.sn",  "774444444", "Informatique", "L3", 2022),
        ("ETU2024005", "MBAYE", "Rokhaya", "2002-06-28", "rmbaye@etud.ussein.edu.sn", "774555555", "MPI",          "L2", 2023),
    ]
    for etud in etudiants:
        curseur.execute("""
            INSERT INTO etudiants (matricule, nom, prenom, date_naissance, email, telephone, filiere, niveau, annee_inscription)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, etud)
    db.commit()
    print("Etudiants de test insérés.")

curseur.execute("SELECT COUNT(*) FROM modules")
if curseur.fetchone()[0] == 0:
    modules = [
        ("INF301", "Programmation Python 2",                 4, 45, "Informatique", "L3", "S6", 1),
        ("INF302", "Base de Données ",               3, 30, "Informatique", "L3", "S5", 1),
        ("MAT201", "Algèbre Linéaire",                      3, 30, "MPI",          "L2", "S3", 2),
        ("INF303", "Réseaux Informatiques",                  3, 30, "Informatique", "L3", "S5", 3),
        ("AGR101", "Introduction à l'Agriculture Numérique", 2, 20, "AgroTIC",     "L1", "S1", 2),
    ]
    for mod in modules:
        curseur.execute("""
            INSERT INTO modules (code, intitule, credits, volume_horaire, filiere, niveau, semestre, enseignant_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, mod)
    db.commit()
    print("Modules de test insérés.")

curseur.execute("SELECT COUNT(*) FROM evaluations")
if curseur.fetchone()[0] == 0:
    evaluations = [
        (1, 1, "CC",     14.50, 1.0, "2025-01-15", "S5", "2024-2025"),
        (1, 1, "Examen", 16.00, 2.0, "2025-02-10", "S5", "2024-2025"),
        (1, 2, "CC",      8.50, 1.0, "2025-01-20", "S5", "2024-2025"),
        (2, 3, "CC",     12.00, 1.0, "2025-01-18", "S3", "2024-2025"),
        (2, 3, "Examen", 11.00, 2.0, "2025-02-12", "S3", "2024-2025"),
        (3, 5, "TP",     15.00, 1.0, "2025-01-25", "S1", "2024-2025"),
        (4, 1, "CC",      7.00, 1.0, "2025-01-15", "S5", "2024-2025"),
        (4, 1, "Examen",  9.50, 2.0, "2025-02-10", "S5", "2024-2025"),
        (4, 2, "TP",     13.00, 1.0, "2025-01-22", "S5", "2024-2025"),
        (5, 3, "CC",     18.00, 1.0, "2025-01-18", "S3", "2024-2025"),
    ]
    for ev in evaluations:
        curseur.execute("""
            INSERT INTO evaluations (etudiant_id, module_id, type_eval, note, coefficient, date_eval, semestre, annee_academique)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, ev)
    db.commit()
    print("Evaluations de test insérées.")



print("\n" + "="*55)
print("  REQUETES SQL DE VALIDATION (Partie A3)")
print("="*55)


print("\n1. Etudiants de la filière 'Informatique' triés par nom :")
curseur.execute("""
    SELECT matricule, nom, prenom, niveau
    FROM etudiants
    WHERE filiere = 'Informatique'
    ORDER BY nom ASC
""")
for row in curseur.fetchall():
    print("  {0} - {1} {2} - {3}".format(row[0], row[1], row[2], row[3]))


print("\n2. Modules avec leur enseignant responsable :")
curseur.execute("""
    SELECT m.code, m.intitule, m.semestre,
           CONCAT(e.nom, ' ', e.prenom) AS enseignant
    FROM modules m
    LEFT JOIN enseignants e ON m.enseignant_id = e.id
    ORDER BY m.code
""")
for row in curseur.fetchall():
    print("  {0} - {1} | S:{2} | {3}".format(row[0], row[1], row[2], row[3]))


print("\n3. Moyenne générale de l'étudiant id=1 (pondérée par coefficient) :")
curseur.execute("""
    SELECT et.nom, et.prenom,
           ROUND(SUM(ev.note * ev.coefficient) / SUM(ev.coefficient), 2) AS moyenne
    FROM evaluations ev
    JOIN etudiants et ON ev.etudiant_id = et.id
    WHERE ev.etudiant_id = 1
    GROUP BY et.id, et.nom, et.prenom
""")
for row in curseur.fetchall():
    print("  {0} {1} → Moyenne : {2} / 20".format(row[0], row[1], row[2]))


print("\n4. Etudiants ayant au moins une note inférieure à 10 :")
curseur.execute("""
    SELECT DISTINCT et.matricule, et.nom, et.prenom, et.filiere
    FROM evaluations ev
    JOIN etudiants et ON ev.etudiant_id = et.id
    WHERE ev.note < 10
    ORDER BY et.nom
""")
for row in curseur.fetchall():
    print("  {0} - {1} {2} - {3}".format(row[0], row[1], row[2], row[3]))


print("\n5. Taux de réussite (note >= 10) par module :")
curseur.execute("""
    SELECT m.code, m.intitule,
           COUNT(ev.id) AS total,
           SUM(CASE WHEN ev.note >= 10 THEN 1 ELSE 0 END) AS reussites,
           ROUND(100.0 * SUM(CASE WHEN ev.note >= 10 THEN 1 ELSE 0 END) / COUNT(ev.id), 1) AS taux
    FROM evaluations ev
    JOIN modules m ON ev.module_id = m.id
    GROUP BY m.id, m.code, m.intitule
    ORDER BY taux DESC
""")
for row in curseur.fetchall():
    print("  {0} - {1} : {2}% ({3}/{4})".format(row[0], row[1], row[4], row[3], row[2]))

print("\n" + "="*55 + "\n")


def ajouter_etudiant(matricule, nom, prenom, date_naissance, email,
                     telephone, filiere, niveau, annee_inscription):
    try:
        curseur.execute("""
            INSERT INTO etudiants
                (matricule, nom, prenom, date_naissance, email,
                 telephone, filiere, niveau, annee_inscription)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (matricule, nom, prenom, date_naissance, email,
              telephone, filiere, niveau, annee_inscription))
        db.commit()
        print(f"Étudiant {nom} {prenom} ajouté avec succès.")
    except Error as e:
        print("Erreur lors de l'ajout de l'étudiant :", e)


def modifier_etudiant(etudiant_id, matricule, nom, prenom, date_naissance,
                      email, telephone, filiere, niveau, annee_inscription):
    try:
        curseur.execute("""
            UPDATE etudiants SET
                matricule=%s, nom=%s, prenom=%s, date_naissance=%s,
                email=%s, telephone=%s, filiere=%s, niveau=%s,
                annee_inscription=%s
            WHERE id=%s
        """, (matricule, nom, prenom, date_naissance, email,
              telephone, filiere, niveau, annee_inscription, etudiant_id))
        db.commit()
        print(f"Étudiant id={etudiant_id} modifié avec succès.")
    except Error as e:
        print("Erreur lors de la modification :", e)


def supprimer_etudiant(etudiant_id):
    try:
        curseur.execute("DELETE FROM etudiants WHERE id=%s", (etudiant_id,))
        db.commit()
        print(f"Étudiant id={etudiant_id} supprimé.")
    except Error as e:
        print("Erreur lors de la suppression :", e)


def get_tous_etudiants():
    curseur.execute("""
        SELECT id, matricule, nom, prenom, date_naissance,
               email, telephone, filiere, niveau, annee_inscription
        FROM etudiants ORDER BY nom, prenom
    """)
    return curseur.fetchall()


def rechercher_etudiants(terme):
    like = f"%{terme}%"
    curseur.execute("""
        SELECT id, matricule, nom, prenom, date_naissance,
               email, telephone, filiere, niveau, annee_inscription
        FROM etudiants
        WHERE nom LIKE %s OR prenom LIKE %s OR matricule LIKE %s
        ORDER BY nom
    """, (like, like, like))
    return curseur.fetchall()


def get_etudiant_par_id(etudiant_id):
    curseur.execute("SELECT * FROM etudiants WHERE id=%s", (etudiant_id,))
    return curseur.fetchone()




def ajouter_enseignant(matricule, nom, prenom, email, telephone,
                       specialite, grade, statut):
    try:
        curseur.execute("""
            INSERT INTO enseignants
                (matricule, nom, prenom, email, telephone, specialite, grade, statut)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (matricule, nom, prenom, email, telephone, specialite, grade, statut))
        db.commit()
        print(f"Enseignant {nom} {prenom} ajouté.")
    except Error as e:
        print("Erreur :", e)


def modifier_enseignant(ens_id, matricule, nom, prenom, email, telephone,
                        specialite, grade, statut):
    try:
        curseur.execute("""
            UPDATE enseignants SET
                matricule=%s, nom=%s, prenom=%s, email=%s, telephone=%s,
                specialite=%s, grade=%s, statut=%s
            WHERE id=%s
        """, (matricule, nom, prenom, email, telephone,
              specialite, grade, statut, ens_id))
        db.commit()
        print(f"Enseignant id={ens_id} modifié.")
    except Error as e:
        print("Erreur :", e)


def supprimer_enseignant(ens_id):
    try:
        curseur.execute("DELETE FROM enseignants WHERE id=%s", (ens_id,))
        db.commit()
        print(f"Enseignant id={ens_id} supprimé.")
    except Error as e:
        print("Erreur :", e)


def get_tous_enseignants():
    curseur.execute("""
        SELECT id, matricule, nom, prenom, email,
               telephone, specialite, grade, statut
        FROM enseignants ORDER BY nom
    """)
    return curseur.fetchall()


def rechercher_enseignants(terme):
    like = f"%{terme}%"
    curseur.execute("""
        SELECT id, matricule, nom, prenom, email,
               telephone, specialite, grade, statut
        FROM enseignants
        WHERE nom LIKE %s OR prenom LIKE %s OR matricule LIKE %s
    """, (like, like, like))
    return curseur.fetchall()


def get_enseignant_par_id(ens_id):
    curseur.execute("SELECT * FROM enseignants WHERE id=%s", (ens_id,))
    return curseur.fetchone()




def ajouter_module(code, intitule, credits, volume_horaire,
                   filiere, niveau, semestre, enseignant_id):
    try:
        curseur.execute("""
            INSERT INTO modules
                (code, intitule, credits, volume_horaire,
                 filiere, niveau, semestre, enseignant_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (code, intitule, credits, volume_horaire,
              filiere, niveau, semestre, enseignant_id))
        db.commit()
        print(f"Module {code} ajouté.")
    except Error as e:
        print("Erreur :", e)


def modifier_module(module_id, code, intitule, credits, volume_horaire,
                    filiere, niveau, semestre, enseignant_id):
    try:
        curseur.execute("""
            UPDATE modules SET
                code=%s, intitule=%s, credits=%s, volume_horaire=%s,
                filiere=%s, niveau=%s, semestre=%s, enseignant_id=%s
            WHERE id=%s
        """, (code, intitule, credits, volume_horaire,
              filiere, niveau, semestre, enseignant_id, module_id))
        db.commit()
        print(f"Module id={module_id} modifié.")
    except Error as e:
        print("Erreur :", e)


def supprimer_module(module_id):
    try:
        curseur.execute("DELETE FROM modules WHERE id=%s", (module_id,))
        db.commit()
        print(f"Module id={module_id} supprimé.")
    except Error as e:
        print("Erreur :", e)


def get_tous_modules():
    curseur.execute("""
        SELECT m.id, m.code, m.intitule, m.credits, m.volume_horaire,
               m.filiere, m.niveau, m.semestre,
               CONCAT(e.nom, ' ', e.prenom) AS enseignant
        FROM modules m
        LEFT JOIN enseignants e ON m.enseignant_id = e.id
        ORDER BY m.code
    """)
    return curseur.fetchall()


def get_module_par_id(module_id):
    curseur.execute("SELECT * FROM modules WHERE id=%s", (module_id,))
    return curseur.fetchone()




def ajouter_evaluation(etudiant_id, module_id, type_eval, note,
                       coefficient, date_eval, semestre, annee_academique):
    try:
        curseur.execute("""
            INSERT INTO evaluations
                (etudiant_id, module_id, type_eval, note,
                 coefficient, date_eval, semestre, annee_academique)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (etudiant_id, module_id, type_eval, note,
              coefficient, date_eval, semestre, annee_academique))
        db.commit()
        print("Évaluation ajoutée.")
    except Error as e:
        print("Erreur :", e)


def modifier_evaluation(eval_id, etudiant_id, module_id, type_eval, note,
                        coefficient, date_eval, semestre, annee_academique):
    try:
        curseur.execute("""
            UPDATE evaluations SET
                etudiant_id=%s, module_id=%s, type_eval=%s, note=%s,
                coefficient=%s, date_eval=%s, semestre=%s, annee_academique=%s
            WHERE id=%s
        """, (etudiant_id, module_id, type_eval, note,
              coefficient, date_eval, semestre, annee_academique, eval_id))
        db.commit()
        print(f"Évaluation id={eval_id} modifiée.")
    except Error as e:
        print("Erreur :", e)


def supprimer_evaluation(eval_id):
    try:
        curseur.execute("DELETE FROM evaluations WHERE id=%s", (eval_id,))
        db.commit()
        print(f"Évaluation id={eval_id} supprimée.")
    except Error as e:
        print("Erreur :", e)


def get_toutes_evaluations():
    curseur.execute("""
        SELECT ev.id,
               CONCAT(et.nom, ' ', et.prenom) AS etudiant,
               m.code AS module,
               ev.type_eval, ev.note, ev.coefficient,
               ev.date_eval, ev.semestre, ev.annee_academique
        FROM evaluations ev
        JOIN etudiants et ON ev.etudiant_id = et.id
        JOIN modules   m  ON ev.module_id   = m.id
        ORDER BY ev.date_eval DESC
    """)
    return curseur.fetchall()


def get_evaluation_par_id(eval_id):
    curseur.execute("SELECT * FROM evaluations WHERE id=%s", (eval_id,))
    return curseur.fetchone()




def get_stats_globales():
    curseur.execute("SELECT COUNT(*) FROM etudiants")
    nb_etudiants = curseur.fetchone()[0]

    curseur.execute("SELECT COUNT(*) FROM enseignants")
    nb_enseignants = curseur.fetchone()[0]

    curseur.execute("SELECT COUNT(*) FROM modules")
    nb_modules = curseur.fetchone()[0]

    curseur.execute("SELECT COUNT(*) FROM evaluations")
    nb_evaluations = curseur.fetchone()[0]

    return {
        "etudiants":   nb_etudiants,
        "enseignants": nb_enseignants,
        "modules":     nb_modules,
        "evaluations": nb_evaluations,
    }


def get_moyenne_etudiant(etudiant_id):
    curseur.execute("""
        SELECT ROUND(SUM(note * coefficient) / SUM(coefficient), 2)
        FROM evaluations WHERE etudiant_id = %s
    """, (etudiant_id,))
    return curseur.fetchone()[0]


def get_taux_reussite_modules():
    curseur.execute("""
        SELECT m.intitule,
               COUNT(ev.id) AS total,
               SUM(CASE WHEN ev.note >= 10 THEN 1 ELSE 0 END) AS reussites,
               ROUND(
                   100.0 * SUM(CASE WHEN ev.note >= 10 THEN 1 ELSE 0 END)
                   / COUNT(ev.id), 1
               ) AS taux
        FROM evaluations ev
        JOIN modules m ON ev.module_id = m.id
        GROUP BY m.id, m.intitule
        ORDER BY taux DESC
    """)
    return curseur.fetchall()
