import os
from dotenv import load_dotenv

# Carga las variables definidas en el archivo .env (en la raíz del proyecto)
# hacia el entorno del proceso. En producción también puedes definirlas
# directamente en la unidad systemd (ver deploy/gunicorn-pazsalvo.service);
# ambas formas conviven sin problema porque os.environ.get() lee lo que sea
# que ya esté puesto ahí.
load_dotenv()


class Config:
    # Clave secreta para proteger las sesiones y las cookies. El valor fijo
    # es SOLO para desarrollo local sin .env; en producción SIEMPRE debe
    # venir de la variable de entorno SECRET_KEY (ver .env.example).
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-super-secreta-inamhi-2026'

    # ==========================================
    # CONFIGURACIÓN DE CONEXIÓN A MYSQL 8
    # ==========================================
    # Formato: mysql+pymysql://usuario:contraseña@servidor/nombre_base_datos
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:root@localhost/paz_salvo_db'

    # Desactivamos esta opción porque consume mucha memoria innecesariamente
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Recicla conexiones inactivas antes de que MySQL las cierre por su
    # cuenta (wait_timeout por defecto de MySQL es 8h, pero es buena
    # práctica no confiar en ese límite en un proceso de larga duración
    # como Gunicorn) y detecta conexiones muertas antes de usarlas.
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 280,
    }

    # Límite de tamaño de subida (PDFs firmados, certificados .p12): debe
    # ser <= client_max_body_size en Nginx (ver deploy/nginx_pazsalvo.conf)
    # para que sea Flask, no Nginx, quien responda con el error legible.
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 25 * 1024 * 1024))

    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    # Cookies de sesión solo por HTTPS: déjalo en False mientras el sitio
    # sirva por HTTP plano (como este despliegue en 10.0.153.64:80). Si más
    # adelante se pone TLS delante (Nginx con certificado), cambia esta
    # variable de entorno a 'true' para que las cookies no viajen sin cifrar.
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'false').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
