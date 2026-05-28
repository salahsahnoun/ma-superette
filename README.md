claude --resume 5f344be4-8bb4-4379-8285-13f88aa324ef

# Superette en Ligne

Site e-commerce pour une superette de quartier, permettant aux clients de parcourir et commander des produits, et à l'administrateur de gérer le catalogue depuis une interface dédiée.

---

## Fonctionnalités

### Côté client
- Parcourir les produits par catégorie (légumes & fruits, conserves, produits ménagers, gâteaux & snacks, autres)
- Voir la fiche détaillée d'un produit (photo, prix, description, stock)
- Ajouter des produits au panier
- Modifier les quantités ou retirer des articles du panier
- Passer une commande (nom, adresse, téléphone)
- Recevoir un récapitulatif de commande

### Côté admin (interface privée)
- Connexion sécurisée (accès réservé)
- Ajouter / modifier / supprimer des produits
- Uploader une photo pour chaque produit
- Gérer les catégories
- Voir la liste des commandes reçues
- Marquer une commande comme traitée

---

## Stack technique

| Composant   | Technologie              |
|-------------|--------------------------|
| Backend     | Python 3.12 / Django 5.x |
| Base de données | SQLite (dev) → PostgreSQL (prod) |
| Frontend    | HTML + Bootstrap 5 + Vanilla JS |
| Images      | Pillow (stockage local)  |
| Admin       | Django Admin (personnalisé) |

---

## Structure du projet

```
ecommerce/
├── manage.py
├── requirements.txt
├── .env.example
│
├── config/                  # Paramètres Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── produits/                # App : catalogue produits
│   ├── models.py            # Produit, Categorie
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── panier/                  # App : gestion du panier (session)
│   ├── cart.py
│   ├── views.py
│   └── urls.py
│
├── commandes/               # App : commandes clients
│   ├── models.py            # Commande, LigneCommande
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── templates/               # Templates HTML
│   ├── base.html
│   ├── produits/
│   │   ├── liste.html
│   │   └── detail.html
│   ├── panier/
│   │   └── panier.html
│   └── commandes/
│       ├── checkout.html
│       └── confirmation.html
│
├── static/                  # CSS, JS, images statiques
│   ├── css/style.css
│   └── js/panier.js
│
└── media/                   # Photos produits uploadées
```

---

## Catégories de produits

- **Légumes & Fruits** — tomates, carottes, bananes, pommes...
- **Conserves** — boîtes de thon, haricots, maïs, tomates pelées...
- **Produits ménagers** — lessive, liquide vaisselle, éponges...
- **Gâteaux & Snacks** — biscuits, gâteaux emballés, bonbons...
- **Autres** — tout ce qui ne rentre pas dans les catégories ci-dessus

---

## Installation (développement)

```bash
# 1. Cloner le projet
git clone <repo>
cd ecommerce

# 2. Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos valeurs

# 5. Initialiser la base de données
python manage.py migrate

# 6. Créer le compte administrateur
python manage.py createsuperuser

# 7. Lancer le serveur
python manage.py runserver
```

Le site sera disponible sur : `http://localhost:8000`  
L'interface admin sera disponible sur : `http://localhost:8000/admin`

---

## Variables d'environnement (`.env`)

```
SECRET_KEY=votre_clé_secrète
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## Utilisation de l'interface admin

1. Aller sur `/admin` et se connecter avec le compte superuser
2. Créer des catégories dans **Produits > Catégories**
3. Ajouter des produits dans **Produits > Produits** (nom, prix, stock, photo, catégorie)
4. Consulter les commandes dans **Commandes > Commandes**

---

## Roadmap (améliorations futures possibles)

- Système de paiement en ligne (Stripe)
- Compte client avec historique de commandes
- Recherche et filtres avancés
- Notifications par email
- Mode sombre
- Application mobile

---

## Licence

Projet privé — tous droits réservés.
