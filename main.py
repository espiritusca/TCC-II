from flask import Flask, jsonify, request, make_response
import sqlite3
from flask_cors import CORS
from meu_banco_de_dados import get_database

app = Flask(__name__)
CORS(app, origins=["*"])

@app.before_request
def before_request():
    headers = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
               'Access-Control-Allow-Headers': 'Content-Type'}
    if request.method.lower() == 'options':
        return jsonify(headers), 200

# Função para buscar pacientes da base de dados
def get_pacientes():
    db = get_database()
    rows = db.fetch_patients()
    db.close()
    pacientes = [{'id': row[0], 'nome': row[1], 'idade': row[2], 'contato': row[3]} for row in rows]
    return pacientes


# Rota para buscar dados dos pacientes
@app.route('/api/pacientes', methods=['GET', 'POST'])
def api_pacientes():
    if request.method == 'GET':
        response = make_response(jsonify(get_pacientes()))
        response.headers["Content-Type"] = "application/json"
        return response, 200
    if request.method == 'POST':
        body = request.json
        db = get_database()
        # todo: validar os dados que vem do cliente, pois nem tudo que vem é válido
        # {"nome": " ", "contato": "", "idade": 24.1}
        # todo: quando o cliente mandar uma requisicao errada, devolver um status code 400(bad request)
        db.insert_patient(nome=body['nome'], contato=body['contato'], idade=body['idade'])
        # todo se o dado foi registrado no banco, nao preciso chamar o banco para retornar os mesmo dados que ja tenho em memoria
        db.cursor.execute("select id, nome, idade, contato from pacientes order by id desc")
        paciente = db.cursor.fetchone()
        db.close()
        return jsonify({'id': paciente[0], 'nome': paciente[1], 'idade': paciente[2], 'contato': paciente[3]})


@app.route('/api/pacientes/<int:paciente_id>', methods=['PUT'])
def update_paciente(paciente_id):
    print("id do paciente: ", paciente_id)
    db = get_database()
    body = request.json
    # todo: caso o paciente na exista, entao devolver um status code 404 informando em um json que o paciente nao foi encontrado
    db.cursor.execute("update pacientes set nome = ?, contato = ? , idade = ? where id = ?",
                      (body["nome"], body["contato"], body["idade"], paciente_id)
                      )
    db.conn.commit()
    db.close()
    # se o dado foi registrado no banco, nao preciso chamar o banco para retornar os mesmo dados que ja tenho em memoria
    return jsonify({'id': paciente_id, 'nome': body["nome"], 'idade': body["idade"], 'contato': body["contato"]})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
