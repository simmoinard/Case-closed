import sqlite3
from datetime import datetime


DB_PATH = "elene.db"

def test_get_categories():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories;")
    categories = cursor.fetchall()
    conn.close()
    print("Catégories trouvées :", categories)

if __name__ == "__main__":
    test_get_categories()

def get_users():
    """Récupère tous les utilisateurs depuis la base de données"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, prenom FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def get_categories():
    """Récupère toutes les catégories depuis la base de données"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom FROM categories")
    categories = cursor.fetchall()
    conn.close()
    return categories

def get_subcategories(category_id):
    """Récupère les sous-catégories d'une catégorie donnée"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom FROM subcategories WHERE category_id = ?", (category_id,))
    subcategories = cursor.fetchall()
    conn.close()
    return subcategories

def get_objects(subcategory_id):
    """Récupère les objets appartenant à une sous-catégorie donnée et disponibles"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom FROM objects WHERE subcategory_id = ? AND disponible = 1", (subcategory_id,))
    objects = cursor.fetchall()
    conn.close()
    return objects

#Ici on récupère tous les objets sans subcategorie. 
def get_objects_summary(object_ids):
    """Récupère les objets en fonction de leurs IDs (pour le récapitulatif)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Récupérer les objets dont les IDs sont dans la liste `object_ids`
    query = f"SELECT id, nom FROM objects WHERE id IN ({','.join(['?'] * len(object_ids))})"
    cursor.execute(query, tuple(object_ids))
    objects = cursor.fetchall()
    
    conn.close()
    return objects

def create_loan_entry(user_id, object_id):
    """Ajoute un emprunt dans la table 'loans'."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Récupération de la date actuelle
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Insertion dans la table 'loan'
    cursor.execute("INSERT INTO loans (user_id, object_id, date_emprunt) VALUES (?, ?, ?)",
                   (user_id, object_id, current_date))
    conn.commit()
    conn.close()

    print(f"Emprunt enregistré : Utilisateur {user_id}, Objet {object_id}, Date {current_date}")

def update_object_availability(object_id, available):
    """Met à jour la disponibilité d'un objet dans la base de données."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE objects SET disponible = ? WHERE id = ?", (available, object_id))
    conn.commit()
    conn.close()
    print(f"Objet {object_id} mis à jour. Disponibilité : {available}")

def get_loans_for_user(user_id):
    """Récupère tous les emprunts pour un utilisateur spécifique (avec date_retour NULL)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT loans.id, loans.object_id, objects.nom
        FROM loans
        JOIN objects ON loans.object_id = objects.id
        WHERE loans.user_id = ? AND loans.date_retour IS NULL
    """, (user_id,))
    loans = cursor.fetchall()
    conn.close()
    return loans

def return_object(object_id, user_id):
    """Met à jour la date de retour et la disponibilité de l'objet."""
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Mettre à jour la table des emprunts pour ajouter la date de retour
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE loans SET date_retour = ? WHERE object_id = ? AND user_id = ? AND date_retour IS NULL",
                   (current_date, object_id, user_id))
    
    # Mettre l'objet comme disponible (disponible = 1)
    cursor.execute("UPDATE objects SET disponible = 1 WHERE id = ?", (object_id,))
    conn.commit()
    conn.close()
    print(f"Objet {object_id} retourné. Date de retour : {current_date}")
