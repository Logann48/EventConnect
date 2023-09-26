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
    if 'user_type' in session and session['user_type'] == 1|3:
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
    if 'user_type' in session and session['user_type'] == 1|3:
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
    if 'user_type' in session and session['user_type'] == 1|3:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM eventos')
        dataEvent = cur.fetchall()
        db.connection.commit()
        return render_template('boletos.html', eventos = dataEvent)
    else:
        return redirect(url_for('login'))

@app.route('/boletos', methods=['GET','POST'])
@login_required
def busquedaBoletos():
    if 'user_type' in session and session['user_type'] == 1|3:
        search_performed = False
        resultBusqueda = None
        if request.method == "POST":
            search_performed = True
            search = request.form['barraBusqueda']
            cur = db.connection.cursor()
            cur.execute("SELECT * FROM eventos WHERE nombre LIKE '%" + search + "%' ORDER BY id_Evento DESC")
            resultBusqueda = cur.fetchall()
            db.connection.commit()
        return render_template('boletosResult.html', resultado = resultBusqueda, search_performed=search_performed)
    else:
        return redirect(url_for('login'))



##############


@app.route('/registropago', methods=['GET','POST'])
def registropago():
    if 'user_type' in session and session['user_type'] == 1|3:
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

##############

@app.route('/organizador')
@login_required
def organizador():
    if 'user_type' in session and session['user_type'] == 2:
        return render_template('organizador.html')
    else:
        return redirect(url_for('login'))
    

@app.route('/crudorganizador')
@login_required
def crudorganizador():
    if 'user_type' in session and session['user_type'] == 2:
        return render_template('crudorganizador.html')
    else:
        return redirect(url_for('login'))

@app.route('/registroevento', methods=['GET','POST'])
@login_required
def registroevento():
    if 'user_type' in session and session['user_type'] == 2|3:
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


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'user_type' in session and session['user_type'] == 2|3:
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
    if 'user_type' in session and session['user_type'] == 2|3:
        return render_template('imagenesEvento.html')
    else:
        return redirect(url_for('login'))
##########################################################################
@app.route('/actualizardatos')
@login_required
def actualizarDatos():
    if 'user_type' in session and session['user_type'] == 1|2|3:
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
    if 'user_type' in session and session['user_type'] == 1|2|3:
        if request.method=='POST':

            cedula = request.form['cedula']
            correo = request.form['correo']
            telefono = request.form['telefono']
            direccion = request.form['direccion']
            
            cur = db.connection.cursor()
            
            update_query = """
            UPDATE usuario 
            SET correo = %s, telefono = %s, direccion = %s
            WHERE cedula = %s
            """
            cur.execute(update_query, (correo, telefono, direccion, cedula))
            db.connection.commit()
            flash('Datos cambiados con éxito', 'success')
        return render_template('actualizarExito.html')
    else:
        return redirect(url_for('login'))
######################################################################################
@app.route('/adminPagos')
@login_required
def adminPagos():
    if 'user_type' in session and session['user_type'] == 3:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM detalle_pago')
        pagoDetail = cur.fetchall()
        db.connection.commit()
        return render_template('adminPagos.html', pagos=pagoDetail)
    else:
        return redirect(url_for('login'))
#####################################################################################


@app.route('/gestionevento')
@login_required
def crearevento():
    return render_template('gestionevento.html')
    

@app.route('/administrativo')
@login_required
def administrativo():
    if 'user_type' in session and session['user_type'] == 3:
        return render_template('administrativo.html')
    else:
        return redirect(url_for('login'))
    

@app.route('/admineventos')
@login_required
def admineventos():
    if 'user_type' in session and session['user_type'] == 3:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM eventos')
        dataEvent = cur.fetchall()
        db.connection.commit()
        return render_template('admineventos.html', eventos=dataEvent)
    else:
        return redirect(url_for('login'))
    

@app.route('/adminorganizadores')
@login_required
def adminorganizadores():
    if 'user_type' in session and session['user_type'] == 3:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM usuario INNER JOIN login ON usuario.cedula = login.cedula WHERE login.tipo = "2"')
        dataUsers = cur.fetchall()
        db.connection.commit()
        return render_template('adminorganizadores.html', usuarios = dataUsers)
    else:
        return redirect(url_for('login'))
    

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


@app.route('/adminadmins')
@login_required
def adminadmins():
    if 'user_type' in session and session['user_type'] == 3:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM usuario INNER JOIN login ON usuario.cedula = login.cedula WHERE login.tipo = "3"')
        dataUsers = cur.fetchall()
        db.connection.commit()
        return render_template('adminadmins.html', usuarios = dataUsers)
    else:
        return redirect(url_for('login'))
    
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

