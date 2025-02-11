# app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('billing.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        stock = request.form['stock']
        price = request.form['price']
        conn = get_db_connection()
        conn.execute('INSERT INTO items (id, name, stock, price) VALUES (?, ?, ?, ?)',
                     (id, name, stock, price))
        conn.commit()
        conn.close()
    return render_template('add_item.html')

@app.route('/update_price', methods=['GET', 'POST'])

def update_price():
    if request.method == 'POST':
        id = request.form['id']
        price = request.form['price']
        conn = get_db_connection()
        conn.execute('UPDATE items SET price = ? WHERE id = ?', (price, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('update_price.html')

@app.route('/update_stock', methods=['GET', 'POST'])
def update_stock():
    if request.method == 'POST':
        id = request.form['id']
        stock = request.form['stock']
        conn = get_db_connection()
        conn.execute('UPDATE items SET stock = stock + ? WHERE id = ?', (stock, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('update_stock.html')

@app.route('/view_stock')
def view_stock():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('view_stock.html', items=items)

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        items = request.form.getlist('items')
        counts = request.form.getlist('counts')
        conn = get_db_connection()
        total = 0
        for item, count in zip(items, counts):
            conn.execute('UPDATE items SET stock = stock - ? WHERE id = ?', (count, item))
            total += conn.execute('SELECT price FROM items WHERE id = ?', (item,)).fetchone()['price'] * int(count)
        conn.commit()
        conn.close()
        return f"Total Bill: {total} rs"
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('order.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)
