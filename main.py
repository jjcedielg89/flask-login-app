from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'mi_clave_super_secreta'

# Usuarios permitidos
usuarios = {
    "admin": "1234",
    "usuario1": "clave1"
}

# Función para registrar la actividad del usuario
def registrar_evento(usuario, accion):
    with open("log_actividad.txt", "a") as archivo:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        archivo.write(f"[{timestamp}] Usuario: {usuario} - Acción: {accion}\n")

# Página principal (login)
@app.route('/')
def home():
    if 'usuario' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# Procesar login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in usuarios and usuarios[username] == password:
        session['usuario'] = username
        registrar_evento(username, "Inicio de sesión")
        return redirect(url_for('dashboard'))
    return "Usuario o contraseña incorrectos. <a href='/'>Volver</a>"

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        registrar_evento(session['usuario'], "Accedió al Dashboard")
        return f"""
            <h2>Bienvenido, {session['usuario']}!</h2>
            <p>Haz clic en el siguiente enlace para acceder a Milesight Cloud:</p>
            <a href="https://cloud.milesight-iot.com/#/index/login" target="_blank">Ir a Milesight</a><br><br>
            <a href="/logout">Cerrar sesión</a>
        """
    return redirect(url_for('home'))

# Logout
@app.route('/logout')
def logout():
    if 'usuario' in session:
        registrar_evento(session['usuario'], "Cerró sesión")
    session.pop('usuario', None)
    return redirect(url_for('home'))

# Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)
