from db import close_driver
import repo

def imprimir(filas):
    if not filas:
        print(" (sin resultados)")
        return
    for fila in filas:
        print(" ", fila)

def pedir_int(texto):
    while True:
        try:
            return int(input(texto))
        except ValueError:
            print(" Escribe un número entero.")

def menu():
    print(
        """
RedAmigos:
 1. Listar personas
 2. Ver persona (con intereses)
 3. Crear persona
 4. Actualizar persona
 5. Eliminar persona
 6. Crear amistad
 7. Eliminar amistad
 8. Agregar interés
 9. Amigos directos
10. Amigos de amigos
11. Camino más corto
12. Recomendar amigos (por amigos en común)
13. Recomendar por intereses
 0. Salir
""")

def main():
    repo.crear_restricciones()
    while True:
        menu()
        op = input("Opción: ").strip()

        if op == "1":
            imprimir(repo.listar_personas())
        elif op == "2":
            imprimir(repo.obtener_persona(pedir_int("ID: ")))
        elif op == "3":
            id_ = pedir_int("ID: ")
            nombre = input("Nombre: ")
            edad = pedir_int("Edad: ")
            ciudad = input("Ciudad: ")
            imprimir(repo.crear_persona(id_, nombre, edad, ciudad))
        elif op == "4":
            id_ = pedir_int("ID a actualizar: ")
            print(" (deja vacío lo que no quieras cambiar)")
            nombre = input("Nuevo nombre: ") or None
            edad_txt = input("Nueva edad: ")
            edad = int(edad_txt) if edad_txt else None
            ciudad = input("Nueva ciudad: ") or None
            imprimir(repo.actualizar_persona(id_, nombre, edad, ciudad))
        elif op == "5":
            imprimir(repo.eliminar_persona(pedir_int("ID a eliminar: ")))
        elif op == "6":
            a = pedir_int("ID persona A: ")
            b = pedir_int("ID persona B: ")
            desde = pedir_int("Año desde: ")
            imprimir(repo.crear_amistad(a, b, desde))
        elif op == "7":
            a = pedir_int("ID persona A: ")
            b = pedir_int("ID persona B: ")
            imprimir(repo.eliminar_amistad(a, b))
        elif op == "8":
            id_ =  pedir_int("ID persona: ")
            interes = input("Interés: ")
            imprimir(repo.agregar_interes(id_, interes))
        elif op == "9": 
            imprimir(repo.amigos_directos(pedir_int("ID: ")))
        elif op == "10": 
            imprimir(repo.amigos_de_amigos(pedir_int("ID: ")))
        elif op == "11":
            a = pedir_int("ID origen: ")
            b = pedir_int("ID destino: ")
            imprimir(repo.camino_mas_corto(a, b))
        elif op == "12":
            imprimir(repo.recomendar_amigos(pedir_int("ID: ")))
        elif op == "13":
            imprimir(repo.recomendar_por_intereses(pedir_int("ID: ")))
        elif op == "0":
            break
        else:
            print(" Opción no válida.")

    close_driver()

if __name__ == "__main__":
    main()