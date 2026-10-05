from models import CAMPOS_ESTUDIANTE
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import (
    crear_estudiante, obtener_todos, obtener_por_id, buscar_Estudiantes,
    actualizar_estudiante, eliminar_Estudiante, agregar_nota, materias_ofertadas, estudiantes_en_comun
)


def pausa():
    input("\nPresione Enter para continuar...")


def mostrar_estudiantes(estudiantes):
    print(
        f"{'ID':<5}{'NOMBRE':<25}{'EMAIL':<30}{'CARNET':<15}"
        f"{'PROMEDIO':<10}"
    )
    print("-" * 85)

    for estudiante in estudiantes:
        print(
            f"{estudiante.id:<5}"
            f"{estudiante.obtener_nombre_completo():<25}"
            f"{estudiante.email:<30}"
            f"{estudiante.carnet:<15}"
            f"{estudiante.obtener_promedio():<10}"
        )

    print("-" * 85)
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")


# ---------- C · CREAR ----------

def opcion_crear():
    imprimir_titulo("CREAR NUEVO ESTUDIANTE")

    datos = {}

    for campo in CAMPOS_ESTUDIANTE:
        datos[campo] = input(f"{campo.capitalize()}: ")

    exito, mensaje = crear_estudiante(datos)

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()


# ---------- R · LEER TODOS ----------

def opcion_ver_todos():
    imprimir_titulo("LISTA DE ESTUDIANTES")

    estudiantes = obtener_todos()

    if not estudiantes:
        imprimir_info(
            "Todavía no hay estudiantes. "
            "Use la opción 1 para crear el primero."
        )
    else:
        mostrar_estudiantes(estudiantes)

    pausa()


# ---------- S · BUSCAR ----------

def opcion_buscar():
    imprimir_titulo("BUSCAR ESTUDIANTE")

    termino = input("Nombre, apellido, email o carnet: ")
    encontrados = buscar_Estudiantes(termino)

    if not encontrados:
        imprimir_info(
            f"Ningún estudiante coincide con '{termino}'."
        )
    else:
        mostrar_estudiantes(encontrados)

    pausa()


# ---------- R · LEER UNO ----------

def opcion_ver_por_id():
    imprimir_titulo("VER ESTUDIANTE POR ID")

    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        pausa()
        return

    estudiante = obtener_por_id(id_estudiante)

    if estudiante is None:
        imprimir_error(
            f"No existe un estudiante con id {id_estudiante}"
        )
    else:
        print(f"ID: {estudiante.id}")
        print(f"Nombre: {estudiante.obtener_nombre_completo()}")
        print(f"Email: {estudiante.email}")
        print(f"Carnet: {estudiante.carnet}")
        print(f"Materias: {', '.join(sorted(estudiante.materias)) or 'Ninguna'}")
        print(f"Promedio: {estudiante.obtener_promedio()}")

    pausa()


# ---------- U · ACTUALIZAR ----------

def opcion_actualizar():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")

    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        pausa()
        return

    estudiante = obtener_por_id(id_estudiante)

    if estudiante is None:
        imprimir_error(
            f"No existe un estudiante con id {id_estudiante}"
        )
        pausa()
        return

    print("Deje vacío un campo si no desea modificarlo.\n")

    cambios = {}

    for campo in CAMPOS_ESTUDIANTE:
        valor = input(
            f"{campo.capitalize()} [{getattr(estudiante, campo)}]: "
        ).strip()

        if valor:
            cambios[campo] = valor

    exito, mensaje = actualizar_estudiante(id_estudiante, cambios)

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()


# ---------- D · ELIMINAR ----------

def opcion_eliminar():
    imprimir_titulo("ELIMINAR ESTUDIANTE")

    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        pausa()
        return

    estudiante = obtener_por_id(id_estudiante)

    if estudiante is None:
        imprimir_error(
            f"No existe un estudiante con id {id_estudiante}"
        )
        pausa()
        return

    pregunta = (
        f"¿Eliminar a {estudiante.obtener_nombre_completo()}?"
    )

    if confirmar(pregunta):
        exito, mensaje = eliminar_Estudiante(id_estudiante)

        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)
    else:
        imprimir_info("Operación cancelada")

    pausa()


# ---------- EXTRA · AGREGAR NOTA ----------

def opcion_agregar_nota():
    imprimir_titulo("AGREGAR NOTA")

    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        pausa()
        return

    materia = input("Materia: ")

    try:
        nota = float(input("Nota (0-20): "))
    except ValueError:
        imprimir_error("La nota debe ser un número entre 0 y 20")
        pausa()
        return

    exito, mensaje = agregar_nota(
        id_estudiante,
        materia,
        nota,
    )

    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)

    pausa()


# ---------- EXTRA · PROMEDIO ----------

def opcion_ver_promedio():
    imprimir_titulo("VER PROMEDIO")

    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        pausa()
        return

    estudiante = obtener_por_id(id_estudiante)

    if estudiante is None:
        imprimir_error(
            f"No existe un estudiante con id {id_estudiante}"
        )
    else:
        print(
            f"Estudiante: {estudiante.obtener_nombre_completo()}"
        )
        print(f"Promedio: {estudiante.obtener_promedio()}")

        if estudiante.notas:
            print("\nNotas por materia:")

            for materia, notas in estudiante.notas.items():
                print(f"- {materia}: {notas}")

    pausa()


# ---------- EXTRA · MATERIAS EN COMÚN ----------

def opcion_materias_en_comun():
    imprimir_titulo("MATERIAS EN COMÚN")

    try:
        id_a = int(input("Id del primer estudiante: "))
        id_b = int(input("Id del segundo estudiante: "))
    except ValueError:
        imprimir_error("Los id deben ser números enteros")
        pausa()
        return

    materias = estudiantes_en_comun(id_a, id_b)

    if materias is None:
        imprimir_error("Uno o ambos estudiantes no existen")
    elif not materias:
        imprimir_info("No tienen materias en común")
    else:
        imprimir_info("Materias en común:")
        for materia in sorted(materias):
            print(f"- {materia}")

    pausa()


# ---------- EXTRA · MATERIAS OFERTADAS ----------

def opcion_materias_ofertadas():
    imprimir_titulo("MATERIAS OFERTADAS")

    materias = materias_ofertadas()

    if not materias:
        imprimir_info("Todavía no hay materias registradas.")
    else:
        for materia in sorted(materias):
            print(f"- {materia}")

    pausa()


OPCIONES = {
    "1": opcion_crear,
    "2": opcion_ver_todos,
    "3": opcion_buscar,
    "4": opcion_ver_por_id,
    "5": opcion_actualizar,
    "6": opcion_eliminar,
    "7": opcion_agregar_nota,
    "8": opcion_ver_promedio,
    "9": opcion_materias_en_comun,
    "10": opcion_materias_ofertadas,
}


def mostrar_menu():
    print("1. Crear estudiante")
    print("2. Ver todos los estudiantes")
    print("3. Buscar estudiante")
    print("4. Ver estudiante por ID")
    print("5. Actualizar estudiante")
    print("6. Eliminar estudiante")
    print("7. Agregar nota")
    print("8. Ver promedio")
    print("9. Materias en común")
    print("10. Ver materias ofertadas")
    print("0. Salir")


def main():
    while True:
        imprimir_titulo("SISTEMA DE ESTUDIANTES")
        mostrar_menu()

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "0":
            imprimir_info("Programa finalizado.")
            break

        funcion = OPCIONES.get(opcion)

        if funcion:
            funcion()
        else:
            imprimir_error("Opción no válida")
            pausa()

if __name__ == "__main__":
    # =====================================================================
    # PRUEBAS DEL PROGRAMA  ·  se ejecutan con:  python main.py
    # (el menú normal queda en:  python main.py --menu)
    #
    # Idea: cada prueba llama a probar("qué espero", condición).
    # Si la condición es True se imprime ✓, si es False se imprime ✗.
    # Las pruebas usan un archivo aparte (data/prueba_estudiantes.json)
    # para NO tocar tus datos reales de data/estudiantes.json.
    # =====================================================================
    import os
    import sys
    import io
    import builtins
    import contextlib

    import views
    from models import Estudiante
    from shared import herramientas
    from shared.json_manager import GestorJSON

    if "--menu" in sys.argv:
        main()
        sys.exit()

    resultados = []          # aquí guardamos True/False de cada prueba

    def probar(descripcion, condicion):
        resultados.append(condicion)
        print(("  ✓ " if condicion else "  ✗ FALLÓ: ") + descripcion)

    # Archivo de pruebas: empezamos siempre desde cero
    ARCHIVO = "data/prueba_estudiantes.json"
    gestor_real = views.gestor
    views.gestor = GestorJSON(ARCHIVO)
    if os.path.exists(ARCHIVO):
        os.remove(ARCHIVO)

    # ------------------------------------------------------------------
    print("\n1) MODELO: la clase Estudiante (models.py)")
    est = Estudiante(1, "Ana", "Pérez", "ana@x.com", "EST1")
    probar("nombre completo = 'Ana Pérez'", est.obtener_nombre_completo() == "Ana Pérez")
    probar("sin notas el promedio es 0", est.obtener_promedio() == 0)

    est.agregar_nota("Matemática", 18)
    est.agregar_nota("Matemática", 20)
    est.agregar_nota("Inglés", 16)
    probar("las notas se agrupan por materia (diccionario de listas)",
           est.notas == {"Matemática": [18, 20], "Inglés": [16]})
    probar("promedio de 18, 20 y 16 = 18.0", est.obtener_promedio() == 18.0)

    est.inscribir_materia("Inglés")            # ya estaba inscrito
    probar("el set no repite materias", est.materias == {"Matemática", "Inglés"})

    probar("al guardar, las materias pasan a lista ordenada",
           est.a_diccionario()["materias"] == ["Inglés", "Matemática"])
    copia = Estudiante.desde_diccionario(est.a_diccionario())
    probar("al leer, las materias vuelven a ser un set",
           isinstance(copia.materias, set) and copia.materias == est.materias)

    luis = Estudiante(2, "Luis", "García", "luis@x.com", "EST2", materias={"Inglés", "Historia"})
    probar("materias en común (intersección) = {'Inglés'}",
           est.materias_en_comun(luis) == {"Inglés"})

    # ------------------------------------------------------------------
    print("\n2) JSON: el gestor de archivos (shared/json_manager.py)")
    gestor_prueba = GestorJSON("data/prueba_json.json")
    probar("si el archivo no existe, leer() devuelve lista vacía", gestor_prueba.leer() == [])
    probar("guardar() devuelve True", gestor_prueba.guardar([{"id": 1, "nombre": "Ñandú"}]) is True)
    probar("leer() devuelve lo mismo que se guardó (con ñ y tildes)",
           gestor_prueba.leer() == [{"id": 1, "nombre": "Ñandú"}])
    probar("guardar() un set falla (JSON no conoce los sets)",
           gestor_prueba.guardar([{"x": {1, 2}}]) is False)
    with open("data/prueba_json.json", "w", encoding="utf-8") as f:
        f.write("esto no es json")
    probar("si el archivo está dañado, leer() devuelve lista vacía", gestor_prueba.leer() == [])
    os.remove("data/prueba_json.json")

    # ------------------------------------------------------------------
    print("\n3) CREAR (Create)")
    exito, mensaje = views.crear_estudiante(
        {"nombre": "Ana", "apellido": "Pérez", "email": "ana@x.com", "carnet": "EST1"})
    probar("crear el estudiante 1", exito)
    exito, mensaje = views.crear_estudiante(
        {"nombre": "Luis", "apellido": "García", "email": "luis@x.com", "carnet": "EST2"})
    probar("crear el estudiante 2", exito and "id 2" in mensaje)
    exito, mensaje = views.crear_estudiante(
        {"nombre": " Marta ", "apellido": "Ruiz", "email": "marta@x.com", "carnet": " EST3 "})
    probar("crear con espacios de sobra", exito)
    probar("los espacios sobrantes se limpian", views.obtener_por_id(3).carnet == "EST3")

    exito, mensaje = views.crear_estudiante(
        {"nombre": "X", "apellido": "Y", "email": "otro@x.com", "carnet": "EST1"})
    probar("carnet repetido -> se rechaza", not exito)
    exito, mensaje = views.crear_estudiante(
        {"nombre": "X", "apellido": "Y", "email": "otro@x.com", "carnet": "est1"})
    probar("carnet repetido con otras mayúsculas -> se rechaza", not exito)
    exito, mensaje = views.crear_estudiante({"nombre": "Solo nombre"})
    probar("faltan campos obligatorios -> se rechaza", not exito)
    exito, mensaje = views.crear_estudiante(
        {"nombre": "X", "apellido": "Y", "email": "sin-arroba", "carnet": "EST9"})
    probar("email con formato inválido -> se rechaza", not exito)
    probar("los intentos fallidos no guardaron nada (siguen 3)", len(views.obtener_todos()) == 3)

    # ------------------------------------------------------------------
    print("\n4) LEER (Read)")
    todos = views.obtener_todos()
    probar("obtener_todos() devuelve 3 objetos Estudiante",
           len(todos) == 3 and isinstance(todos[0], Estudiante))
    probar("obtener_por_id(2) devuelve a Luis", views.obtener_por_id(2).nombre == "Luis")
    probar("obtener_por_id(99) devuelve None", views.obtener_por_id(99) is None)

    # ------------------------------------------------------------------
    print("\n5) BUSCAR (Search)")
    probar("buscar 'pér' (nombre con tilde) encuentra 1", len(views.buscar_Estudiantes("pér")) == 1)
    probar("buscar 'EST2' (por carnet) encuentra a Luis",
           views.buscar_Estudiantes("EST2")[0].nombre == "Luis")
    probar("buscar 'x.com' (parte del email) encuentra 3", len(views.buscar_Estudiantes("x.com")) == 3)
    probar("buscar 'zzzz' no encuentra nada", views.buscar_Estudiantes("zzzz") == [])
    probar("buscar texto vacío devuelve lista vacía", views.buscar_Estudiantes("   ") == [])
    probar("si coincide en 2 campos, el estudiante no sale repetido",
           len(views.buscar_Estudiantes("ana")) == 1)

    # ------------------------------------------------------------------
    print("\n6) ACTUALIZAR (Update)")
    exito, mensaje = views.actualizar_estudiante(1, {"nombre": "Anita"})
    probar("cambiar el nombre", exito and views.obtener_por_id(1).nombre == "Anita")
    probar("los demás campos no cambian", views.obtener_por_id(1).email == "ana@x.com")
    exito, mensaje = views.actualizar_estudiante(1, {"carnet": "EST1"})
    probar("dejar su propio carnet es válido", exito)
    exito, mensaje = views.actualizar_estudiante(2, {"carnet": "est1"})
    probar("usar el carnet de otro estudiante -> se rechaza", not exito)
    exito, mensaje = views.actualizar_estudiante(1, {"email": "malo"})
    probar("email inválido -> se rechaza", not exito)
    exito, mensaje = views.actualizar_estudiante(1, {"nombre": "   "})
    probar("campo obligatorio vacío -> se rechaza", not exito)
    exito, mensaje = views.actualizar_estudiante(1, {"inventado": "x"})
    probar("campo que no existe -> se rechaza", not exito)
    exito, mensaje = views.actualizar_estudiante(1, {})
    probar("sin ningún cambio -> se rechaza", not exito)
    exito, mensaje = views.actualizar_estudiante(99, {"nombre": "X"})
    probar("id que no existe -> se rechaza", not exito)

    # ------------------------------------------------------------------
    print("\n7) NOTAS, PROMEDIO Y MATERIAS")
    probar("agregar nota 18", views.agregar_nota(1, "Matemática", 18)[0])
    probar("agregar nota 20 (el máximo)", views.agregar_nota(1, "Matemática", 20)[0])
    probar("agregar nota 16 en otra materia", views.agregar_nota(1, "Inglés", 16)[0])
    probar("agregar nota 15 al estudiante 2", views.agregar_nota(2, "Matemática", 15)[0])
    probar("agregar nota 0 (el mínimo)", views.agregar_nota(2, "Historia", 0)[0])
    probar("nota 21 -> se rechaza", not views.agregar_nota(1, "Física", 21)[0])
    probar("nota -1 -> se rechaza", not views.agregar_nota(1, "Física", -1)[0])
    probar("nota 'abc' -> se rechaza", not views.agregar_nota(1, "Física", "abc")[0])
    probar("materia vacía -> se rechaza", not views.agregar_nota(1, "   ", 10)[0])
    probar("estudiante que no existe -> se rechaza", not views.agregar_nota(99, "Física", 10)[0])
    probar("las notas rechazadas no se guardaron",
           views.obtener_por_id(1).notas == {"Matemática": [18, 20], "Inglés": [16]})
    probar("una nota rechazada tampoco inscribe la materia",
           "Física" not in views.obtener_por_id(1).materias)

    probar("promedio del estudiante 1 = 18.0", views.obtener_por_id(1).obtener_promedio() == 18.0)
    probar("promedio del estudiante 2 = 7.5", views.obtener_por_id(2).obtener_promedio() == 7.5)
    probar("promedio de quien no tiene notas = 0", views.obtener_por_id(3).obtener_promedio() == 0)

    probar("materias_ofertadas() junta todas sin repetir",
           views.materias_ofertadas() == {"Matemática", "Inglés", "Historia"})
    probar("estudiantes_en_comun(1, 2) = {'Matemática'}",
           views.estudiantes_en_comun(1, 2) == {"Matemática"})
    probar("si no comparten materias, devuelve set vacío", views.estudiantes_en_comun(1, 3) == set())
    probar("si un id no existe, devuelve None", views.estudiantes_en_comun(1, 99) is None)

    # ------------------------------------------------------------------
    print("\n8) PERSISTENCIA: ¿se guarda y se vuelve a leer bien?")
    releido = views.obtener_por_id(1)         # esto lee el archivo JSON otra vez
    probar("las materias vuelven a ser un set", isinstance(releido.materias, set))
    probar("no se perdieron ni las notas ni las materias",
           releido.notas["Matemática"] == [18, 20] and releido.materias == {"Inglés", "Matemática"})

    # ------------------------------------------------------------------
    print("\n9) ELIMINAR (Delete)")
    exito, mensaje = views.eliminar_Estudiante(3)
    probar("eliminar al estudiante 3", exito and views.obtener_por_id(3) is None)
    probar("quedan 2 estudiantes", len(views.obtener_todos()) == 2)
    exito, mensaje = views.eliminar_Estudiante(3)
    probar("eliminar de nuevo al 3 -> se rechaza", not exito)

    # ------------------------------------------------------------------
    print("\n10) VISTA: el menú (main.py) con respuestas simuladas")
    os.remove(ARCHIVO)                         # archivo limpio para esta parte

    # Estas son las "teclas" que el usuario escribiría, en orden.
    # Cada "" es un Enter para el "Presione Enter para continuar".
    respuestas = [
        "1", "Sol", "Ruiz", "sol@x.com", "EST10", "",    # opción 1: crear
        "2", "",                                          # opción 2: ver todos
        "3", "sol", "",                                   # opción 3: buscar
        "3", "zzz", "",                                   # opción 3: sin resultados
        "4", "abc", "",                                   # opción 4: id inválido
        "7", "1", "Matemática", "18", "",                 # opción 7: agregar nota
        "8", "1", "",                                     # opción 8: ver promedio
        "99", "",                                         # opción que no existe
        "0",                                              # salir
    ]
    builtins_input = builtins.input
    limpiar_original = herramientas.limpiar_pantalla
    builtins.input = lambda texto="": respuestas.pop(0)    # input() lee de la lista
    herramientas.limpiar_pantalla = lambda: None           # no borrar la consola
    pantalla = io.StringIO()
    try:
        with contextlib.redirect_stdout(pantalla):         # guardamos lo que se imprime
            main()
        error = None
    except Exception as e:
        error = e
    finally:
        builtins.input = builtins_input
        herramientas.limpiar_pantalla = limpiar_original
    texto = pantalla.getvalue()

    probar("el menú corrió completo sin errores", error is None)
    probar("usó todas las respuestas (ninguna sobró)", respuestas == [])
    probar("el menú muestra las opciones", "Crear estudiante" in texto)
    probar("ver todos muestra a 'Sol Ruiz'", "Sol Ruiz" in texto)
    probar("buscar 'sol' muestra 'Total: 1'", "Total: 1 estudiante(s)" in texto)
    probar("buscar 'zzz' avisa que no hay coincidencias",
           "Ningún estudiante coincide con 'zzz'" in texto)
    probar("id 'abc' muestra el error", "El id debe ser un número entero" in texto)
    probar("ver promedio muestra 18.0", "Promedio: 18.0" in texto)
    probar("opción inexistente muestra el error", "Opción no válida" in texto)
    probar("al salir muestra 'Programa finalizado.'", "Programa finalizado." in texto)

    # ------------------------------------------------------------------
    # Limpieza: borramos el archivo de pruebas y devolvemos el gestor real
    if os.path.exists(ARCHIVO):
        os.remove(ARCHIVO)
    views.gestor = gestor_real

    # Resumen
    total = len(resultados)
    buenas = resultados.count(True)
    print("\n" + "=" * 55)
    if buenas == total:
        print(f"✓ TODAS LAS PRUEBAS PASARON: {buenas}/{total}")
    else:
        print(f"✗ FALLARON {total - buenas}. Pasaron {buenas}/{total}")
    print("=" * 55)