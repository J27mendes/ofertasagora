import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

# Define o caminho base e força o carregamento do .env na raiz
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=env_path)

# DEBUG PARA VOCÊ VER NO TERMINAL SE ESTÁ CARREGANDO
print(f"DATABASE_URL carregada? {os.getenv('DATABASE_URL') is not None}")

# --- SEGURANÇA ---
# Em produção, a SECRET_KEY deve vir do .env
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-mude-isso-em-producao')

# DEBUG deve ser False em produção. O .env resolve isso:
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# ALLOWED_HOSTS: No Docker/Produção, permitimos o domínio ou '*' (com cuidado)
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost,.vercel.app').split(',')

# --- APLICAÇÕES ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'money',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # ESSENCIAL para arquivos estáticos no Docker
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'money.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Melhorado para achar templates globais
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'money.wsgi.application'

# --- BANCO DE DADOS ---
# Se DATABASE_URL não existir no .env, ele usa o SQLite local por padrão
db_url = os.getenv('DATABASE_URL')

if db_url:
    # Limpeza profunda para evitar o erro de Scheme '://'
    db_url = db_url.strip().replace('"', '').replace("'", "")
    
    # Se por acaso a limpeza deixar a string vazia ou inválida
    if not db_url.startswith('postgres'):
         print("AVISO: DATABASE_URL encontrada, mas não começa com 'postgres'. Verifique o .env")

DATABASES = {
    'default': dj_database_url.config(
        default=db_url,
        conn_max_age=600,
        ssl_require=not DEBUG 
    )
}

# --- ARQUIVOS ESTÁTICOS ---
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- INTERNACIONALIZAÇÃO ---
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo' # Ajustado para o horário de Brasília
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'