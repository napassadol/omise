from flask import Flask, render_template, request
import omise
app = Flask(__name__)

def charge(token):
    omise.api_secret = 'skey_test_528pq8jk1ws5hvq6lyu'
    ch = omise.Charge.create(
        amount=100000,
        currency='thb',
        descption='test',
        ip='127.0.0.1',
        card=token
    )

@app.route("/")
def hello():
    return render_template('index.html', currency=2222)

@app.route("/checkout", methods=['POST'])
def test():
    token = request.form.getlist('omiseToken')[0]
    charge(token)
    return render_template('index.html', currency=0)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)