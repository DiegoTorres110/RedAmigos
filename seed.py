from db import run_query, close_driver
import repo

PERSONAS = [
    (1, "Ana",    22, "Mérida"),
    (2, "Luis",   24, "Mérida"),
    (3, "Carla",  21, "Valladolid"),
    (4, "Diego",  23, "Mérida"),
    (5, "Elena",  25, "Progreso"),
    (6, "Fabián", 22, "Mérida"),
    (7, "Gaby",   20, "Valladolid"),
    (8, "Hugo",   26, "Izamal"),
]

AMISTADES = [
    (1, 2, 2019), (1, 3, 2020), (2, 4, 2018), (3, 5, 2021),
    (4, 5, 2022), (4, 6, 2020), (5, 7, 2023), (6, 8, 2021),
]

INTERESES = [
    (1, "Música"), (1, "Cine"), (2, "Música"), (2, "Fútbol"),
    (3, "Cine"), (4, "Fútbol"), (5, "Viajes"), (6, "Música"),
    (7, "Viajes"), (7, "Cine"), (8, "Fútbol"),
]

def main():
    print("Limpiando base de datos...")
    run_query("MATCH (n) DETACH DELETE n")

    print("Creando restricciones...")
    repo.crear_restricciones()

    print("Creando personas...")
    for p in PERSONAS:
        repo.crear_persona(*p)

    print("Creando amistades...")
    for a in AMISTADES:
        repo.crear_amistad(*a)

    print("Asignando intereses...")
    for i in INTERESES:
        repo.agregar_interes(*i)

    print(f"Listo: {len(PERSONAS)} personas, {len(AMISTADES)} amistades, "
          f"{len(INTERESES)} intereses.")

if __name__=="__main__":
    try:
        main()
    finally:
        close_driver()