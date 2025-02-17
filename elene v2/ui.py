from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QGridLayout, QScrollArea
from PyQt6.QtCore import Qt
from db_utils import *
import sys
import subprocess


class BaseWindow(QWidget):
    def __init__(self, parent_window=None):
        super().__init__()
        self.setWindowTitle("E-lene")
        self.showFullScreen()

        self.parent_window = parent_window  # Référence à la fenêtre parente si elle existe

        # Bouton Retour
        back_button = QPushButton("← Retour")
        back_button.setObjectName("backButton")
        back_button.setFixedSize(100, 50)
        back_button.clicked.connect(self.go_back)

        # Bouton Home
        home_button = QPushButton("Home")
        home_button.setObjectName("homeButton")
        home_button.setFixedSize(150, 50)
        home_button.clicked.connect(self.go_home)

        # Bouton Quitter
        quit_button = QPushButton("X")
        quit_button.setObjectName("quitButton")
        quit_button.setFixedSize(50, 50)
        quit_button.clicked.connect(self.close)

        # Barre du haut avec les boutons
        self.top_layout = QHBoxLayout()
        self.top_layout.addWidget(back_button)
        self.top_layout.addStretch()
        self.top_layout.addWidget(home_button)
        self.top_layout.addStretch()
        self.top_layout.addWidget(quit_button)

        # Layout principal
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.top_layout)

        self.setLayout(self.main_layout)

    def setup_ui(self, layout):
        """Ajoute un layout spécifique sous la barre supérieure"""
        self.main_layout.addLayout(layout)

    def go_home(self):
        """Retour à l'accueil"""
        self.main_window = MainWindow()
        self.main_window.showFullScreen()
        self.close()

    def go_back(self):
        """Retour à la fenêtre précédente (parent)"""
        if self.parent_window:
            self.parent_window.showMaximized()  # Maximise la fenêtre parente
            self.parent_window.show()  # Assure que la fenêtre parente est visible

        self.close()  # Ferme la fenêtre actuelle

class MainWindow(BaseWindow):
    def __init__(self, parent_window=None):
        super().__init__(parent_window)  # Même si c'est la première fenêtre, pour uniformiser
        self.showFullScreen()
        
        self.selected_objects = []  # Liste des objets sélectionnés

        title_label = QLabel("E-lene")
        title_label.setStyleSheet("font-size: 36px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setObjectName("titleLabel")

        subtitle_label = QLabel("Emprunter ou rendre ?")
        subtitle_label.setStyleSheet("font-size: 20px;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setObjectName("subtitleLabel")

        self.borrow_button = QPushButton("Emprunter")
        self.return_button = QPushButton("Rendre")

        for button in [self.borrow_button, self.return_button]:
            button.setObjectName("actionButton")
            button.setFixedSize(250, 100)

        self.borrow_button.clicked.connect(self.show_user_selection)
        self.return_button.clicked.connect(self.show_return_user_selection)

        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.borrow_button)
        button_layout.addWidget(self.return_button)

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addLayout(button_layout)
        layout.addStretch()

        self.setup_ui(layout)

    def show_user_selection(self):
        self.user_window = UserSelectionWindow(self.selected_objects, parent_window=self)  # Passe la sélection d'objets
        self.user_window.showFullScreen()
        self.close()
    def show_return_user_selection(self):
        self.user_window = ReturnUserSelectionWindow(parent_window=self)  # Passe la sélection d'objets
        self.user_window.showFullScreen()
        self.close()

class UserSelectionWindow(BaseWindow):
    def __init__(self, selected_objects, parent_window=None):
        super().__init__(parent_window)
        self.selected_objects = selected_objects
        self.showFullScreen()

        title_label = QLabel("Sélectionnez un utilisateur")
        title_label.setStyleSheet("font-size: 24px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.user_list = QListWidget()
        self.user_list.setStyleSheet("font-size: 24px; padding: 10px;")

        self.users = get_users()
        for user in self.users:
            self.user_list.addItem(f"{user[1]} {user[2]}")

        self.user_list.itemClicked.connect(self.select_user)

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(self.user_list)

        self.setup_ui(layout)

    def select_user(self, item):
        """Enregistre l'utilisateur sélectionné et passe à la sélection de catégorie."""
        selected_user_name = item.text()
        selected_user_id = next(user[0] for user in self.users if f"{user[1]} {user[2]}" == selected_user_name)
        
        # Enregistrer l'ID de l'utilisateur
        self.selected_user_id = selected_user_id

        # Passer à la fenêtre suivante en incluant l'ID de l'utilisateur
        self.category_window = CategoryWindow(self.selected_objects, self.selected_user_id, parent_window=self)  
        self.category_window.showFullScreen()
        self.close()

class CategoryWindow(BaseWindow):
    def __init__(self, selected_objects, user_id, parent_window=None):
        super().__init__(parent_window)
        self.selected_objects = selected_objects
        self.user_id = user_id  # Sauvegarder l'ID de l'utilisateur
        self.showFullScreen()

        title_label = QLabel("Choisir une catégorie")
        title_label.setStyleSheet("font-size: 24px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        self.categories = get_categories()
        for category in self.categories:
            button = QPushButton(category[1])
            button.setObjectName("actionButton")
            button.setFixedSize(250, 80)
            button.clicked.connect(lambda _, c=category[0]: self.select_category(c))
            layout.addWidget(button)

        self.setup_ui(layout)

    def select_category(self, category_id):
        """Passer à la sous-catégorie en incluant l'ID de l'utilisateur"""
        self.subcategory_window = SubCategoryWindow(self.selected_objects, category_id, self.user_id, parent_window=self)
        self.subcategory_window.showFullScreen()
        self.close()

class SubCategoryWindow(BaseWindow):
    def __init__(self, selected_objects, category_id, user_id, parent_window=None):
        super().__init__(parent_window)
        self.selected_objects = selected_objects
        self.category_id = category_id
        self.user_id = user_id  # Sauvegarder l'ID de l'utilisateur
        self.showFullScreen()

        title_label = QLabel("Choisir une sous-catégorie")
        title_label.setStyleSheet("font-size: 24px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        self.subcategories = get_subcategories(category_id)
        for subcategory in self.subcategories:
            button = QPushButton(subcategory[1])
            button.setObjectName("actionButton")
            button.setFixedSize(250, 80)
            button.clicked.connect(lambda _, s=subcategory[0]: self.select_subcategory(s))
            layout.addWidget(button)

        self.setup_ui(layout)

    def select_subcategory(self, subcategory_id):
        """Passer à la sélection des objets en incluant l'ID de l'utilisateur"""
        self.object_window = ObjectSelectionWindow(self.selected_objects, subcategory_id, self.user_id, parent_window=self)
        self.object_window.showFullScreen()
        self.close()

class ObjectSelectionWindow(BaseWindow):
    def __init__(self, selected_objects, subcategory_id, user_id, parent_window=None):
        super().__init__(parent_window)
        self.selected_objects = selected_objects
        self.subcategory_id = subcategory_id
        self.user_id = user_id  # Sauvegarder l'ID de l'utilisateur
        self.showFullScreen()

        title_label = QLabel("Choisir un ou plusieurs objets")
        title_label.setStyleSheet("font-size: 24px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(title_label)

        self.objects = get_objects(subcategory_id)

        button_widget = QWidget()
        button_layout = QGridLayout()

        column_count = 2 if len(self.objects) > 5 else 1
        row = 0
        col = 0

        for i, obj in enumerate(self.objects):
            button = QPushButton(obj[1])
            button.setObjectName("actionButton")
            button.setFixedSize(150, 80)
            button_layout.addWidget(button, row, col)

            # Appliquer la couleur en fonction de la sélection précédente
            if obj[0] in self.selected_objects:
                button.setStyleSheet("background-color: #2ecc71;")  # Couleur de sélection
            else:
                button.setStyleSheet("background-color: #3498db;")  # Couleur par défaut

            button.clicked.connect(lambda _, o=obj[0], b=button: self.toggle_selection(o, b))
            col += 1
            if col >= column_count:
                col = 0
                row += 1

        button_widget.setLayout(button_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidget(button_widget)
        scroll_area.setWidgetResizable(True)

        layout.addWidget(scroll_area)

        # Bouton "Valider"
        validate_button = QPushButton("Valider")
        validate_button.setObjectName("validateButtonSelection")  # Appliquer la classe CSS
        validate_button.clicked.connect(self.show_summary)
        layout.addWidget(validate_button)

        self.setup_ui(layout)

    def toggle_selection(self, object_id, button):
        """Ajoute ou retire un objet de la liste des objets sélectionnés."""
        if object_id in self.selected_objects:
            self.selected_objects.remove(object_id)
            button.setStyleSheet("background-color: #3498db;")  # Réinitialiser la couleur
        else:
            self.selected_objects.append(object_id)
            button.setStyleSheet("background-color: #2ecc71;")  # Couleur de sélection

    def show_summary(self):
        """Affiche une nouvelle fenêtre avec le récapitulatif des objets sélectionnés."""
        self.summary_window = SummaryWindow(self.selected_objects, self.user_id, parent_window=self)  # Passer l'ID de l'utilisateur
        self.summary_window.showFullScreen()
        self.close()

class SummaryWindow(BaseWindow):
    def __init__(self, selected_objects, user_id, parent_window=None):
        super().__init__(parent_window)
        self.selected_objects = selected_objects  # Liste des objets sélectionnés
        self.user_id = user_id  # L'ID de l'utilisateur
        self.showFullScreen()

        title_label = QLabel("Récapitulatif : ")
        title_label.setObjectName("titleLabel")
        layout = QVBoxLayout()
        layout.addWidget(title_label)

        # Récupération des objets sélectionnés
        objects = get_objects_summary(self.selected_objects)

        for object in objects:
            object_name = object[1]
            object_label = QLabel(object_name)
            object_label.setObjectName("objectLabel")
            layout.addWidget(object_label)

        open_button = QPushButton("Ouvrir la porte ! ")
        open_button.setObjectName("openDoorButton")
        open_button.clicked.connect(self.open_door)
        layout.addWidget(open_button)

        self.setup_ui(layout)

    def open_door(self):
        """Fonction pour ouvrir la porte et enregistrer l'emprunt dans la base de données."""
        print("La porte est ouverte.")

        # Enregistrer les emprunts
        for object_id in self.selected_objects:
            create_loan_entry(self.user_id, object_id)  # Appel de la fonction pour enregistrer l'emprunt dans la base de données
            update_object_availability(object_id, 0)  # Mettre l'objet à "emprunté" (disponible = 0)

        # Afficher la fenêtre de "Fermer la porte"
        self.close_door_window = CloseDoorWindow(parent_window=self)
        self.close_door_window.showFullScreen()

        # Fermer la fenêtre actuelle
        self.close()

class CloseDoorWindow(BaseWindow):

    def __init__(self, parent_window=None):
        super().__init__(parent_window)
        self.showFullScreen()


        # Titre principal
        subtitle_label = QLabel("La porte est ouverte ! pensez à la fermer.")
        subtitle_label.setStyleSheet("font-size: 20px;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setObjectName("subtitleLabel")
        layout = QVBoxLayout()
        layout.addWidget(subtitle_label)

        # Bouton "Retour à l'accueil"
        close_button = QPushButton("Fermez la porte !")
        close_button.setObjectName("openDoorButton")
        close_button.clicked.connect(self.quit_and_restart)
        layout.addWidget(close_button)

        self.setup_ui(layout)

    def quit_and_restart(self):
        """Quitte l'application et relance main.py"""
        print("Quitter et relancer l'application...")

        # Relancer main.py (ou le fichier principal de l'application)
        subprocess.Popen([sys.executable, "main.py"])

        # Ferme l'application actuelle
        self.close()
        sys.exit(0)

class ReturnUserSelectionWindow(BaseWindow):
    def __init__(self, parent_window=None):
        super().__init__(parent_window)
        self.showFullScreen()

        title_label = QLabel("Sélectionnez un utilisateur")
        title_label.setStyleSheet("font-size: 24px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.user_list = QListWidget()
        self.user_list.setStyleSheet("font-size: 24px; padding: 10px;")

        self.users = get_users()  # Récupérer tous les utilisateurs
        for user in self.users:
            self.user_list.addItem(f"{user[1]} {user[2]}")  # Afficher le nom complet de chaque utilisateur

        self.user_list.itemClicked.connect(self.select_user)

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(self.user_list)

        self.setup_ui(layout)

    def select_user(self, item):
        """Enregistre l'utilisateur sélectionné et passe à la gestion des objets à rendre."""
        selected_user_name = item.text()
        selected_user_id = next(user[0] for user in self.users if f"{user[1]} {user[2]}" == selected_user_name)
        selected_user_prenom = next(user[1] for user in self.users if f"{user[1]} {user[2]}" == selected_user_name)
        selected_user_nom = next(user[2] for user in self.users if f"{user[1]} {user[2]}" == selected_user_name)

        # Enregistrer l'ID de l'utilisateur et le prénom/nom
        self.selected_user_id = selected_user_id
        self.selected_user_prenom = selected_user_prenom
        self.selected_user_nom = selected_user_nom

        # Passer à la fenêtre suivante pour afficher les objets empruntés à rendre
        self.return_object_window = ReturnObjectWindow(self.selected_user_id, self.selected_user_prenom, self.selected_user_nom, parent_window=self)
        self.return_object_window.showFullScreen()
        self.close()

class ReturnObjectWindow(BaseWindow):
    def __init__(self, user_id, prenom, nom, selected_objects=None, parent_window=None):
        super().__init__(parent_window)
        self.selected_objects = selected_objects if selected_objects else []
        self.user_id = user_id  # L'ID de l'utilisateur dont on veut gérer les retours
        self.prenom = prenom  # Prénom de l'utilisateur
        self.nom = nom  # Nom de l'utilisateur
        self.showFullScreen()

        # Personnalisation du titre
        title_label = QLabel(f"Bonjour {self.prenom} {self.nom}, sélectionnez les objets à rendre")
        title_label.setStyleSheet("font-size: 24px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(title_label)

        # Récupérer les objets empruntés par cet utilisateur (sans date de retour)
        self.loans = get_loans_for_user(self.user_id)  # Appel à la fonction déplacée
        
        button_widget = QWidget()
        button_layout = QGridLayout()

        column_count = 2 if len(self.loans) > 5 else 1
        row = 0
        col = 0

        for loan in self.loans:
            object_id = loan[1]
            object_name = loan[2]  # Le nom de l'objet emprunté

            button = QPushButton(object_name)
            button.setObjectName("actionButton")
            button.setFixedSize(150, 80)
            button_layout.addWidget(button, row, col)

            # Connecter le bouton pour marquer l'objet comme sélectionné/désélectionné
            button.clicked.connect(lambda _, o=object_id, b=button: self.toggle_selection(o, b))
            col += 1
            if col >= column_count:
                col = 0
                row += 1

        button_widget.setLayout(button_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidget(button_widget)
        scroll_area.setWidgetResizable(True)

        layout.addWidget(scroll_area)

        # Bouton "Ouvrir la porte" pour confirmer le retour
        open_button = QPushButton("Ouvrir la porte")
        open_button.setObjectName("openDoorButton")
        open_button.clicked.connect(self.open_door)  # Connexion à la méthode open_door
        layout.addWidget(open_button)

        self.setup_ui(layout)

    def toggle_selection(self, object_id, button):
        """Ajoute ou retire un objet de la liste des objets sélectionnés à rendre."""
        if object_id in self.selected_objects:
            self.selected_objects.remove(object_id)
            button.setStyleSheet("background-color: #3498db;")  # Réinitialiser la couleur
        else:
            self.selected_objects.append(object_id)
            button.setStyleSheet("background-color: #2ecc71;")  # Couleur de sélection

    def open_door(self):
        """Fonction pour ouvrir la porte et enregistrer le retour des objets."""
        print("La porte est ouverte.")

        # Enregistrer les retours des objets et mettre à jour la disponibilité
        for object_id in self.selected_objects:
            return_object(object_id, self.user_id)  # Appel à la fonction déplacée dans db_utils

        # Afficher la fenêtre de "Fermer la porte"
        self.close_door_window = CloseDoorWindow(parent_window=self)
        self.close_door_window.showFullScreen()

        # Fermer la fenêtre actuelle
        self.close()
