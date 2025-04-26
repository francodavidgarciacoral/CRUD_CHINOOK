# Nom Cognoms: Franco David Garcia Coral
import psycopg 

# FUNCIÓN DE CONEXIÓN A LA BASE DE DATOS
def connect_db():
    connection = """
                    dbname=chinook_v2
                    user=postgres 
                    password=1234
                    host=localhost
                    port=5432
                    """
    return psycopg.connect(connection)

# FUNCIONES DE OPERACIONES
def consulta_art(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT 'ID: '||artist_id||', NOM: '||name as artists FROM artist")
    print(cursor.fetchall())

def consulta_nom(conn):
    str_art = input('\nBuscar en artistas: ')
    while len(str_art) < 2:
        print('\nIntroduce al menos 2 caracteres.')
        str_art = input('Buscar en artistas: ')
    cursor = conn.cursor()
    cursor.execute("SELECT 'ID: '||artist_id||', NOM: '||name as artists FROM artist WHERE name LIKE %s", ('%' + str_art + '%',))
    print(cursor.fetchall())
    
def consulta_alb(conn):
    str_alb = input('\nBuscar en artistas: ')
    while len(str_alb) < 2:
        print('\nIntroduce al menos 2 caracteres.')
        str_alb = input('Buscar en artistas: ')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 'ID_ALBUM:' || a.album_id || ', NOM_ALBUM:' || a.title || ', NOM_ARTISTA:' || r.name 
        FROM album a 
        JOIN artist r ON a.artist_id = r.artist_id 
        WHERE r.name LIKE %s 
        LIMIT 5
    """, (str_alb + '%',))
    print(cursor.fetchall())

def agregar_art(conn):
    str_agr = input('\nNombre del artista: ')
    while len(str_agr) < 2:
        print('\nIntroduce al menos 2 caracteres.')
        str_agr = input('Nombre del artista: ')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO artist(artist_id, name) VALUES ((SELECT MAX(artist_id) FROM artist) + 1, %s)", (str_agr,))
    conn.commit()
    print('Artista agregado correctamente.')

def modificar_art(conn):
    str_mod_old = input('\nNombre actual del artista: ')
    while len(str_mod_old) < 2:
        print('\nIntroduce al menos 2 caracteres.')
        str_mod_old = input('Nombre actual del artista: ')
    str_mod_new = input('\nNuevo nombre del artista: ')
    while len(str_mod_new) < 2:
        print('\nIntroduce al menos 2 caracteres.')
        str_mod_new = input('Nuevo nombre del artista: ')
    cursor = conn.cursor()
    cursor.execute("UPDATE artist SET name = %s WHERE name = %s", (str_mod_new, str_mod_old))
    conn.commit()
    print('\nArtista actualizado.')

def borrar_art(conn):
    str_del = input('\nNombre del artista a borrar: ')
    while len(str_del) < 2:
        print('\nIntroduce al menos 2 caracteres.')
        str_del = input('Nombre del artista a borrar: ')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM artist WHERE name = %s", (str_del,))
    conn.commit()
    print('Artista eliminado.')

def exit(conn):
    print('\n¡Adiós!')
    conn.close()

# MENÚ PRINCIPAL
def menu():
    conn = connect_db()
    while True:
        print("\nMenú Principal")
        print("1 - Consultar todos los artistas")
        print("2 - Consultar artistas por nombre")
        print("3 - Consultar los 5 primeros álbumes por artista")
        print("4 - Añadir artista")
        print("5 - Modificar nombre de artista")
        print("6 - Borrar artista")
        print("7 - Salir")
        opcion = input("Selecciona una opción: ")
        
        if not opcion.isdigit():
            print("\n¡Error! Introduce un número.")
            continue
            
        opcion = int(opcion)
        
        if opcion == 7:
            exit(conn)
            break
        elif 1 <= opcion <= 6:
            { 
                1: consulta_art,
                2: consulta_nom,
                3: consulta_alb,
                4: agregar_art,
                5: modificar_art,
                6: borrar_art
            }[opcion](conn)
        else:
            print("\nOpción no válida.")

# EJECUCIÓN
if __name__ == "__main__":
    menu()