from flask import Flask, render_template, request
import omise
import mysql.connector

app = Flask(__name__, static_folder='templates/styles')

def connectDB():
    mydb = mysql.connector.connect(
        host="178.128.111.50",
        user="admin2",
        passwd="192837465",
        database="payment"
    )
    return mydb

def charge(token):
    omise.api_secret = 'skey_test_528pq8jk1ws5hvq6lyu'
    ch = omise.Charge.create(
        amount=100000,
        currency='thb',
        descption='test',
        ip='127.0.0.1',
        card=token
    )

@app.route("/", methods=['GET'])
def index():
    token = request.args.get("token")

    mydb = connectDB()
    mycursor = mydb.cursor()
    querystr = "SELECT price FROM payment WHERE token = '" + str(token) + "';"
    mycursor.execute(querystr)
    myresult = mycursor.fetchall()
    price = int(myresult[0][0]) * 100
    print(price)
    return render_template('index.html', currency=price)


@app.route("/checkout", methods=['POST'])
def checkout():
    token = request.form.getlist('omiseToken')[0]
    charge(token)
    return render_template('index.html', currency=0)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)