from flask import Flask, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

app = Flask(__name__)

# Secure secret key
app.secret_key = secrets.token_hex(32)

# Securely hashed passwords
USERS = {
    'admin': generate_password_hash('admin123'),
    'alice': generate_password_hash('alicepass'),
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        # Verify password using secure hash comparison
        if u in USERS and check_password_hash(USERS[u], p):
            session['user'] = u
            return redirect('/dashboard')

        return 'Wrong credentials'

    return '''
    <form method="POST">
        <input name="username" placeholder="Username">
        <input name="password" type="password" placeholder="Password">
        <button type="submit">Login</button>
    </form>
    '''

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    return f'Welcome, {session["user"]}! <a href="/logout">Logout</a>'

@app.route('/logout')
def logout():
    # Clear the entire session
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)