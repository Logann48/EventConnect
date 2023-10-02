from .entities.User import User
from .entities.User import AddUser
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from PIL import Image

class ModelUser():
    @classmethod
    def login(self,db,user):
        try:
            cursor=db.connection.cursor()
            sql="""SELECT cedula, password ,estado ,tipo FROM login 
                    WHERE cedula = '{}'""".format(user.cedula)
            cursor.execute(sql)
            row=cursor.fetchone()
            
            if row != None:
                user=User(row[0], User.check_password(row[1],user.password), row[2], row[3])
                return user
            else:
                return None

        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_by_cedula(cls, db, id):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT cedula, password ,estado ,tipo FROM login 
                    WHERE cedula = '{}'""".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            
            if row is not None:
                return User(row[0], row[1], row[2], row[3])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)



    @classmethod   
    def guardarU(self,db,userG,tipo):
        try:
            print(AddUser.create_password(userG.password))
            estado=1
            cursor=db.connection.cursor()
            sql = """INSERT INTO `usuario` (`cedula`, `nombre`, `apellido`, `correo`, `telefono`, `direccion`) VALUES (%s, %s, %s, %s, %s, %s)"""
            data = (userG.cedula, userG.nombre, userG.apellido, userG.correo, userG.telefono, userG.direccion)
            cursor.execute(sql, data)

            sql="""INSERT INTO `login`(`cedula`, `password`, `estado`, `tipo`) VALUES (%s, %s, %s, %s)"""
            data = (userG.cedula, AddUser.create_password(userG.password), estado, tipo)
            cursor.execute(sql,data)

            sql = "SELECT * FROM usuario INNER JOIN login ON usuario.cedula = login.cedula WHERE login.cedula AND usuario.cedula = '{}'".format(userG.cedula)
            cursor.execute(sql)
            db.connection.commit()
            row=cursor.fetchone()
            
            if row != None:
                return userG  
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod   
    def guardarE(self,db,Nevento,cedula_organizador,Entradas):
        try:
            cursor=db.connection.cursor()
            cursor1=db.connection.cursor()
            cursor2=db.connection.cursor()
            sql = ("INSERT INTO `eventos` (`cedula`,`nombre`, `fecha_Evento`, `descripcion`, `estado`)"
            "VALUES (%s, %s, %s, %s, %s)")
            data = (cedula_organizador, Nevento.nombre, Nevento.Fecha, Nevento.descripcion,Nevento.estado)
            cursor.execute(sql, data)

            print(Entradas.nombre,Entradas.precio)
            sql1 = ("INSERT INTO `tipo_entrada` (`tipo`,`Precio`)"
            "VALUES (%s,%s)")
            data1 = (Entradas.nombre,Entradas.precio)
            cursor1.execute(sql1, data1)
            cursor1.execute("SELECT LAST_INSERT_ID() AS id_TipoEntrada")
            result = cursor1.fetchone()[0]
            print(result)
            sql2 = ("INSERT INTO `entrada_evento` (`id_Evento`,`Precio`)"
            "VALUES (%s,%s)")
            data2 = (Entradas.nombre,Entradas.precio)
            cursor2.execute(sql2, data2)
            db.connection.commit()
            
            if result != None:
                return result
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod   
    def guardarI(self,db,files,app,id_evento):
        filenames = []
        for file in files:
            filename = secure_filename(file.filename)
            try:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                try:
                    Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                except IOError:
                    return 'File is not an image: ' + filename

                filenames.append(filename)
            except Exception as e:
                return 'Error saving file: ' + str(e)

        try:
            cursor = db.connection.cursor()
            for filename in filenames:
                query = "INSERT INTO fotos (`id_Evento`,`foto`) VALUES (%s,%s)"
                cursor.execute(query, (id_evento, os.path.join(app.config['UPLOAD_FOLDER'], filename)))

            db.connection.commit()
            cursor.close()
            
        except Exception as e:
            db.connection.rollback()
            print('Error inserting into database: ' + str(e))
            return None
        return 'File uploaded successfully'
    
    @classmethod   
    def guardarC(self, db, pago, app, entrada):
        filenames = []
        try:
            file = pago.file[0]
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER_CAPS'], filename))
            try:
                Image.open(os.path.join(app.config['UPLOAD_FOLDER_CAPS'], filename))
            except IOError:
                return None
            filenames.append(filename)
        except Exception as e:
            return 'Error saving file: ' + str(e)
        try:
            cursor = db.connection.cursor()
            cursor2 = db.connection.cursor()
            cursor3 = db.connection.cursor()
            cursor4 = db.connection.cursor()
            cursor5 = db.connection.cursor()
            cursor6 = db.connection.cursor()
            cursor7 = db.connection.cursor()
            query = "INSERT INTO detalle_pago (`cedula`,`fecha_Compra`,`Nombre_Apellido`,`cedula_Pagador`,`Metodo_Pago`,`fecha_Pago`,`Referencia_Pago`,`telefono_Cuenta`,`monto`,`id_Capture`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            myDate = datetime.strptime(pago.myDate, "%Y-%m-%d").date()
            cursor.execute(query, (pago.cedula_Cliente, pago.fecha_Compra, pago.Nombre_Apellido, pago.cedula_Pagador, pago.metodo, myDate, pago.referencia, pago.telefono_Cuenta, pago.monto, app.config['UPLOAD_FOLDER_CAPS'] + '/' + filenames[0]))

            consulta = "SELECT id_DetallePago FROM detalle_pago WHERE cedula='{}' ORDER BY fecha_Compra DESC LIMIT 1".format(pago.cedula_Cliente)
            cursor2.execute(consulta) 
            id_DetallePago = cursor2.fetchone()

            query2 = "INSERT INTO compra (`cedula`,`id_Evento`,`id_DetallePago`) VALUES (%s,%s,%s)"
            cursor3.execute(query2, (pago.cedula_Cliente, pago.id_Evento, id_DetallePago))

            consulta = "SELECT id_Compra FROM compra WHERE cedula='{}' ORDER BY id_Compra DESC LIMIT 1".format(pago.cedula_Cliente)
            cursor4.execute(consulta) 
            id_Compra = cursor4.fetchone()

            consulta2 = "SELECT entrada_evento.id_TipoEntrada FROM tipo_entrada INNER JOIN entrada_evento on tipo_entrada.id_TipoEntrada=entrada_evento.id_TipoEntrada WHERE entrada_evento.id_Evento='{}'".format(pago.id_Evento)
            cursor6.execute(consulta2)
            TipoEntrada = cursor6.fetchall()
            print(len(entrada.cantidades))

            for i in range(len(entrada.cantidades)):
                id_TipoEntrada=TipoEntrada[i][0] 
                cantidad=entrada.cantidades[i]
                precio=entrada.precios[i]
                if cantidad>0:
                    query4 = "INSERT INTO detalle_compra (`id_Compra`,`precio`,`id_TipoEntrada`,`cantidad`) VALUES (%s,%s,%s,%s)"
                    cursor7.execute(query4, (id_Compra, precio, id_TipoEntrada, cantidad))
            cursor.close()
            cursor2.close()
            cursor3.close()
            cursor4.close()
            cursor5.close()
            cursor6.close()
            cursor7.close()
            db.connection.commit()
            
        except Exception as e:
            db.connection.rollback()
            print('Error inserting into database: ' + str(e))
            return None
        return pago
