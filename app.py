from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# DATABASE INIT
def init_db():
    conn = sqlite3.connect('contacts.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# HOME - VIEW CONTACTS
@app.route('/')
def index():
    conn = sqlite3.connect('contacts.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts")
    contacts = cur.fetchall()
    conn.close()
    return render_template('index.html', contacts=contacts)

# ADD CONTACT
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        conn = sqlite3.connect('contacts.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
                    (name, phone, email))
        conn.commit()
        conn.close()

        return redirect('/')
    return render_template('add.html')

# DELETE CONTACT
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('contacts.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# EDIT CONTACT
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('contacts.db')
    cur = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        cur.execute("""
            UPDATE contacts 
            SET name=?, phone=?, email=? 
            WHERE id=?
        """, (name, phone, email, id))

        conn.commit()
        conn.close()
        return redirect('/')

    cur.execute("SELECT * FROM contacts WHERE id=?", (id,))
    contact = cur.fetchone()
    conn.close()

    return render_template('edit.html', contact=contact)

# SEARCH
@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']

    conn = sqlite3.connect('contacts.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM contacts 
        WHERE name LIKE ? OR phone LIKE ?
    """, ('%' + keyword + '%', '%' + keyword + '%'))

    contacts = cur.fetchall()
    conn.close()

    return render_template('index.html', contacts=contacts)

if __name__ == '__main__':
    app.run(debug=True)