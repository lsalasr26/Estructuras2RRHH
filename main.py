import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDateEdit, QGridLayout, QLabel, QLineEdit, QSpinBox, QPushButton, QMessageBox
from PyQt5.QtCore import QDate, Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sistema de calculo de salario Bisemanal de RRHH')
        self.setFixedSize(1000, 270) 
        self.initUI()
    

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QGridLayout(central_widget)

        # Configurar el campo de fecha inicial
        self.start_date_edit = QDateEdit(calendarPopup=True)
        self.start_date_edit.setDate(QDate.currentDate())  
        self.start_date_edit.setFixedWidth(100) 
        #Añadir el campo
        self.layout.addWidget(QLabel("Fecha de inicio"), 0, 0)
        self.layout.itemAtPosition(0, 0).widget().setFixedWidth(100)
        self.layout.addWidget(self.start_date_edit, 0, 1) 
        
        # Configurar el campo de fecha final
        self.end_date_edit = QDateEdit(calendarPopup=True)
        self.end_date_edit.setDate(self.start_date_edit.date().addDays(13))
        self.end_date_edit.setFixedWidth(100)
        self.end_date_edit.setEnabled(False)  
        self.start_date_edit.dateChanged.connect(self.update_end_date)
        #Añadir el campo
        self.layout.addWidget(QLabel("Fecha de fin"), 0, 2)
        self.layout.itemAtPosition(0, 2).widget().setFixedWidth(100)
        self.layout.addWidget(self.end_date_edit, 0, 3)
        self.end_date_edit.setStyleSheet("QDateEdit { color: black; }")
       
        # Configurar el campo horas extra
        self.number_extra = QSpinBox()
        self.number_extra.setFixedWidth(100)
        self.number_extra.setMinimum(0)
        self.number_extra.setMaximum(60)
        #Añadir el campo
        self.layout.addWidget(self.number_extra, 1, 1)
        self.number_extra.valueChanged.connect(lambda value: self.sync_values(value))
        self.layout.addWidget(QLabel("Horas extra"), 1, 0)
        self.layout.itemAtPosition(1, 0).widget().setFixedWidth(100)

        # Configurar el campo ID de empleado
        self.employee_id_edit = QLineEdit()
        self.employee_id_edit.setFixedWidth(100)
        # Añadir el campo
        self.layout.addWidget(self.employee_id_edit, 1, 3 ) 
        self.layout.addWidget(QLabel("ID Empleado"), 1, 2)
        self.layout.itemAtPosition(1, 2).widget().setFixedWidth(100)

        #Añadir un campo vacio para dejar un espacio antes de iniciar los dias de la semana 
        self.layout.addWidget(QLabel(" "), 2, 0)
        self.layout.itemAtPosition(2, 0).widget().setFixedWidth(100)

        #Añadir las eqtiquetas de los dias de la semana 
        days_of_week = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        for i, day in enumerate(days_of_week, start=1):
            label = QLabel(day)
            label.setAlignment(Qt.AlignCenter)  # Centra horizontalmente el texto dentro del QLabel
            self.layout.addWidget(label, 2, i)
            self.layout.itemAtPosition(2, i).widget().setFixedWidth(100)

        #Añadir los campos para las horas corrientes de cada dia  
        for i in range(1, 3):
                for j in range(1, 8):
                    number_edit = QSpinBox()
                    number_edit.setFixedWidth(100)
                    number_edit.setMinimum(0)
                    number_edit.setMaximum(8)
                    self.layout.addWidget(number_edit, i + 2, j)
                    number_edit.valueChanged.connect(self.update_week_total)

        #Añadir la etiqyeta de semana 1
        self.layout.addWidget(QLabel("Semana 1"), 3, 0)
        self.layout.itemAtPosition(3, 0).widget().setFixedWidth(100)

        #Añadir la etiqyeta de semana 2
        self.layout.addWidget(QLabel("Semana 2"), 4, 0)
        self.layout.itemAtPosition(4, 0).widget().setFixedWidth(100)

        #Añadir un campo vacio para dejar un espacio antes los encabezados del resumen
        self.layout.addWidget(QLabel(" "), 5, 0)
        self.layout.itemAtPosition(5, 0).widget().setFixedWidth(100)

        #Añadir los encabezados del resumen
        label = QLabel("Cantidad")
        label.setAlignment(Qt.AlignCenter) 
        self.layout.addWidget(label, 5, 1)
        self.layout.itemAtPosition(5, 1).widget().setFixedWidth(100)

        label = QLabel("Monto")
        label.setAlignment(Qt.AlignCenter) 
        self.layout.addWidget(label, 5, 2)
        self.layout.itemAtPosition(5, 2).widget().setFixedWidth(100)

        #Añadir los laterales del resumen 
        self.layout.addWidget(QLabel("H. regulares"), 6, 0)
        self.layout.itemAtPosition(6, 0).widget().setFixedWidth(100)

        self.layout.addWidget(QLabel("H. extra"), 7, 0)
        self.layout.itemAtPosition(7, 0).widget().setFixedWidth(100)

        self.layout.addWidget(QLabel("Total"), 8, 0)
        self.layout.itemAtPosition(7, 0).widget().setFixedWidth(100)


        #Configurar el campo de cantidad de horas corrientes 
        self.h_regulares = QSpinBox()
        self.h_regulares.setFixedWidth(100)
        self.h_regulares.setMinimum(0)
        self.h_regulares.setStyleSheet("QSpinBox { color: black; }")
        self.h_regulares.setEnabled(False) 
        #Añadir el campo
        self.layout.addWidget(self.h_regulares, 6, 1)

        #Configurar el campo de monto de horas corrientes        
        self.h_regulares_monto = QSpinBox()
        self.h_regulares_monto.setFixedWidth(100)
        self.h_regulares_monto.setMinimum(0)
        self.h_regulares_monto.setMaximum(10000)
        self.h_regulares_monto.setStyleSheet("QSpinBox { color: black; }")
        self.h_regulares_monto.setEnabled(False) 
        #Añadir el campo
        self.layout.addWidget(self.h_regulares_monto, 6, 2)

        #Configurar el campo de cantidad de horas extra 
        self.h_extra = QSpinBox()
        self.h_extra.setFixedWidth(100)
        self.h_extra.setMinimum(0)
        self.h_extra.setStyleSheet("QSpinBox { color: black; }")
        self.h_extra.setEnabled(False) 
        #Añadir el campo
        self.layout.addWidget(self.h_extra, 7, 1)

        #Configurar el campo de monto de horas extra 
        self.h_extra_monto = QSpinBox()
        self.h_extra_monto.setFixedWidth(100)
        self.h_extra_monto.setMinimum(0)
        self.h_extra_monto.setMaximum(10000)
        self.h_extra_monto.setStyleSheet("QSpinBox { color: black; }")
        self.h_extra_monto.setEnabled(False)
        #Añadir el campo
        self.layout.addWidget(self.h_extra_monto, 7, 2)

        #Configurar el campo de monto total
        self.total = QSpinBox()
        self.total.setFixedWidth(100)
        self.total.setMinimum(0)
        self.total.setMaximum(10000)
        self.total.setStyleSheet("QSpinBox { color: black; }")
        self.total.setEnabled(False)
        #Añadir el campo
        self.layout.addWidget(self.total, 8, 2)

        #Añadir el Limpiar
        button = QPushButton("Limpiar")
        self.layout.addWidget(button, 6, 4)
        button.clicked.connect(self.clear_fields) 

        #Añadir el Enviar
        button = QPushButton("Enviar")
        button.clicked.connect(self.send_data) 
        self.layout.addWidget(button, 6, 5)

        #Añadir el Cerrar
        button = QPushButton("Cerrar")
        button.clicked.connect(self.close)
        self.layout.addWidget(button, 6, 6)

    #Actualizar dia fina como +13 del dia de inicio
    def update_end_date(self, date):
        self.end_date_edit.setDate(date.addDays(13))

    #Actualizar el monto de las horas extra
    def sync_values(self, value):
        spinbox = self.layout.itemAtPosition(7, 1).widget()
        spinbox.setValue(value)
        h_extra = value
        h_extra_monto = h_extra * 90  
        self.h_extra_monto.setValue(h_extra_monto)
        self.update_total()

    #Actualizar el total de las horas corrientes y el monto
    def update_week_total(self):
        week_total = sum([
            self.layout.itemAtPosition(row, column).widget().value()
            for row in range(3, 5)
            for column in range(1, 8)
        ])
        self.h_regulares.setValue(week_total)
        self.h_regulares_monto.setValue(week_total * 60)
        self.update_total()
        
    #Actualizar monto total
    def update_total(self):
        total = self.h_regulares_monto.value() + self.h_extra_monto.value()
        self.total.setValue(total)


    #Limpiar los campos
    def clear_fields(self):
        self.start_date_edit.setDate(QDate.currentDate())
        for row in range(1, 8):  
            for column in range(1, 8):  
                item = self.layout.itemAtPosition(row, column)
                if item is not None:
                    widget = item.widget()
                    if isinstance(widget, QSpinBox):
                        widget.setValue(0)

    #Mensaje de resumen
    def send_data(self):
        total_hours = self.h_regulares.value()
        employee = self.employee_id_edit.text()
        total = self.total.value()

        if not employee :
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Debe digitar el Id del empleado.")
            msgBox.setWindowTitle("Error")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        else:
            if total_hours > 96:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText("El total de horas corrientes sobrepasa las 48 horas por semana.")
                msgBox.setWindowTitle("Error")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()
            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText(f"Datos enviados correctamente.\n\nEmpleado ID: {employee}.\n\nMonto a percibir: ${total}")
                msgBox.setWindowTitle("Éxito")
                msgBox.setStandardButtons(QMessageBox.Ok)
                returnValue = msgBox.exec()
                if returnValue == QMessageBox.Ok:
                    self.clear_fields()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
