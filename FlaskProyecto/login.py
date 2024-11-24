from flask import session, redirect, url_for
import bcrypt

users = {
    'usuario1': bcrypt.hashpw('12345'.encode(), bcrypt.gensalt()).decode(),
    'usuario2': bcrypt.hashpw('abcdef'.encode(), bcrypt.gensalt()).decode()
}
def authenticate_user(usuario, contraseña):
    if usuario in users and bcrypt.checkpw(contraseña.encode(), users[usuario].encode()):
        return True
    return False

def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap
