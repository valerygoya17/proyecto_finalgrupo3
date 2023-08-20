from datetime import datetime

import pyodbc
from PySide6 import QtGui
from PySide6.QtCore import QDate
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QMainWindow

from IU.untitled import Ui_TIPO
from datos.estudiante_dao import EstudianteDao
from dominio.Estudiante import Estudiante




class Persona_principal(QMainWindow):

    def __init__(self):
        super(Persona_principal, self).__init__()
        self.iu = Ui_TIPO()
        self.iu.setupUi(self)
        self.iu.stb_estado.showMessage('Bienvenido', 2000)
        self.iu.stb_estado.showMessage("Saludos")
        self.iu.GRABAR.clicked.connect(self.GRABAR)
        self.iu.btn_promedio.clicked.connect(self.promedio)


        self.iu.txt_cedula.setValidator(QtGui.QIntValidator())

        correo_exp = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        validator = QRegularExpressionValidator(correo_exp, self)
        self.iu.txt_email.setValidator(validator)

    def GRABAR(self):
        tipo_persona = self.iu.cb_tipo_persona.currentText()
        if (self.iu.txt_NOMBRE.text() == '' or
            self.iu.txt_APELLIDO.text() == '' or
            len(self.iu.txt_cedula.text()) < 10 or
            self.iu.txt_email.text() == ''):
            # Mostrar un mensaje de advertencia o mostrar un cuadro de diálogo
            pass
        else:
            if tipo_persona == 'Estudiante':
                persona = Estudiante()
                persona.nombre = self.iu.txt_NOMBRE.text()
                persona.apellido = self.iu.txt_APELLIDO.text()
                persona.cedula = self.iu.txt_cedula.text()
                persona.email = self.iu.txt_email.text()
                persona.estatura = self.iu.sp_estatura.text()
                persona.peso = self.iu.sp_peso.text()
                persona.fechanacimiento = self.iu.dateEdit.date().toString('yyyy-MM-dd')
            EstudianteDao.insertar_estudiante(persona)

            self.iu.txt_NOMBRE.setText('')
            self.iu.txt_APELLIDO.setText('')
            self.iu.txt_cedula.setText('')
            self.iu.txt_email.setText('')
            self.iu.sp_estatura.setValue(0)
            self.iu.sp_peso.setValue(0)
            self.iu.dateEdit.setDate(QDate.currentDate())

            self.iu.stb_estado.showMessage('Grabado con éxito.', 2000)


    def calcular_moda(self, lista):
            frecuencias = {}
            max_frecuencia = 0
            moda = []

            for valor in lista:
                if valor in frecuencias:
                    frecuencias[valor] += 1
                else:
                    frecuencias[valor] = 1

                if frecuencias[valor] > max_frecuencia:
                    max_frecuencia = frecuencias[valor]
                    moda = [valor]
                elif frecuencias[valor] == max_frecuencia:
                    moda.append(valor)

            if len(moda) == 1:
                return moda[0]
            else:
                return "No hay moda única"

    def buscar_x_cedula(self):
        cedula = self.ui.txt_cedula.text()
        e = Estudiante(cedula=cedula)
        e = EstudianteDao.seleccionar_por_cedula(e)
        print(e)
        self.ui.txt_nombre.setText(e.nombre)
        self.ui.txt_apellido.setText(e.apellido)
        self.ui.txt_correo.setText(e.correo)
        self.ui.cb_tipo_persona.setCurrentText('Estudiante')

    from datetime import datetime

    def promedio(self):
        estudiantes = EstudianteDao.seleccionar_estudiante()

        suma_estaturas = 0
        edades = []

        for estudiante in estudiantes:
            suma_estaturas += estudiante.estatura

            # Calcular edades a partir de las fechas de nacimiento
            fecha_nacimiento = estudiante.fechanacimiento

            fecha_actual = datetime.now().date()
            edad = fecha_actual.year - fecha_nacimiento.year - (
                    (fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
            edades.append(edad)

        cantidad_estudiantes = len(estudiantes)
        promedio_estatura = suma_estaturas / cantidad_estudiantes
        print(f'EL PROMEDIO DE ESTATURA ES: {promedio_estatura}')

        # Calcular moda, media, mínimo y máximo de las edades
        moda_edades = self.calcular_moda(edades)
        media_edades = sum(edades) / len(edades)
        min_edad = min(edades)
        max_edad = max(edades)

        print(f'MODA DE EDADES: {moda_edades}')
        print(f'MEDIA DE EDADES: {media_edades}')
        print(f'MÍNIMO DE EDADES: {min_edad}')
        print(f'MÁXIMO DE EDADES: {max_edad}')






