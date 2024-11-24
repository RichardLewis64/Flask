from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from model import train_model, train_clustering, train_logistic_regression
from data_loader import load_data
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'login'
#app.config['MYSQL_SSL_DISABLED'] = True  # Desactivar SSL
app.config['MYSQL_CONNECT_ARGS'] ={'ssl_disabled': False}  # This line forces SSL off

app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM Usuarios')
    dato=cur.fetchall()
    print('dato')
#    if 'loggedin' in session:
    return render_template('index.html')


@app.route('/add_contact')
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur= mysql.connection.cursor()
        cur.execute('INSERT INTO usuarios (email, fullname, phone) VALUES (%s,%s,%s)',(fullname, phone, email))
        mysql.connection.commit()
        flash('usuario agregado satisfied')
    return redirect(url_for('index.html'))

@app.route('/editar_contact')
def edit_contact():
    return 'edit_contact'
"""
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('loggedin', None)
    return redirect(url_for('login'))
"""
@app.route('/registrar')
def registrar():
    return render_template('registrar.html')



@app.route('/data', methods=['POST'])   #se quito el get
def data_view():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            try:
                data = load_data(file)
                return render_template('data.html', data=data.to_html())
            except Exception as e:
                return render_template('data.html', error=str(e))
    return render_template('data.html')

@app.route('/ml_models', methods=['GET', 'POST'])
def ml_models_view():
    if request.method == 'POST':
        model_type = request.form['model_type']
        data = load_data()  # Load data from session or database
        try:
            if model_type == 'linear_regression':
                model, mse = train_model(data)
                return render_template('ml_models.html', result=f'MSE: {mse}')
            elif model_type == 'clustering':
                labels = train_clustering(data)
                return render_template('ml_models.html', result=f'Labels: {labels}')
            elif model_type == 'logistic_regression':
                model, accuracy = train_logistic_regression(data)
                return render_template('ml_models.html', result=f'Accuracy: {accuracy}')
        except Exception as e:
            return render_template('ml_models.html', error=str(e))
    return render_template('ml_models.html')

if __name__ == '__main__':
    app.run(port=3005 , debug=True)
