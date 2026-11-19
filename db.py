import os
from pathlib import Path
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(Path(__file__).parent / ".env", override=True)

_driver = None

def get_driver():
    """Crea (una sola vez) y devuelve el driver."""
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD")),
        )
        _driver.verify_connectivity()
    return _driver

def run_query(query, **params):
    db = os.getenv("NEO4J_DATABASE", "neo4j")
    with get_driver().session(database=db) as session:
        result = session.run(query, **params)
        return [record.data() for record in result]

def close_driver():
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None