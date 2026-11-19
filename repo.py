from db import run_query

def crear_restricciones():
    run_query(
        "CREATE CONSTRAINT persona_id IF NOT EXISTS "
        "FOR (p:Persona) REQUIRE p.id IS UNIQUE"
    )
    run_query(
        "CREATE CONSTRAINT interes_nombre IF NOT EXISTS "
        "FOR (i:Interes) REQUIRE i.nombre IS UNIQUE"
    )

def crear_persona(id_, nombre, edad, ciudad):
    return run_query(
        """
        MERGE (p:Persona {id: $id})
        SET p.nombre = $nombre, p.edad = $edad, p.ciudad = $ciudad
        RETURN p.id AS id, p.nombre AS nombre, p.edad AS edad, p.ciudad AS ciudad
        """,
        id=id_, nombre=nombre, edad=edad, ciudad=ciudad,
    )

def crear_amistad(id_a, id_b, desde):
    return run_query(
        """
        MATCH (a:Persona {id: $a}), (b:Persona {id: $b})
        MERGE (a)-[r:AMIGO_DE]-(b)
        SET r.desde = $desde
        RETURN a.nombre AS a, b.nombre AS b, r.desde AS desde
        """,
        a=id_a, b=id_b, desde=desde,
    )

def agregar_interes(id_persona, interes):
    return run_query(
        """
        MATCH (p:Persona {id: $id})
        MERGE (i:Interes {nombre: $interes})
        MERGE (p)-[:INTERESADO_EN]->(i)
        RETURN p.nombre AS persona, i.nombre AS interes
        """,
        id=id_persona, interes=interes,
    )

def actualizar_persona(id_, nombre=None, edad=None, ciudad=None):
    return run_query(
        """
        MATCH (p:Persona {id: $id})
        SET p.nombre = coalesce($nombre, p.nombre),
            p.edad   = coalesce($edad, p.edad),
            p.ciudad = coalesce($ciudad, p.ciudad)
        RETURN p.id AS id, p.nombre AS nombre, p.edad AS edad, p.ciudad AS ciudad
        """,
        id=id_, nombre=nombre, edad=edad, ciudad=ciudad,
    )

def obtener_persona(id_):
    return run_query(
        """
        MATCH (p:Persona {id: $id})
        OPTIONAL MATCH (p)-[:INTERESADO_EN]->(i:Interes)
        RETURN p.id AS id, p.nombre AS nombre, p.edad AS edad,
               p.ciudad AS ciudad, collect(i.nombre) AS intereses
        """,
        id=id_,
    )

def listar_personas():
    return run_query(
        """
        MATCH (p:Persona)
        RETURN p.id AS id, p.nombre AS nombre, p.edad AS edad, p.ciudad AS ciudad
        ORDER BY p.id
        """
    )

def eliminar_persona(id_):
    """Borra la persona y todas sus relaciones."""
    return run_query(
        """
        MATCH (p:Persona {id: $id})
        DETACH DELETE p
        RETURN count(p) AS eliminados
        """,
        id=id_,
    )

def eliminar_amistad(id_a, id_b):
    return run_query(
        """
        MATCH (a:Persona {id: $a})-[r:AMIGO_DE]-(b:Persona {id: $b})
        DELETE r
        RETURN count(r) AS eliminadas
        """,
        a=id_a, b=id_b,
    )

def amigos_directos(id_):
    """Vecinidad de 1 salto."""
    return run_query(
        """
        MATCH (p:Persona {id: $id})-[:AMIGO_DE]-(amigo:Persona)
        RETURN amigo.id AS id, amigo.nombre AS nombre, amigo.ciudad AS ciudad
        ORDER BY amigo.nombre
        """,
        id=id_,
    )

def amigos_de_amigos(id_):
    """Vecinidad de 2 saltos, excluyendo a la persona y a sus amigos directos."""
    return run_query(
        """
        MATCH (yo:Persona {id: $id})-[:AMIGO_DE*2]-(fof:Persona)
        WHERE fof <> yo AND NOT (yo)-[:AMIGO_DE]-(fof)
        RETURN DISTINCT fof.id AS id, fof.nombre AS nombre, fof.ciudad AS ciudad
        ORDER BY fof.nombre
        """,
        id=id_,
    )

def camino_mas_corto(id_a, id_b):
    """Camino más corto entre dos personas."""
    return run_query(
        """
        MATCH (a:Persona {id: $a}), (b:Persona {id: $b})
        MATCH ruta = shortestPath((a)-[:AMIGO_DE*..10]-(b))
        RETURN [n IN nodes(ruta) | n.nombre] AS camino,
        length(ruta) AS saltos
        """,
        a=id_a, b=id_b,
    )

def recomendar_amigos(id_):
    """Recomienda personas por amigos en común (ordenado por cantidad)."""
    return run_query(
        """
        MATCH (yo:Persona {id: $id})-[:AMIGO_DE]-(comun:Persona)-[:AMIGO_DE]-(rec:Persona)
        WHERE rec <> yo AND NOT (yo)-[:AMIGO_DE]-(rec)
        RETURN rec.id AS id, rec.nombre AS nombre,
            count(DISTINCT comun) AS amigos_en_comun,
            collect(DISTINCT comun.nombre) AS via
        ORDER BY amigos_en_comun DESC, rec.nombre
        LIMIT 5
        """,
        id=id_,
    )

def recomendar_por_intereses(id_):
    """Recomienda personas con intereses en común que aún no son amigos."""
    return run_query(
        """
        MATCH (yo:Persona {id: $id})-[:INTERESADO_EN]->(i:Interes)<-[:INTERESADO_EN]-(rec:Persona)
        WHERE rec <> yo AND NOT (yo)-[:AMIGO_DE]-(rec)
        RETURN rec.id AS id, rec.nombre AS nombre,
            count(i) AS intereses_comunes,
            collect(i.nombre) AS intereses
        ORDER BY intereses_comunes DESC, rec.nombre
        LIMIT 5
        """,
        id=id_,
    )