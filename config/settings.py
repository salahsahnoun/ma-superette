import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-changez-moi')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'jazzmin',                           # doit être avant django.contrib.admin
    'modeltranslation',                  # doit être avant django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'produits',
    'panier',
    'commandes',
    'comptes',
]

LOGIN_URL          = '/comptes/connexion/'
LOGIN_REDIRECT_URL = '/comptes/profil/'
LOGOUT_REDIRECT_URL = '/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'panier.context_processors.panier_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ── Base de données ─────────────────────────────────────────────────────────
_db_url = os.environ.get('DATABASE_URL', '')
if _db_url:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(default=_db_url, conn_max_age=600, ssl_require=True)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fr'
LANGUAGES = [
    ('fr', 'Français'),
    ('en', 'English'),
    ('ar', 'العربية'),
]
LOCALE_PATHS = [BASE_DIR / 'locale']
TIME_ZONE = 'Africa/Algiers'
USE_I18N = True
USE_L10N = False
USE_TZ = True

CURRENCY_SYMBOL = 'DA'

AUTHENTICATION_BACKENDS = [
    'comptes.backends.EmailOrPhoneBackend',
]

# ── Fichiers statiques ──────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'config.storage.StaticStorage'

# ── Fichiers média (images produits) ────────────────────────────────────────
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', ''),
    'API_KEY':    os.environ.get('CLOUDINARY_API_KEY', ''),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', ''),
}

if os.environ.get('CLOUDINARY_CLOUD_NAME'):
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    MEDIA_URL = '/media/'
else:
    MEDIA_URL  = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ADMINS = []

FRAIS_LIVRAISON = '3.00'

# ── Sécurité HTTPS (production uniquement) ──────────────────────────────────
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT      = True
    SESSION_COOKIE_SECURE    = True
    CSRF_COOKIE_SECURE       = True
    SECURE_HSTS_SECONDS      = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# ═══════════════════════════════════════════════
#  JAZZMIN — Interface admin
# ═══════════════════════════════════════════════
JAZZMIN_SETTINGS = {
    # Titres
    "site_title":    "Ma Superette",
    "site_header":   "Ma Superette",
    "site_brand":    "🌿 Ma Superette",
    "welcome_sign":  "Bienvenue dans l'espace administration",
    "copyright":     "Ma Superette © 2026",

    # Recherche globale
    "search_model": ["produits.Produit", "commandes.Commande"],

    # Liens dans la top-bar
    "topmenu_links": [
        {
            "name": "🏪 Voir le site",
            "url": "/",
            "new_window": True,
        },
        {
            "name": "⏳ Commandes en attente",
            "url": "/admin/commandes/commande/?statut__exact=en_attente",
        },
        {
            "name": "⚙️ En cours",
            "url": "/admin/commandes/commande/?statut__exact=en_cours",
        },
        {
            "name": "🚪 Déconnexion",
            "url": "/admin/deconnexion/",
        },
    ],

    # Lien dans le menu utilisateur
    "usermenu_links": [
        {"name": "Voir le site", "url": "/", "new_window": True},
    ],

    # Sidebar
    "show_sidebar": True,
    "navigation_expanded": True,

    # Ordre des apps dans la sidebar
    "order_with_respect_to": ["produits", "commandes", "auth"],

    # Icônes Font Awesome pour chaque modèle
    "icons": {
        "auth":                    "fas fa-shield-alt",
        "auth.user":               "fas fa-user",
        "auth.Group":              "fas fa-users",
        "produits.Categorie":      "fas fa-tags",
        "produits.Produit":        "fas fa-box-open",
        "commandes.Commande":      "fas fa-shopping-bag",
        "commandes.LigneCommande": "fas fa-list-ul",
    },

    "default_icon_parents":  "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    # Modal pour les FK (ex: choisir un produit)
    "related_modal_active": True,

    # CSS/JS custom
    "custom_css": "css/admin_custom.css",
    "custom_js":  "js/admin_camera.js",

    "use_google_fonts_cdn": False,
    "show_ui_builder":      False,

    # Format du formulaire de détail
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user":  "collapsible",
        "auth.group": "vertical_tabs",
    },

    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text":          False,
    "footer_small_text":          True,
    "body_small_text":            True,
    "brand_small_text":           False,

    # Couleurs — vert forêt comme le site
    "brand_colour":               "navbar-success",
    "accent":                     "accent-success",
    "navbar":                     "navbar-white",
    "no_navbar_border":           False,
    "navbar_fixed":               True,
    "sidebar_fixed":              True,
    "sidebar":                    "sidebar-dark-success",
    "sidebar_nav_compact_style":  True,
    "sidebar_nav_child_indent":   True,

    "layout_boxed":               False,
    "footer_fixed":               False,
    "actions_sticky_top":         True,

    "button_classes": {
        "primary":   "btn-primary",
        "secondary": "btn-secondary",
        "info":      "btn-outline-info",
        "warning":   "btn-warning",
        "danger":    "btn-danger",
        "success":   "btn-success",
    },
}
