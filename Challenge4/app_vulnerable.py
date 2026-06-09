from flask import Flask, request, session, redirect
import hashlib

app = Flask(__name__)
app.secret_key = 'abc'  # Flaw 1?

USERS = {
    'admin': hashlib.md5(b'admin123').hexdigest(),  # Flaw 2?
    'alice': hashlib.md5(b'alicepass').hexdigest(),
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        hashed = hashlib.md5(p.encode()).hexdigest()

        if USERS.get(u) == hashed:
            session['user'] = u
            return redirect('/dashboard')

        return 'Wrong credentials'

    return '''
    <form method="POST">
        <input name="username">
        <input name="password" type="password">
        <button>Login</button>
    </form>
    '''

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    return f'Welcome, {session["user"]}! <a href="/logout">Logout</a>'

@app.route('/logout')
def logout():
    session.pop('user', None)  # Flaw 3?
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)