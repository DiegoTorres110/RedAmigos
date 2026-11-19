# RedAmigos

Red social con recomendaciones sobre Neo4j AuraDB (Python + driver oficial).

## Requisitos
- Python 3.9+
- Cuenta gratuita en https://console.neo4j.io (instancia AuraDB Free)

## Instalación
```
pip install -r requirements.txt
```
Crea un archivo ` .env` con las credenciales de tu instancia:
```
NEO4J_URI=neo4j+s://xxxxxxxx.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=tu_password
NEO4J_DATABASE=neo4j
```

## Ejecución
```
python seed.py
python main.py
```