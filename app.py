
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secreto_seguro'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

usuarios = {
    "admin": {
        "password": generate_password_hash("admin123"),
        "rol": "Administrador"
    },
    "usuario": {
        "password": generate_password_hash("usuario123"),
        "rol": "Usuario"
    }
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.rol = usuarios[username]["rol"]

@login_manager.user_loader
def load_user(user_id):
    if user_id in usuarios:
        return User(user_id)
    return None

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in usuarios and check_password_hash(usuarios[username]['password'], password):
            user = User(username)
            login_user(user)
            flash('¡Bienvenido, {}!'.format(username), 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales incorrectas', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.id, rol=current_user.rol)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
