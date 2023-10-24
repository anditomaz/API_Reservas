from flask import Flask, jsonify, make_response
import pyodbc
import json

app = Flask(__name__, static_folder='static')

############################  Alias de conexão ##############################

server = ''
database = 'APIRESERVAS'
username = ''
password = ''

conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = conn.cursor()

#############################################################################

# Autenticação da API
@app.route("/autenticacao_api/<chave>", methods=['GET', 'POST'])
def autenticacao(chave):

    try:
        cursor.execute("SELECT * FROM autenticacao WHERE Chave = ?", (chave,))
        chaveapi = cursor.fetchone()

        if chaveapi:
            return jsonify({'message': 'Autenticado com sucesso'})
        else:
            return jsonify({'message': 'Chave incorreta'})
    except:
        return jsonify({'error': 'Algo de errado aconteceu'})


# Consultar as reservas e suas datas final para entrega do veículo
@app.route("/reservas", methods=['GET'])
def reservasapi():

    try:
        cursor.execute("SELECT A.NomeCliente, B.marca, B.modelo FROM Reservas A INNER JOIN Carros B on B.ID = A.ID_Carro")
        reservas = cursor.fetchall()

        inf_reservas = list()
        for list_reservas in reservas:
            inf_reservas.append(
                {
                    'NomeCliente': list_reservas[0],
                    'Marca': list_reservas[1],
                    'Modelo': list_reservas[2]
                }
            )

        return make_response(
            jsonify(
                mensagem='Lista de reservas',
                dados=inf_reservas
            )
        )
    except Exception as e:
        return jsonify({'error': str(e)})


# Executa a API
app.run(host='0.0.0.0', port=5000)