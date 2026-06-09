from flask import Flask, render_template_string

app = Flask(__name__)
app.config['DEBUG'] = True  # shipped to "production"

PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>My App</title>
</head>
<body>
    <h1>Hello, world!</h1>
    <iframe src="https://evil.com"></iframe>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(PAGE)

@app.route('/error')
def error():
    raise Exception(
        "Database config: host=10.0.0.1, db=prod_users, pass=hunter2"
    )

if __name__ == '__main__':
    app.run()