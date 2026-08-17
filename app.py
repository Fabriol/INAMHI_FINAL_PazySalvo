import os
from app import create_app, db

# Llamamos a la fábrica para crear nuestra aplicación
app = create_app()

# Este bloque asegura que el servidor solo se encienda si ejecutamos este archivo directamente
# (uso local con `python app.py`; en producción el proceso lo levanta Gunicorn vía wsgi.py,
# nunca este bloque).
if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', '1') == '1'
    puerto = int(os.environ.get('PORT', 9095))
    app.run(debug=debug, port=puerto, host='0.0.0.0')
