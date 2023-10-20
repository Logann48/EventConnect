from flask import Flask, render_template,request,redirect,url_for,flash,session
from werkzeug.utils import secure_filename
from config import config
from flask_mysqldb import MySQL
from models.ModelUser import ModelUser
from models.entities.User import User, AddUser, Foto,Evento,Compra, Pago, Entrada,PrecioEntrada
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from flask_login import LoginManager,login_user, logout_user,login_required,current_user
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
from flask import send_file


app = Flask(__name__)
app.secret_key = 'F1341716E82A4E9C16448426E86C48F056246405B771F17946ADD3342B435808'
app.config['UPLOAD_FOLDER'] = 'pics'
app.config['UPLOAD_FOLDER_CAPS'] = 'caps'

csrf=CSRFProtect()

db=MySQL(app)

login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_cedula(db, id)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        user=User(request.form['cedula'],request.form['password'],0,0)
        logged_user=ModelUser.login(db, user)
        if logged_user!=None:
            if logged_user.password:
                if(logged_user.estado==1):
                    if(logged_user.tipo==1):
                        session['user_type'] = logged_user.tipo
                        session.permanent = True
                        login_user(logged_user)#pendiente aquí
                        return redirect(url_for('usuario'))
                    
                    if(logged_user.tipo==2):
                        session['user_type'] = logged_user.tipo
                        session.permanent = True
                        login_user(logged_user)#pendiente aquí
                        return redirect(url_for('organizador'))

                    if(logged_user.tipo==3):
                        session['user_type'] = logged_user.tipo
                        session.permanent = True
                        login_user(logged_user)#pendiente aquí
                        return redirect(url_for('administrativo'))
                                        
                else:
                    flash("Usuario inhabilitado...")
                    return render_template('login.html')
                
            else:
                flash("Usuario o Constraseña Incorrecto")
                return render_template('login.html')
        else:
            flash("Usuario inexistente...")
            return render_template('login.html')
            
    else:
        return render_template('login.html')
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/usuario')
@login_required
def usuario():
    if 'user_type' in session and session['user_type'] == 1:
        return render_template('usuario.html')
    else:
        return redirect(url_for('login'))

    
@app.route('/registrar', methods=['GET','POST'])
def registrar():
    if request.method=='POST':
        print(request.form['apellido'])
        userG=AddUser(request.form['cedula'],request.form['nombre'],request.form['apellido'],request.form['correo'],request.form['telefono'],request.form['direccion'],request.form['password'])
        tipo=1
        guardarU=ModelUser.guardarU(db,userG,tipo)
        if guardarU:
            flash("Registro exitoso...")
            return render_template('registrar.html') 

        else:
            flash("Registro fallido...")
            return render_template('registrar.html')

    else:
        return render_template('registrar.html')

###############

@app.route('/compraentradas', methods=['GET','POST'])
@login_required
def cargarTipoEntradas():
    if 'user_type' in session and session['user_type'] == 1 or 2 or 3:
        if request.method == 'POST':
            xd = request.form['id_Evento']
            session['id_Evento'] = xd
            cur= db.connection.cursor()
            cur2 = db.connection.cursor()
            cur.execute('SELECT tipo, precio FROM tipo_entrada')
            cur2.execute('SELECT id_Evento, nombre FROM eventos WHERE id_Evento LIKE "%'+xd+'%"')
            entryType = cur.fetchall()
            xdd = cur2.fetchone()
            db.connection.commit()

            return render_template('compraEntradas.html', entradas = entryType, xdd=xdd)
    else:
        return redirect(url_for('login'))
    
@app.route('/compra')
@login_required
def compra():
    if 'user_type' in session and session['user_type'] == 1 or 2 or 3:
        id_Evento = session['id_Evento']
        cur= db.connection.cursor()
        cur.execute("""SELECT COUNT(tipo) FROM tipo_entrada INNER JOIN entrada_evento ON tipo_entrada.id_TipoEntrada=entrada_evento.id_TipoEntrada WHERE entrada_evento.id_Evento = '{}'""".format(id_Evento))
        cantidad_tipos=cur.fetchone()[0]
        db.connection.commit()
        precios = []
        cantidades = []

        for i in range(cantidad_tipos):
            cantidadEn = request.args.get('cantidadEn{}'.format(i))
            precioEntradas = request.args.get('precio{}'.format(i))
            if cantidadEn == "":
                cantidadEn = 0

            print(type(cantidadEn))
            precios.append(float(precioEntradas))
            cantidades.append(int(cantidadEn))
        session['precios'] = precios
        session['cantidades'] = cantidades
        return redirect(url_for('registropago'))
    else:
        return redirect(url_for('login'))




################

@app.route('/cusuario', methods=['GET','POST'])
@login_required
def cusuario():
    if 'user_type' in session and session['user_type'] == 1:
        if request.method=='POST':
            current_datetime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            compra=Compra(session['cedula'],current_datetime,request.form['id_Evento'])
            return render_template('crudusuario.html')
    else:
        return redirect(url_for('login'))

@app.route('/boletos')
@login_required
def boletos():
    if 'user_type' in session and session['user_type'] == 1 or 2 or 3:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM eventos WHERE estado = 1')
        dataEvent = cur.fetchall()
        db.connection.commit()
        return render_template('boletos.html', eventos = dataEvent)
    else:
        return redirect(url_for('login'))

@app.route('/boletos', methods=['GET','POST'])
@login_required
def busquedaBoletos():
    if 'user_type' in session and session['user_type'] == 1 or 2 or 3:
        search_performed = False
        resultBusqueda = None
        if request.method == "POST":
            search_performed = True
            search = request.form['barraBusqueda']
            cur = db.connection.cursor()
            cur.execute("SELECT * FROM eventos WHERE nombre LIKE '%" + search + "%' AND estado = 1 ORDER BY id_Evento DESC")
            resultBusqueda = cur.fetchall()
            db.connection.commit()

        return render_template('boletosResult.html', resultado = resultBusqueda, search_performed=search_performed)
    else:
        return redirect(url_for('login'))



##############


@app.route('/registropago', methods=['GET','POST'])
def registropago():
    if 'user_type' in session and session['user_type'] == 1 or 2 or 3:
        check1 = False  # Define check1 here
        if request.method == "POST":
            if 'file' not in request.files:
                flash("Sin foto")
            else:
                Nombre_Apellido = request.form['nombre']
                cedula_Pagador = request.form['cedula']
                check1 = 'check1' in request.form
                referencia = request.form['nroTrans']
                myDate = request.form['myDate']
                telefono_Cuenta = request.form['telefono']
                monto = request.form['monto']
                file = request.files.getlist('file')
                if check1 == True:
                    metodo = "Pago Movil"
                else:
                    metodo = "Transferencia"

                cantidades=session['cantidades']
                precios=session['precios']
                cedula=current_user.cedula
                fecha_actual = datetime.now()
                id_Evento = session['id_Evento']
                entrada=Entrada(cantidades,precios)
                pago = Pago(cedula ,fecha_actual, Nombre_Apellido, cedula_Pagador, myDate, metodo, referencia, telefono_Cuenta, monto, file,id_Evento)
                guardarC = ModelUser.guardarC(db, pago, app, entrada)
                if guardarC != pago:
                    flash("guardarC")
                    return render_template('registroPago.html')
                else:
                    return redirect(url_for('registroexitoso'))
        else:
            return render_template('registroPago.html')
    else:
        return redirect(url_for('login'))

############################################################################

@app.route('/organizador')
@login_required
def organizador():
    if 'user_type' in session and session['user_type'] == 2 or 3:
        return render_template('organizador.html')
    else:
        return redirect(url_for('login'))
    

@app.route('/crudorganizador')
@login_required
def crudorganizador():
    if 'user_type' in session and session['user_type'] == 2 or 3:
        return render_template('crudorganizador.html')
    else:
        return redirect(url_for('login'))

@app.route('/registroevento', methods=['GET','POST'])
@login_required
def registroevento():
    if 'user_type' in session and session['user_type'] == 2 or 3:
        if request.method=='POST':
            tipo = []
            precio = []
            estado=1
            date_str = request.form['myDate']  # 'YYYY-MM-DD'
            time_str = request.form['horaEv']  # 'HH:MM'
            datetime_str = date_str + ' ' + time_str
            datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
            for i in range(1,4):
                tipo = request.form['tipo{}'.format(i)]
                precio = request.form['precio{}'.format(i)]

            Entradas=PrecioEntrada(tipo,precio)
            Nevento=Evento(request.form['nombreEv'], datetime_obj, request.form['descripEv'], estado)
            guardarU=ModelUser.guardarE(db,Nevento,current_user.cedula,Entradas)
            if guardarU:
                session['id_evento'] = guardarU
                flash("Registro Exitoso")
                return redirect(url_for('imagenesevento'))
            else:
                flash("Registro fallido...")
                return render_template('registroEvento.html')
        else:
            return render_template('registroEvento.html')
    else:
        return redirect(url_for('login'))


@app.route('/principal')
@login_required
def principal():
    if 'user_type' in session and session['user_type'] == 1:
        return redirect(url_for('usuario'))
    elif 'user_type' in session and session['user_type'] == 2:
        return redirect(url_for('organizador'))
    elif 'user_type' in session and session['user_type'] == 3:
        return redirect(url_for('administrativo'))


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'user_type' in session and session['user_type'] == 2 or 3:
        id_evento = session.get('id_evento')
        if 'file' not in request.files:
            flash("Sin foto")
            return redirect(url_for('imagenesevento'))
        else:
            files = request.files.getlist('file')
            guardarI=ModelUser.guardarI(db,files,app,id_evento)
            if guardarI!=None:
                return redirect(url_for('registroexitoso'))
            else:
                flash("Registro fallido...")
                return redirect(url_for('imagenesevento'))
    else:
        return redirect(url_for('login'))    

@app.route('/imagenesevento')
def imagenesevento():
    if 'user_type' in session and session['user_type'] == 2 or 3:
        return render_template('imagenesEvento.html')
    else:
        return redirect(url_for('login'))
##########################################################################
@app.route('/actualizardatos')
@login_required
def actualizarDatos():
    if 'user_type' in session and session['user_type'] == 1 or 2 or 3:
        cedula = current_user.cedula
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM usuario WHERE cedula = %s", (cedula,))
        dataUser = cur.fetchone()
        db.connection.commit()
        return render_template('actualizarDatos.html', cedula=cedula, datos=dataUser)
    else:
        return redirect(url_for('login'))

@app.route('/',  methods=['GET','POST'])
@login_required
def actualDatos():
    if 'user_type' in session and session['user_type'] == 1 or 2 or 3:
        if request.method=='POST':

            cedula = request.form['cedula']
            correo = request.form['correo']
            telefono = request.form['telefono']
            direccion = request.form['direccion']
            
            cur = db.connection.cursor()
            
            update_query = """UPDATE usuario SET correo = %s, telefono = %s, direccion = %sWHERE cedula = %s"""
            cur.execute(update_query, (correo, telefono, direccion, cedula))
            db.connection.commit()

        return render_template('actualizarExito.html')
    else:
        return redirect(url_for('login'))
######################################################################################
@app.route('/adminPagos')
@login_required
def adminPagos():
    if 'user_type' in session and session['user_type'] == 3:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM detalle_pago WHERE estado = 0')
        pagoDetail = cur.fetchall()
        db.connection.commit()
        return render_template('adminPagos.html', pagos=pagoDetail)
    else:
        return redirect(url_for('login'))

@app.route('/adminPagos', methods=['GET','POST'])
@login_required
def tablaPago1():
    if 'user_type' in session and session['user_type'] == 3:
        if request.method == "POST":
            fecha = request.form['fecha']
            nombre = request.form['nombre']
            cedula = request.form['cedula']
            metodo = request.form['metodo']
            fechaPago = request.form['fechaPago']
            referencia = request.form['referencia']
            telefonoCuenta = request.form['telefonoCuenta']
            monto = request.form['monto']
            captura = request.form['captura']
            estado = request.form['estado']

            cur = db.connection.cursor()
            cur.execute("UPDATE detalle_pago SET estado = 1 WHERE fecha_Compra = %s AND Nombre_Apellido = %s AND cedula_Pagador = %s AND Metodo_Pago = %s AND fecha_Pago = %s AND Referencia_Pago = %s AND telefono_Cuenta = %s AND monto = %s AND id_Capture = %s",
            (fecha,nombre,cedula,metodo,fechaPago,referencia,telefonoCuenta,monto,captura))
            db.connection.commit()

        return render_template('ConPagoAdmin.html')
    else:
        return redirect(url_for('login'))
#####################################################################################
@app.route('/gestionevento')
@login_required
def gestionevento():
    if 'user_type' in session and session['user_type'] == 2:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM eventos WHERE estado = 1')
        dataEvent = cur.fetchall()
        db.connection.commit()
        return render_template('gestionevento.html', eventos=dataEvent)
    else:
        return redirect(url_for('login'))

@app.route('/gestionevento', methods=['GET','POST'])
@login_required
def tablaEvento1():
    if 'user_type' in session and session['user_type'] == 2:
        if request.method == "POST":
            nombre = request.form['nombre']
            fecha_hora = request.form['fecha_hora']
            descripcion = request.form['descripcion']
            estado = request.form['estado']

            cur = db.connection.cursor()
            cur.execute("UPDATE eventos SET estado = 0 WHERE nombre = %s AND fecha = %s AND descripcion = %s AND estado = %s",
            (nombre, fecha_hora, descripcion, estado))
            db.connection.commit()

        return render_template('InhaEvExito.html')
    else:
        return redirect(url_for('login'))

####################################################################################   

@app.route('/administrativo')
@login_required
def administrativo():
    if 'user_type' in session and session['user_type'] == 3:
        return render_template('administrativo.html')
    else:
        return redirect(url_for('login'))
    
#####################################################################################

@app.route('/admineventos')
@login_required
def admineventos():
    if 'user_type' in session and session['user_type'] == 3:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM eventos WHERE estado = 1')
        dataEvent = cur.fetchall()
        db.connection.commit()
        return render_template('admineventos.html', eventos=dataEvent)
    else:
        return redirect(url_for('login'))

@app.route('/admineventos', methods=['GET','POST'])
@login_required
def tablaEvento2():
    if 'user_type' in session and session['user_type'] == 3:
        if request.method == "POST":
            nombre = request.form['nombre']
            fecha_hora = request.form['fecha_hora']
            descripcion = request.form['descripcion']
            estado = request.form['estado']

            cur = db.connection.cursor()
            cur.execute("UPDATE eventos SET estado = 0 WHERE nombre = %s AND fecha = %s AND descripcion = %s AND estado = %s",
            (nombre, fecha_hora, descripcion, estado))
            db.connection.commit()

        return render_template('InhaEvAdminExito.html')
    else:
        return redirect(url_for('login'))

############################################################################

@app.route('/adminorganizadores')
@login_required
def adminorganizadores():
    if 'user_type' in session and session['user_type'] == 3:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM usuario INNER JOIN login ON usuario.cedula = login.cedula WHERE login.tipo = "2" AND login.estado = 1')
        dataUsers = cur.fetchall()
        return render_template('adminorganizadores.html', usuarios = dataUsers)
    else:
        return redirect(url_for('login'))

@app.route('/adminorganizadores', methods=['GET','POST'])
@login_required
def tablaOrg():
    if 'user_type' in session and session['user_type'] == 3:
        if request.method == "POST":
            cedula = request.form['cedula']

            cur = db.connection.cursor()
            cur.execute("UPDATE login SET estado = 0 WHERE cedula = %s",
            (cedula,))
            db.connection.commit()

        return render_template('InhaOrgExito.html')
    else:
        return redirect(url_for('login'))

###########################################################################
    
@app.route('/adminclientes')
@login_required
def adminclientes():
    if 'user_type' in session and session['user_type'] == 3:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM usuario INNER JOIN login ON usuario.cedula = login.cedula WHERE login.tipo = "1"')
        dataUsers = cur.fetchall()
        db.connection.commit()
        return render_template('adminclientes.html', usuarios = dataUsers)
    else:
        return redirect(url_for('login'))

#################################################################################################
@app.route('/adminadmins')
@login_required
def adminadmins():
    if 'user_type' in session and session['user_type'] == 3:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM usuario INNER JOIN login ON usuario.cedula = login.cedula WHERE login.tipo = "3" AND login.estado = "1"')
        dataUsers = cur.fetchall()
        db.connection.commit()
        return render_template('adminadmins.html', usuarios = dataUsers)
    else:
        return redirect(url_for('login'))
    
@app.route('/adminadmins', methods=['GET','POST'])
@login_required
def tablaAdmin():
    if 'user_type' in session and session['user_type'] == 3:
        if request.method == "POST":
            cedula = request.form['cedula']

            cur = db.connection.cursor()
            cur.execute("UPDATE login SET estado = 0 WHERE cedula = %s",
            (cedula,))
            db.connection.commit()

        return render_template('InhaAdminExito.html')
    else:
        return redirect(url_for('login'))
###############################################################################################
    
@app.route('/registrarorganizador', methods=['GET','POST'])
def registrarorganizador():
    if 'user_type' in session and session['user_type'] == 3:
        if request.method=='POST':
            userG=AddUser(request.form['cedula'],request.form['nombre'],request.form['apellido'],request.form['correo'],request.form['telefono'],request.form['direccion'],request.form['password'])
            tipo=2
            guardarU=ModelUser.guardarU(db,userG,tipo)
            if guardarU:
                flash("Registro exitoso...")
                return render_template('registrarOrg.html')
            else:
                flash("Registro fallido, vuelva a intentarlo...")
                return render_template('registrarOrg.html')
        else:
            return render_template('registrarOrg.html')
    else:
        return redirect(url_for('login'))


@app.route('/registraradministrador', methods=['GET','POST'])
def registraradministrador():
    if 'user_type' in session and session['user_type'] == 3:
        if request.method=='POST':
            userG=AddUser(request.form['cedula'],request.form['nombre'],request.form['apellido'],request.form['correo'],request.form['telefono'],request.form['direccion'],request.form['password'])
            tipo=3
            guardarU=ModelUser.guardarU(db,userG,tipo)
            if guardarU:
                flash("Registro exitoso...")
                return render_template('login.html')
            else:
                flash("Registro fallido...")
                return render_template('registraradmin.html')
        else:
            return render_template('registraradmin.html')
    else:
        return redirect(url_for('login'))

@app.route('/adminreportes')
@login_required
def adminreportes():
    if 'user_type' in session and session['user_type'] == 3:
        return render_template('adminreportes.html')
    else:
        return redirect(url_for('login'))
    
############## REPORTES ###################
@app.route('/reporte1', methods=['GET','POST'])
@login_required
def reporte1():
    if 'user_type' in session and session['user_type'] == 3:
        num_users = ModelUser.get_report1(db)
        width, height = letter
        line_height = 11
        gap_between_rows = 10
        pdfmetrics.registerFont(TTFont('Times-Bold', 'Times Bold.ttf'))
        
        c = canvas.Canvas("reporte_usuarios_activos.pdf", pagesize=letter)
        c.setFont('Times-Bold', 12)
        c.drawCentredString(width / 2, height - 8 * line_height, "Reporte de Usuarios Activos")
        c.setFont('Times-Roman', 12)
        c.drawString(width - 150, height - 2.5 * line_height, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        c.drawString(width - 150, height - 5.5 * line_height, f"Administrador: {current_user.cedula}")
        c.drawString(200, height - 12 * line_height, f"Número de usuarios activos registrados: {num_users}")
        
        c.drawString(width - 150, height - 4 * line_height, "Página 1 de 1")
        
        c.showPage()
        c.save()
        
        try:
            return send_file("reporte_usuarios_activos.pdf", as_attachment=True)
        except Exception as e:
            return str(e)
    else:
        return redirect(url_for('login'))


@app.route('/reporte2', methods=['GET','POST'])
@login_required
def reporte2():
    if 'user_type' in session and session['user_type'] == 3:
        num_users = ModelUser.get_reporte2(db)
        print(num_users)
        width, height = letter
        line_height = 11
        gap_between_rows = 10
        pdfmetrics.registerFont(TTFont('Times-Bold', 'Times Bold.ttf'))
        
        c = canvas.Canvas("reporte_Organizadores_activos.pdf", pagesize=letter)
        c.setFont('Times-Bold', 12)
        c.drawCentredString(width / 2, height - 8 * line_height, "Reporte de Organizadores Activos")
        c.setFont('Times-Roman', 12)
        c.drawString(width - 150, height - 2.5 * line_height, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        c.drawString(width - 150, height - 5.5 * line_height, f"Administrador: {current_user.cedula}")
        c.drawString(200, height - 12 * line_height, f"Número de Organizadores activos registrados: {num_users}")
        c.drawString(width - 150, height - 4 * line_height, "Página 1 de 1")
        c.showPage()
        c.save()
        try:
            return send_file("reporte_Organizadores_activos.pdf", as_attachment=True)
        except Exception as e:
            return str(e)
    else:
        return redirect(url_for('login'))

@app.route('/reporte3', methods=['GET','POST'])
@login_required
def reporte3():
    if 'user_type' in session and session['user_type'] == 3:
        print(request.form['start-date'])
        print(request.form['end-date'])
        inicio=request.form['start-date']
        fin=request.form['end-date']
        data = ModelUser.get_reporte3(db, inicio, fin)
        if data!=None and "0":
            width, height = letter
            line_height = 11
            gap_between_rows = 10
            pdfmetrics.registerFont(TTFont('Times-Bold', 'Times Bold.ttf'))
            # First pass to count the number of pages
            c = canvas.Canvas(None)
            start_height = height - 10*line_height
            for i, row in enumerate(data, start=1):
                if i == 1 or row['nombre'] != data[i-2]['nombre']:
                    start_height -= 5*line_height + gap_between_rows
                else:
                    start_height -= 2*line_height + gap_between_rows
                if start_height < 0:
                    c.showPage()
                    start_height = height - 10*line_height
            total_pages = c.getPageNumber()
            # Second pass to draw the content and include the total page count
            c = canvas.Canvas("reporte_venta_entradas_por_evento.pdf", pagesize=letter)
            c.setFont('Times-Bold', 12)
            c.drawCentredString(width / 2, height - 8* line_height, "Reporte de Venta de Entradas por Evento")
            c.setFont('Times-Roman', 12)
            c.drawString(width - 150, height - 2.5 * line_height, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            c.drawString(width - 150, height - 5.5 * line_height, f"Administrador: {current_user.cedula}")
            start_height = height - 10*line_height
            for i, row in enumerate(data, start=1):
                if i == 1 or row['nombre'] != data[i-2]['nombre']:
                    start_height -= 5*line_height + gap_between_rows
                    c.setFont('Times-Bold', 12)
                    c.drawString(30, start_height, f"Nombre del evento: {row['nombre']}")
                    c.setFont('Times-Roman', 12)
                    c.drawString(30, start_height - 1.3*line_height, f"ID del organizador: {row['cedula']}")
                    c.drawString(30, start_height - 2.3*line_height, f"Fecha del evento: {row['fecha']}")
                if start_height < 0:
                    c.showPage()
                    start_height = height - 10*line_height
            c.drawString(width - 150, height - 4 * line_height, f"Página {c.getPageNumber()} de {total_pages}")
            c.showPage()
            c.save()
            try:
                return send_file("reporte_venta_entradas_por_evento.pdf", as_attachment=True)
            except Exception as e:
                return print(str(e))
        else:
            print("si")
            return redirect(url_for('adminreportes'))
    else:
        return redirect(url_for('login'))


@app.route('/reporte4', methods=['GET','POST'])
@login_required
def reporte4():
    if 'user_type' in session and session['user_type'] == 3:
        data = ModelUser.get_report4(db)
        width, height = letter
        line_height = 11
        gap_between_rows = 10
        pdfmetrics.registerFont(TTFont('Times-Bold', 'Times Bold.ttf'))
        # First pass to count the number of pages
        c = canvas.Canvas(None)
        start_height = height - 10*line_height
        for i, row in enumerate(data, start=1):
            if i == 1 or row['nombre'] != data[i-2]['nombre']:
                start_height -= 5*line_height + gap_between_rows
            else:
                start_height -= 2*line_height + gap_between_rows
            if start_height < 0:
                c.showPage()
                start_height = height - 10*line_height
        total_pages = c.getPageNumber()
        # Second pass to draw the content and include the total page count
        c = canvas.Canvas("reporte_venta_entradas_por_evento.pdf", pagesize=letter)
        c.setFont('Times-Bold', 12)
        c.drawCentredString(width / 2, height - 8* line_height, "Reporte de Venta de Entradas por Evento")
        c.setFont('Times-Roman', 12)
        c.drawString(width - 150, height - 2.5 * line_height, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        c.drawString(width - 150, height - 5.5 * line_height, f"Administrador: {current_user.cedula}")
        start_height = height - 10*line_height
        for i, row in enumerate(data, start=1):
            if i == 1 or row['nombre'] != data[i-2]['nombre']:
                start_height -= 5*line_height + gap_between_rows
                c.drawString(30, start_height, f"Nombre del evento: {row['nombre']}")
                c.drawString(30, start_height - 1.3*line_height, f"ID del organizador: {row['cedula']}")
                c.drawString(30, start_height - 2.3*line_height, f"Estado del evento: {row['estado']}")
            else:
                start_height -= 2*line_height + gap_between_rows
            c.drawString(30, start_height - 3.3*line_height, f"Tipo de entrada: {row['tipo']}")
            c.drawString(30, start_height - 4.3*line_height, f"Cantidad vendida: {row['cantidad_vendida']}")
            if start_height < 0:
                c.showPage()
                start_height = height - 10*line_height
        c.drawString(width - 150, height - 4 * line_height, f"Página {c.getPageNumber()} de {total_pages}")
        c.showPage()
        c.save()
        try:
            return send_file("reporte_venta_entradas_por_evento.pdf", as_attachment=True)
        except Exception as e:
            return str(e)
    else:
        return redirect(url_for('login'))

############## REPORTES ###################
@app.route('/registro_exitoso')
def registroexitoso():
    return render_template('exito.html')

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1> Página no encontrada</h1>",404

if __name__ == '__main__':
    app.config.from_object (config['development'])
    csrf.init_app(app)
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)
    app.run(debug=True)

