from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users
        (id INTEGER PRIMARY KEY, username TEXT, password TEXT)
    ''')
    conn.execute("INSERT OR IGNORE INTO users VALUES (1, 'alice', 'password123')")
    conn.execute("INSERT OR IGNORE INTO users VALUES (2, 'bob', 'letmein')")
    conn.commit()
    conn.close()

LOGIN_PAGE = '''
<form method="POST">
    <input name="username" placeholder="Username"><br>
    <input name="password" type="password" placeholder="Password"><br>
    <button type="submit">Login</button>
</form>
{{ msg }}
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''

    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        conn = sqlite3.connect('users.db')

        # ← dangerous (SQL Injection vulnerability)
        query = f"SELECT * FROM users WHERE username='{u}' AND password='{p}'"

        row = conn.execute(query).fetchone()
        conn.close()

        if row:
            msg = f'<p>Welcome, {row[1]}!</p>'
        else:
            msg = '<p>Invalid credentials.</p>'

    return render_template_string(LOGIN_PAGE, msg=msg)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)