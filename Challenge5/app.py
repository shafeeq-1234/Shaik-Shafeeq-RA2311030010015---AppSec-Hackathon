from flask import Flask, render_template_string

app = Flask(__name__)

# Disable debug mode
app.config['DEBUG'] = False

PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>My App</title>
</head>
<body>
    <h1>Hello, world!</h1>
</body>
</html>
'''

# Add security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

@app.route('/')
def index():
    return render_template_string(PAGE)

@app.route('/error')
def error():
    raise Exception("Internal server error")

if __name__ == '__main__':
    app.run(debug=False)
