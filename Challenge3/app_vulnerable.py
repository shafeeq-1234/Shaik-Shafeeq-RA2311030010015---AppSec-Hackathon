from flask import Flask, request, session, render_template_string

app = Flask(__name__)
app.secret_key = 'dev'

INVOICES = {
    1: {'owner': 'alice', 'amount': '$1,200', 'item': 'Consulting'},
    2: {'owner': 'alice', 'amount': '$850', 'item': 'Design Work'},
    3: {'owner': 'bob', 'amount': '$4,500', 'item': 'Server Costs'},
}

@app.route('/')
def home():
    session['user'] = 'alice'  # simulate logged-in alice
    return 'Logged in as alice. Try /invoice/1 or /invoice/3'

@app.route('/invoice/<int:inv_id>')
def view_invoice(inv_id):
    inv = INVOICES.get(inv_id)

    if not inv:
        return 'Not found', 404

    # BUG: no ownership check here!
    return render_template_string(
        '<h2>Invoice #{{ id }}</h2><p>{{ inv.item }}: {{ inv.amount }}</p>',
        id=inv_id,
        inv=inv
    )

if __name__ == '__main__':
    app.run(debug=True)