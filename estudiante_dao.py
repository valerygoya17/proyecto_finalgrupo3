import pyodbc

from datos.conexion import Conexion
from dominio.Estudiante import Estudiante

class EstudianteDao:
    _INSERTAR = "INSERT INTO Estudiantes (cedula, nombre, apellido, email, carrera, activo, estatura, peso, fechanacimiento) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    _SELECCIONAR = "select id, cedula, nombre, apellido, email, carrera, activo, estatura, peso, fechanacimiento from Estudiantes "


    @classmethod
    def insertar_estudiante(cls, estudiante):
        try:
            with Conexion.obtenerConexion() as conn:
                cursor = conn.cursor()
                datos = (estudiante.cedula, estudiante.nombre, estudiante.apellido, estudiante.email,
                         estudiante.carrera, estudiante.activo, estudiante.estatura, estudiante.peso, estudiante.fechanacimiento)
                cursor.execute(cls._INSERTAR, datos)
                conn.commit()
        except pyodbc.IntegrityError as e:
            print("Error de integridad en la base de datos:", e)
        except pyodbc.ProgrammingError as e:
            print("Error de programación en la base de datos:", e)



    @classmethod
    def seleccionar_estudiante(cls):
            lista_estudiantes = []
            try:
                with Conexion.obtenerCursor() as cursor:
                    resultado = cursor.execute(cls._SELECCIONAR)
                    for tupla_estudiante in resultado.fetchall():
                        estudiante = Estudiante()
                        estudiante.id = tupla_estudiante[0]
                        estudiante.cedula = tupla_estudiante[1]
                        estudiante.nombre = tupla_estudiante[2]
                        estudiante.apellido = tupla_estudiante[3]
                        estudiante.email = tupla_estudiante[4]
                        estudiante.carrera = tupla_estudiante[5]
                        estudiante.activo = tupla_estudiante[6]
                        estudiante.estatura = tupla_estudiante[7]
                        estudiante.peso = tupla_estudiante[8]
                        estudiante.fechanacimiento = tupla_estudiante[9]
                        lista_estudiantes.append(estudiante)
            except Exception as e:
                print(f"Error al seleccionar estudiantes: {e}")
            return lista_estudiantes




if __name__=='__main__':
    e1 = Estudiante()
    e1.cedula = '0214586321'
    e1.nombre = 'APOLO'
    e1.apellido = 'Cruz'
    e1.email = 'apoloruz@gmail.com'
    e1.carrera = 'admi'
    e1.activo = True
    e1.estatura = 170  # Agrega la estatura, peso y fechanacimiento
    e1.peso = 70
    e1.fechanacimiento = '2000-01-01'
    estudiantes = EstudianteDao.seleccionar_estudiante()
    for estudiante in estudiantes:
        print(estudiante)
    if __name__ == '__main__':
        try:
            estudiantes = EstudianteDao.seleccionar_estudiante()
            if estudiantes is list:
                print("No se pudieron recuperar estudiantes.")
            else:
                cantidad_estudiante = len(estudiantes)
                print(f"Cantidad de estudiantes: {cantidad_estudiante}")
                for estudiante in estudiantes:
                    print(estudiante)
        except Exception as e:
            print(f"Error al seleccionar estudiantes: {e}")




