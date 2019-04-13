from flask import Flask, render_template, request
import omise
import mysql.connector

app = Flask(__name__, static_folder='templates/styles')

def connectDB():
    mydb = mysql.connector.connect(
        host="68.183.227.154",
        user="admin2",
        passwd="192837465",
        database="payment"
    )
    return mydb

def charge(token, db_token):
    omise.api_secret = 'skey_test_528pq8jk1ws5hvq6lyu'
    ch = omise.Charge.create(
        amount=100000,
        currency='thb',
        descption='test',
        ip='127.0.0.1',
        card=token
    )
    if ch._attributes['paid']:
        mydb = connectDB()
        mycursor = mydb.cursor()
        sql = "UPDATE payment SET pay_status = 1 WHERE token = '" + db_token + "'"
        mycursor.execute(sql)
        mydb.commit()
        return True
    else:
        return False

@app.route("/", methods=['GET'])
def index():
    token = request.args.get("token")

    mydb = connectDB()
    mycursor = mydb.cursor()
    querystr = "SELECT price, pay_status FROM payment WHERE token = '" + str(token) + "';"
    mycursor.execute(querystr)
    myresult = mycursor.fetchall()
    if int(myresult[0][1]) == 1:
        return render_template('success.html')
    else:
        price = int(myresult[0][0]) * 100
        return render_template('index.html', currency=price, db_token=token)


@app.route("/checkout", methods=['POST'])
def checkout():
    token = request.form.getlist('omiseToken')[0]
    db_token = request.form.getlist('db_token')[0]
    if token != '':
        ret = charge(token, db_token)
    else:
        return render_template('fail.html')

    if ret == True:
        return render_template('success.html')
    else:
        return render_template('fail.html')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)