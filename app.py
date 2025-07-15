from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# Conexión a PostgreSQL usando DATABASE_URL de Render
DATABASE_URL = os.environ.get('DATABASE_URL')

# Crear la tabla si no existe
def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS recomendaciones (
            id SERIAL PRIMARY KEY,
            destino TEXT,
            descripcion TEXT,
            enlace TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Ruta principal: mostrar recomendaciones
@app.route('/')
def index():
    conn = psycopg2.connect(DATABASE_URL)
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

        conn = psycopg2.connect(DATABASE_URL)
        c = conn.cursor()
        c.execute('INSERT INTO recomendaciones (destino, descripcion, enlace) VALUES (%s, %s, %s)',
                  (destino, descripcion, enlace))
        conn.commit()
        conn.close()

        return redirect('/')
    return render_template('add.html')

# Ruta para eliminar recomendación
@app.route('/delete/<int:id>')
def delete(id):
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    c.execute('DELETE FROM recomendaciones WHERE id=%s', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Ruta para ver datos crudos (para pruebas)
@app.route('/verdb')
def verdb():
    conn = psycopg2.connect(DATABASE_URL)
    c = conn.cursor()
    c.execute('SELECT * FROM recomendaciones')
    data = c.fetchall()
    conn.close()
    return str(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=81, debug=True)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=81, debug=True)

