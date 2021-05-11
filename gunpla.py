from flask import Flask, jsonify, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'eunhye'
app.config['MYSQL_DB'] = 'gunpladb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['JSON_SORT_KEYS'] = False

db = MySQL(app)


@app.route("/")
def index():
    query = 'select * from mechanic'
    cur = db.connection.cursor()
    cur.execute(query)
    return render_template('list.html', list=cur.fetchall())


@app.route("/mechanic", methods=["GET"])
def mechanic():
    query = 'select * from mechanic'
    cur = db.connection.cursor()
    cur.execute(query)
    return jsonify(cur.fetchall())


@app.route("/insert", methods=["GET", "POST"])
def insert():
    if request.method == 'GET':
        return render_template('insert.html')
    elif request.method == 'POST':
        query = 'insert into mechanic values (null, %s, %s, %s, %s, %s, %s)'
        # print(request.form)
        params = (
            request.form['name'],
            request.form['model'],
            request.form['manufacturer'],
            request.form['armor'],
            float(request.form['height']),
            float(request.form['weight'])
        )
        cur = db.connection.cursor()
        cur.execute(query, params)
        db.connection.commit()
        return index()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
