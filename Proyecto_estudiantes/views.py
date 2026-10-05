from models import Estudiante, CAMPOS_ESTUDIANTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

gestor = GestorJSON("data/estudiantes.json")

# TUPLAS de configuración: fijas, nadie las modifica en tiempo de ejecución
CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")


# ===================== AYUDAS INTERNAS =====================

def carnets_registrados(excepto_id=None):
    """CONJUNTO con los carnets ya usados."""
    return {
        registro["carnet"].lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


def siguiente_id():
    ids = [registro["id"] for registro in gestor.leer()]
    return max(ids) + 1 if ids else 1


# ===================== C · CREATE =====================

def crear_estudiante(datos):
    """datos: diccionario con las claves de CAMPOS_ESTUDIANTE. Devuelve (exito, mensaje)."""
    try:
        # 1) Normalizo: un diccionario con todos los campos, sin espacios sobrantes
        valores = {campo: str(datos.get(campo, "")).strip() for campo in CAMPOS_ESTUDIANTE}

        # 2) Reviso obligatorios recorriendo la TUPLA
        faltantes = [campo for campo in CAMPOS_OBLIGATORIOS if not valores[campo]]
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        # 3) Formato del email
        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no tiene un formato válido"

        # 4) Duplicado: búsqueda instantánea dentro del CONJUNTO
        if valores["carnet"].lower() in carnets_registrados():
            return False, "Ese email ya está registrado"

        # 5) Creo el objeto del Modelo. ** convierte el diccionario en argumentos
        estudiante = Estudiante(siguiente_id(), **valores)

        # 6) Agrego a la LISTA y guardo
        registros = gestor.leer()
        registros.append(estudiante.a_diccionario())
        if not gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"

        return True, f"estudiante {estudiante.obtener_nombre_completo()} creado con id {estudiante.id}"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== R · READ =====================

def obtener_todos():
    """LISTA de objetos estudiante."""
    return [Estudiante.desde_diccionario(registro) for registro in gestor.leer()]


def obtener_por_id(id_Estudiante):
    for estudiante in obtener_todos():
        if estudiante.id == id_Estudiante:
            return estudiante
    return None


# ===================== S · SEARCH =====================

def buscar_Estudiantes(termino):
    """Búsqueda lineal: revisa registro por registro los campos de CAMPOS_BUSCABLES."""
    termino = termino.strip().lower()
    if not termino:
        return []

    encontrados = []
    for registro in gestor.leer():
        for campo in CAMPOS_BUSCABLES:                 # recorro la TUPLA de campos
            if termino in str(registro.get(campo, "")).lower():
                encontrados.append(Estudiante.desde_diccionario(registro))
                break                                   # ya coincidió: paso al siguiente estudiante
    return encontrados


# ===================== U · UPDATE =====================

def actualizar_estudiante(id_estudiante, cambios):
    """Actualiza únicamente los campos recibidos en cambios."""
    try:
        desconocidos = set(cambios) - set(CAMPOS_ESTUDIANTE)

        if desconocidos:
            return False, (
                f"Campos no válidos: {', '.join(sorted(desconocidos))}"
            )

        if not cambios:
            return False, "No se indicó ningún cambio"

        valores = {
            campo: str(valor).strip()
            for campo, valor in cambios.items()
        }

        for campo in CAMPOS_OBLIGATORIOS:
            if campo in valores and not valores[campo]:
                return False, f"El campo {campo} no puede estar vacío"

        if "email" in valores:
            if not es_email_valido(valores["email"]):
                return False, "El email no tiene un formato válido"

        if "carnet" in valores:
            if valores["carnet"].lower() in carnets_registrados(
                excepto_id=id_estudiante
            ):
                return False, "Ese carnet ya lo usa otro estudiante"

        registros = gestor.leer()
        posicion = None

        for indice, registro in enumerate(registros):
            if registro["id"] == id_estudiante:
                posicion = indice
                break

        if posicion is None:
            return False, f"No existe un estudiante con id {id_estudiante}"

        registros[posicion].update(valores)

        if not gestor.guardar(registros):
            return False, "No se pudo guardar la actualización"

        return (
            True,
            f"Estudiante {id_estudiante} actualizado "
            f"({len(cambios)} campo/s)",
        )

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== D · DELETE =====================

def eliminar_Estudiante(id_Estudiante):
    registros = gestor.leer()
    # Construyo una LISTA NUEVA sin ese registro: nunca borro mientras recorro
    quedan = [registro for registro in registros if registro["id"] != id_Estudiante]

    if len(quedan) == len(registros):
        return False, f"No existe un estudiante con id {id_Estudiante}"

    if not gestor.guardar(quedan):
            return False, "No se pudo guardar el archivo"

    gestor.guardar(quedan)
    return True, f"estudiante {id_Estudiante} eliminado"


# ===================== EXTRA: estadísticas con conjuntos =====================

def agregar_nota(id_estudiante, materia, nota):
    """Agrega una nota válida entre 0 y 20."""
    try:
        estudiante = obtener_por_id(id_estudiante)

        if estudiante is None:
            return False, f"No existe un estudiante con id {id_estudiante}"

        materia = str(materia).strip()

        if not materia:
            return False, "La materia no puede estar vacía"

        try:
            nota = float(nota)
        except (TypeError, ValueError):
            return False, "La nota debe ser un número entre 0 y 20"

        if nota < 0 or nota > 20:
            return False, "La nota debe estar entre 0 y 20"

        if nota.is_integer():
            nota = int(nota)

        estudiante.agregar_nota(materia, nota)

        registros = gestor.leer()

        for indice, registro in enumerate(registros):
            if registro["id"] == id_estudiante:
                registros[indice] = estudiante.a_diccionario()
                break

        if not gestor.guardar(registros):
            return False, "No se pudo guardar la nota"

        return (
            True,
            f"Nota {nota} agregada en {materia} "
            f"al estudiante {estudiante.obtener_nombre_completo()}",
        )

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== EXTRA · MATERIAS =====================

def materias_ofertadas():
    """CONJUNTO con todas las materias, sin duplicados."""
    materias = set()

    for estudiante in obtener_todos():
        materias.update(estudiante.materias)

    return materias


def estudiantes_en_comun(id_a, id_b):
    """Devuelve el CONJUNTO de materias compartidas por dos estudiantes."""
    estudiante_a = obtener_por_id(id_a)
    estudiante_b = obtener_por_id(id_b)

    if estudiante_a is None or estudiante_b is None:
        return None

    return estudiante_a.materias_en_comun(estudiante_b)
