from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flasgger import Swagger
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.by import By

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'minha_chave'  # Troque por uma chave segura

# Inicializa JWT e Swagger
jwt = JWTManager(app)

swagger = Swagger(app,  template={
    "info": {
        "title": "API Vitivinicultura Embrapa",
        "description": "Consulta dados públicos de vitivinicultura (produção, importação, exportação, etc.) direto do site da Embrapa. API protegida com JWT. Obtenha um token via /login.",
        "version": "1.0"
    }
})

def get_routes(link, aba, sep):
    # URL da aba desejada (por exemplo, "Processamento")
    url = link

    # Configurações do Selenium em modo headless
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    # Acessar a página
    driver.get(url)

    # Capturar HTML da página
    html = driver.page_source

    # Encerrar o Selenium (não precisamos mais dele)
    driver.quit()

    # Usar BeautifulSoup para analisar a página
    soup = BeautifulSoup(html, 'html.parser')

    # Procurar o primeiro link que contenha 'download' no href
    link_download = soup.find('a', href=aba)

    print(link_download)

    if link_download:
        href = link_download['href']
        full_url = 'http://vitibrasil.cnpuv.embrapa.br/' + href

        # Fazer o download com requests
        response = requests.get(full_url)

        # Salvar o arquivo
        filename = full_url.split('/')[-1]
        with open(filename, 'wb') as f:
            f.write(response.content)

        print(f"Arquivo salvo como: {filename}")
    else:
        print("Link de download não encontrado.")


    df = pd.read_csv(BytesIO(response.content), sep=sep)

    return df.head(100).to_dict(orient='records')

USUARIOS = {
    "admin": "admin123"
}

@app.route('/login', methods=['POST'])
def login():
    """
    Faz login e retorna um token JWT.
    ---
    parameters:
      - name: username
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
    responses:
      200:
        description: Token JWT gerado
    """
    username = request.form.get('username')
    password = request.form.get('password')

    if username in USUARIOS and USUARIOS[username] == password:
        access_token = create_access_token(identity=username)
        return jsonify(token=access_token), 200
    else:
        return jsonify(msg="Usuário ou senha inválidos"), 401

@app.route('/api/producao', methods=['GET'])
@jwt_required()
def producao():
    """
        Retorna os dados de produção, requer autenticação.
        ---
        responses:
          200:
            description: Dados da aba de produção
    """
    dados = get_routes('http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02','download/Producao.csv', sep=";")
    return jsonify(dados)

@app.route('/api/processamento', methods=['GET'])
@jwt_required()
def processamento():
    """
        Retorna os dados de processamento, requer autenticação.
        ---
        responses:
          200:
            description: Dados da aba de processamento
    """
    dados = get_routes('http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03', 'download/ProcessaViniferas.csv', sep=";")
    return jsonify(dados)

@app.route('/api/comercializacao', methods=['GET'])
@jwt_required()
def comercializacao():
    """
        Retorna os dados de comercialização, requer autenticação.
        ---
        responses:
          200:
            description: Dados da aba de comercialização
    """
    dados = get_routes('http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04', 'download/Comercio.csv', sep=";")
    return jsonify(dados)

@app.route('/api/importacao', methods=['GET'])
@jwt_required()
def importacao():
    """
        Retorna os dados de importação, requer autenticação.
        ---
        responses:
          200:
            description: Dados da aba de importação
    """
    dados = get_routes('http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05', 'download/ImpVinhos.csv', sep="\t")
    return jsonify(dados)

@app.route('/api/exportacao', methods=['GET'])
@jwt_required()
def exportacao():
    """
        Retorna os dados de exportação, requer autenticação.
        ---
        responses:
          200:
            description: Dados da aba de exportação
    """
    dados = get_routes('http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06', 'download/ExpVinho.csv', sep="\t")
    return jsonify(dados)

if __name__ == '__main__':
    app.run(debug=True)
