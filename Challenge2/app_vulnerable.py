from flask import Flask, request, render_template_string, make_response

app = Flask(__name__)

comments = []

PAGE = '''
<h2>Comments</h2>

{% for c in comments %}
    <div>{{ c | safe }}</div>
{% endfor %}

<form method="POST">
    <textarea name="comment" placeholder="Leave a comment..."></textarea><br>
    <button type="submit">Post</button>
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Stored directly — no sanitisation!
        comments.append(request.form['comment'])

    resp = make_response(
        render_template_string(PAGE, comments=comments)
    )

    # No HttpOnly flag!
    resp.set_cookie('session', 'SUPERSECRET42')

    return resp

if __name__ == '__main__':
    app.run(debug=True)