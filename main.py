from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import requests

app = Flask(__name__)
app.secret_key = 'mi_clave_super_secreta'

# Usuarios permitidos
usuarios = {
    "admin": "1234",
    "usuario1": "clave1"
}

# Función para registrar evento en Google Sheets
def registrar_evento_en_sheets(usuario, accion):
    url = "https://script.google.com/macros/s/AKfycbzco4XBT-yo9nJSBEF97xAasnL48LHZjTsei5w5VB9fkwRvlh7e6xB3k_vmOsJUQZXroQ/exec"  # Coloca la URL de tu API de Google Apps Script aquí
    payload = {
        'usuario': usuario,
        'accion': accion
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print("Error al registrar el evento en Google Sheets.")

@app.route('/')
def home():
    if 'usuario' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in usuarios and usuarios[username] == password:
        session['usuario'] = username
        registrar_evento_en_sheets(username, "Inicio de sesión")
        return redirect(url_for('dashboard'))
    return "Usuario o contraseña incorrectos. <a href='/'>Volver</a>"

@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        registrar_evento_en_sheets(session['usuario'], "Accedió al Dashboard")
        return f"""
            <h2>Bienvenido, {session['usuario']}!</h2>
            <p>Este sería el enlace hacia Milesight Cloud.</p>
            <a href="/logout">Cerrar sesión</a>
        """
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    if 'usuario' in session:
        registrar_evento_en_sheets(session['usuario'], "Cerró sesión")
    session.pop('usuario', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
