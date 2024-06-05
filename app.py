from flask import Flask, redirect, jsonify, request
from flask import render_template
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

init_db()

@app.route('/')
def index():
    try:
        db = get_db()

        cursor = db.cursor()

        cursor.execute("""
            SELECT 
            tv.*, 
            CASE 
                 tv.status
              WHEN 1 THEN 'DISPONÍVEL'
              WHEN 2 THEN 'ALUGADO'
              WHEN 3 THEN 'REPARO'
              ELSE
                 'DESCONHECIDO'
              END status_descricao,
            tmo.nome as modelo, tma.nome as marca
            FROM tb_veiculo tv
            INNER JOIN tb_modelo tmo
            ON tv.id_modelo = tmo.id
            INNER JOIN tb_marca tma
            on tmo.id_marca = tma.id
        """)

        veiculos = cursor.fetchall()

        cursor.execute("""
                    SELECT 
                        CASE status
                            WHEN 1 THEN 'DISPONÍVEL'
                            WHEN 2 THEN 'ALUGADO'
                            WHEN 3 THEN 'REPARO'
                            ELSE 'DESCONHECIDO'
                        END status, 
                        COUNT(*) AS quantidade
                      FROM tb_veiculo
                    GROUP BY status;
                """)

        totais = cursor.fetchall()

        cursor.execute("""
            SELECT tb_modelo.id, tb_modelo.nome as modelo, tb_marca.nome as marca
            FROM tb_modelo
            INNER JOIN tb_marca
            on tb_modelo.id_marca = tb_marca.id
        """)

        modelos = cursor.fetchall()

        return render_template('index.html', veiculos=veiculos, totais=totais, modelos=modelos)
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@app.route('/register', methods=['POST'])
def cadastrar():
    try:
        placa = request.form.get('placa')
        cor = request.form.get('cor')
        ano = request.form.get('ano')
        status = 1
        modelo = request.form.get('modelo')

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO tb_veiculo (placa, cor, ano, status, id_modelo) VALUES (?, ?, ?, ?, ?)", (placa, cor, ano, status, modelo))
        db.commit()
        db.close()
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        return redirect('/')

@app.route('/update/<id>', methods=['POST'])
def atualizar(id):
    try:
        placa = request.form.get('placa')
        cor = request.form.get('cor')
        ano = request.form.get('ano')
        status = request.form.get('status')
        modelo = request.form.get('modelo')

        db = get_db()
        cursor = db.cursor()
        cursor.execute('UPDATE tb_veiculo SET placa = ?, cor = ?, ano = ?, status = ?, id_modelo = ? WHERE id = ?', (placa, cor, ano, status, modelo, id))
        db.commit()
        db.close()
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        return redirect('/')

@app.route('/delete/<id>', methods=['POST'])
def excluir(id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM tb_veiculo WHERE id='"+id+"'")
        db.commit()
        db.close()
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        return redirect('/')
