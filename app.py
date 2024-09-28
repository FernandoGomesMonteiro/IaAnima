from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Função para conectar ao banco de dados SQLite
def get_db_connection():
    conn = sqlite3.connect('data/user_data.db')
    conn.row_factory = sqlite3.Row
    return conn

# Página inicial - tela de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_or_name = request.form['email_or_name']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM user WHERE email = ? OR nome = ?", (email_or_name, email_or_name)).fetchone()
        conn.close()

        if user and check_password_hash(user['senha'], password):
            session['user_id'] = user['id']
            session['nome'] = user['nome']
            return redirect(url_for('dashboard'))
        else:
            flash('Login inválido. Verifique suas credenciais.')
            return redirect(url_for('login'))
    return render_template('login.html')

# Página de criação de conta
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        idade = request.form['idade']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('As senhas não coincidem!')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        conn.execute("INSERT INTO user (nome, email, idade, senha, data_criacao) VALUES (?, ?, ?, ?, ?)",
                     (nome, email, idade, hashed_password, datetime.now()))
        conn.commit()
        conn.close()
        flash('Conta criada com sucesso! Faça login.')
        return redirect(url_for('login'))
    return render_template('register.html')

# Dashboard com formulário de mensagem, nível de ansiedade e depressão
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        flash('Faça login para acessar o dashboard.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        mensagem = request.form['mensagem']
        nivel_ansiedade = float(request.form['nivel_ansiedade'])
        nivel_depressao = float(request.form['nivel_depressao'])

        conn = get_db_connection()
        conn.execute("INSERT INTO chat_memory (id_user, mensagem, nivel_ansiedade, nivel_depressao, data_criacao) VALUES (?, ?, ?, ?, ?)",
                     (session['user_id'], mensagem, nivel_ansiedade, nivel_depressao, datetime.now()))
        conn.commit()
        conn.close()
        flash('Dados salvos com sucesso!')
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', nome=session['nome'])

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
