from werkzeug.security  import check_password_hash, generate_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self,cedula,password, estado, tipo) -> None:
        self.cedula=cedula
        self.password=password
        self.estado=estado
        self.tipo=tipo

    def get_id(self):
        return self.cedula

    @classmethod
    def check_password(self,hashed_password, password):
        return check_password_hash(hashed_password,password)
        
class AddUser():
    def __init__(self,cedula,nombre, apellido, correo, telefono, direccion,password) -> None:
        self.cedula=cedula
        self.nombre=nombre
        self.apellido=apellido
        self.correo=correo
        self.telefono=telefono
        self.direccion=direccion
        self.password=password

    @classmethod
    def create_password(self, password):
        return generate_password_hash(password)

    
class Evento():
    def __init__(self, nombre, Fecha, descripcion, estado) -> None:
        self.nombre=nombre
        self.estado=estado
        self.Fecha=Fecha
        self.descripcion=descripcion
        self.estado=estado

class Foto():
    def __init__(self,foto,app,id_evento) -> None:
        self.foto=foto
        self.app=app
        self.id_evento=id_evento

class Compra():
    def __init__(self,cedula,fecha,id_Evento) -> None:
        self.cedula=cedula
        self.fecha=fecha
        self.id_Evento=id_Evento

class Pago():
    def __init__(self,cedula_Cliente, fecha_Compra, Nombre_Apellido, cedula_Pagador, myDate, metodo, referencia, telefono_Cuenta, monto, file,id_Evento) -> None:
        self.Nombre_Apellido=Nombre_Apellido
        self.metodo=metodo
        self.fecha_Compra=fecha_Compra
        self.cedula_Cliente=cedula_Cliente
        self.myDate=myDate
        self.cedula_Pagador=cedula_Pagador
        self.telefono_Cuenta=telefono_Cuenta
        self.referencia=referencia
        self.monto=monto
        self.file=file
        self.id_Evento=id_Evento

class Entrada():
    def __init__(self,cantidades,precios) -> None:
        self.cantidades=cantidades
        self.precios=precios