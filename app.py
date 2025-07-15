from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Crear la base de datos si no existe
def init_db():
    conn = sqlite3.connect('viajes.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS recomendaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destino TEXT,
            descripcion TEXT,
            enlace TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Ruta principal
@app.route('/')
def index():
    conn = sqlite3.connect('viajes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM recomendaciones')
    recomendaciones = c.fetchall()
    conn.close()
    return render_template('index.html', recomendaciones=recomendaciones)

# Ruta para agregar recomendación
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        destino = request.form['destino']
        descripcion = request.form['descripcion']
        enlace = request.form['enlace']

        conn = sqlite3.connect('viajes.db')
        c = conn.cursor()
        c.execute('INSERT INTO recomendaciones (destino, descripcion, enlace) VALUES (?, ?, ?)',
                  (destino, descripcion, enlace))
        conn.commit()
        conn.close()

        return redirect('/')
    return render_template('add.html')

# Ruta para eliminar recomendación
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('viajes.db')
    c = conn.cursor()
    c.execute('DELETE FROM recomendaciones WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=81, debug=True)
