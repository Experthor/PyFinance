from wsgiref.validate import validator
from flask import Flask, render_template, url_for, request, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
import psycopg2
from conectar import conectar
from wtforms import Form, StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired
import os

class SignInForm(FlaskForm):
    Nickname=StringField('Nickname', validators=[validators.DataRequired()])
    Nombre=StringField('Nombre', validators=[validators.DataRequired()])
    Apellidos=StringField('Apellidos',validators=[validators.DataRequired()])
    Correo=StringField('Correo', validators=[validators.DataRequired()])
    Contrasena=PasswordField('Contrasena', validators=[validators.DataRequired()]) 
    submit=SubmitField('Registrar')

class LoginForm(FlaskForm):
    Correo=StringField('Correo', validators=[DataRequired()])
    Contrasena=PasswordField('Contrasena', validators=[DataRequired()])
    submit=SubmitField('Iniciar Sesion')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

def load_user(user_id):
    return User(user_id)

login_manager.user_loader(load_user)

#paginas principales
@app.route('/')
def Home():
    return render_template("Home.html", url_for=url_for)

@app.route('/Signin')
def Signin():
    form=SignInForm()
    return render_template("Signin.html",form=form)

@app.route('/Login')
def Login():
    form=LoginForm()
    return render_template("Login.html",form=form)

@app.route('/startPage')
@login_required
def startPage():
    return render_template("startPage.html", url_for=url_for)

#aqui terminan las paginas principales

#rutas para cosas de grupos
@app.route('/htmlsGrupos/grupoFormCreate')
@login_required
def grupoFormCreate():
    return render_template("htmlsGrupos/grupoFormCreate.html", url_for=url_for)

@app.route('/htmlsGrupos/grupoFormJoin')
@login_required
def grupoFormJoin():
    return render_template("htmlsGrupos/grupoFormJoin.html", url_for=url_for)

@app.route('/htmlsGrupos/gruposView')
@login_required
def gruposView():
    return render_template("htmlsGrupos/gruposView.html", url_for=url_for)

#aqui terminan las cosas de grupos

#inician cosas de pagos

@app.route('/htmlsGrupos/htmlsPagos/pagoFormCreate')
@login_required
def pagoFormCreate():
    return render_template("pagosFormCreate.html", url_for=url_for)

@app.route('/htmlsGrupos/htmlsPagos/verPago')
@login_required
def verPago():
    return render_template("verPago.html", url_for=url_for)

#terminan cosas de pagos


'''

@app.route('/Pago', methods=['GET','POST'])
def Pago():
    if request.method=='POST':
        Nombre_pago=request.form.get("Nombre_pago")
        Fecha_pago=request.form.get("Fecha_pago")
        Fecha_creacion=request.form.get("Fecha_creacion")
        Progreso_pago=request.form.get("Progreso_pago")
        Cantidad_pagar=request.form.get("Cantidad_pagar")
        Estatus=request.form.get("Estatus")
        conn.commit()
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute('INSERT INTO Pagos (Nombre_pago,Fecha_pago,Fecha_creacion,Progreso_pago,Cantidad_pagar,Estatus) VALUES (%s,%s,%s,%s,%s,%s);', (Nombre_pago, Fecha_pago, Fecha_creacion, Progreso_pago, Cantidad_pagar, Estatus))
        except(psycopg2.DatabaseError,Exception) as error:
            if str(error) == no_match:
                retorno = "Pago.html"
                print(error)
            finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
            
        return redirect(url_for('confirmacion_pago'))

    return render_template("formulario_de_pagos.html")
    
@app.route('/ver_pagos')
def ver_pagos():
    pagos = obtener_pagos()
    
    return render_template('ver_pagos.html', pagos=pagos)
    
def obtener_pagos():
    conn = None
    try:
        conn = conectar()  # Establece la conexión a la base de datos
        cur = conn.cursor()

        cur.execute('SELECT "Nombre_pago", "Fecha_pago", "Fecha_creacion", "Progreso_pago", "Cantidad_pagar", "Estatus" FROM "Pagos";')
        
        pagos = cur.fetchall()

        return [{
            "Nombre_pago": pago[0],
            "Fecha_pago": pago[1],
            "Fecha_creacion": pago[2],
            "Progreso_pago": pago[3],
            "Cantidad_pagar": pago[4],
            "Estatus": pago[5]
        } for pago in pagos]

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        # Maneja el error según tus necesidades
        return []

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

@app.route('/formulario_grupo')
def formulario_grupo():
    return render_template('formulario_grupo.html')

@app.route('/registrar_grupo', methods=['POST'])
def registrar_grupo():
    nombre_grupo = request.form.get('Nombre_grupo')
    
    id_usuario = obtener_id_usuario_actual()  # Asegúrate de tener esta función implementada
    
    try:
        conn = conectar()
        cur = conn.cursor()

        cur.execute('INSERT INTO Grupos (Nombre_grupo, Id_usuario) VALUES (%s, %s);', (nombre_grupo, id_usuario))
        conn.commit()

        return redirect(url_for('confirmacion_registro_grupo'))

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return "Error al registrar el grupo"

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

@app.route('/confirmacion_registro_grupo')
def confirmacion_registro_grupo():
    return "Grupo registrado exitosamente. ¡Felicidades!"
    

@app.route('/mis_grupos')
def mis_grupos():    
    try:
        conn = conectar()
        cur = conn.cursor()

        cur.execute('SELECT Nombre_grupo FROM Grupos)
        grupos = cur.fetchall()

        return render_template('mis_grupos.html', grupos=grupos)

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return "Error al obtener los grupos del usuario"

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

'''
    
#metodos de recoleccion de datos 

@app.route('/Logout')
@login_required
def Logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('Home'))

@app.route('/SignIn', methods=['POST'])
def SignIn():
    form=SignInForm()
    if form.validate_on_submit() and request.method=='POST':
        Nickname=form.Nickname.data
        Nombre=form.Nombre.data
        Apellidos=form.Apellidos.data
        Correo=form.Correo.data
        Contrasena=form.Contrasena.data
        conn = conectar()
        cur = conn.cursor()
        try:
            cur.execute('INSERT INTO "Usuarios" ("Nickname", "Nombre", "Apellidos", "Correo", "Contrasena") VALUES (%s, %s, %s, %s, %s);', (Nickname, Nombre, Apellidos, Correo, Contrasena))
            conn.commit()
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
            # Maneja el error según tus necesidades
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
        return render_template("Home.html")
    else:
        return render_template("SignIn.html", form=form)


@app.route("/LogIn", methods=['POST'])
def LogIn():
    logout_user()
    form=LoginForm()
    if form.validate_on_submit and request.method=='POST':
        Correo=form.Correo.data
        Contrasena=form.Contrasena.data
        print(Correo, ' ', Contrasena)
        no_match = "El correo y/o la contraseña son incorrectos"
        cur = None
        try:
            conn = conectar()
            cur=conn.cursor()
            cur.execute('SELECT "Correo", "Contrasena", "ID_usuario" FROM "Usuarios" WHERE "Correo" = %s AND "Contrasena" = %s;', (Correo, Contrasena))
            r = cur.fetchall()
            if len(r) == 0:
                print('1')
                raise Exception(no_match)
            else:
                print('0')
                print(r[0][0], ' ', r[0][1], ' ', r[0][2])
                user_id = r[0][2]
                user = User(user_id)
                login_user(user)
        except (psycopg2.DatabaseError, Exception) as error:
            print(type(error))
            if str(error)==no_match:
                print('1')
                return redirect(url_for('Login'))
            print(error)   
            print('0')
        finally:
            if cur is not None:
                cur.close()
                if conn is not None:
                    conn.close()
                    return redirect(url_for('startPage'))
    else:
        return render_template("Login.html")

if __name__ == '__main__':
    app.run(debug=True)