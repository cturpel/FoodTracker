from flask import Flask, render_template, g, request
import sqlite3

app = Flask(__name__)

def connect_db():
    sql = sqlite3.connect('data.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/view')
def view():
    return render_template('day.html')

@app.route('/food', methods=['GET', 'POST'])
def food():
    db = get_db()

    if request.method == 'POST':
        name = request.form['food-name']
        fat = int(request.form['fat'])
        protein = int(request.form['protein'])
        carbohydrates = int(request.form['carbohydrates'])
        calories = protein * 4 + carbohydrates * 4 + fat * 9
        db.execute('INSERT INTO food (name, protein, carbohydrates, fat, calories) VALUES (?,?,?,?,?)', [name, protein, carbohydrates, fat, calories])
        db.commit()

    cur = db.execute('SELECT name, protein, carbohydrates, fat, calories FROM food')
    results = cur.fetchall()

    return render_template('add_food.html', results= results)


if __name__ == '__main__':
    app.run(debug=True)