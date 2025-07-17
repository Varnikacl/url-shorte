import sqlite3
import string, random
from flask import Flask, request, redirect, render_template

app = Flask(__name__)

# Create database on startup
def init_db():
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls (
                    id INTEGER PRIMARY KEY,
                    long_url TEXT,
                    short_code TEXT UNIQUE
                )''')
    conn.commit()
    conn.close()

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        long_url = request.form['long_url']
        code = generate_code()
        conn = sqlite3.connect('urls.db')
        c = conn.cursor()
        c.execute('INSERT INTO urls (long_url, short_code) VALUES (?, ?)', (long_url, code))
        conn.commit()
        conn.close()
        return render_template('result.html', code=code)
    return render_template('index.html')

@app.route('/<code>')
def redirect_url(code):
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('SELECT long_url FROM urls WHERE short_code = ?', (code,))
    result = c.fetchone()
    conn.close()
    if result:
        return redirect(result[0])
    else:
        return 'Invalid URL', 404

if'__name__' == '__main__':
     init_db()
     app.run(debug=True)