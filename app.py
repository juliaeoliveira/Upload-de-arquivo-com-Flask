import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from asgiref.wsgi import WsgiToAsgi

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads/eventos_lc')

app = Flask(__name__)
'''
app = Flask(__name__) => cria uma aplicação web
__name__ diz ao Flask:
-onde estão os templates
-onde estão os arquivos estáticos
-como localizar recursos internos
Sem isso, o Flask não sabe onde está o projeto.
'''
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# “Sempre que eu falar em UPLOAD_FOLDER, use esse caminho”

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# o Flask usa o retorno como resposta HTTP
# Toda função de rota precisa retornar algo
@app.route('/')
def upload_page():
    return render_template('upload.html')

'''
return render_template('upload.html')
O que isso faz?
- Carrega um arquivo HTML da pasta templates/
- Processa variáveis (Jinja2)
'''


@app.route('/upload', methods=['POST']) #Upload de arquivos precisa ser POST
def upload_image():
    if 'image' not in request.files:
        return redirect(url_for('upload_page'))

    file = request.files['image'] 
    # request.files['image'] => Dicionário com arquivos enviados
    #A chave ('image') vem do: <input type="file" name="image">

    if file.filename == '':
        return redirect(url_for('upload_page'))

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #.save() grava um arquivo físico no disco

    return redirect(url_for('viewer_page')) #Gera a URL a partir do nome da função


@app.route('/viewer')
def viewer_page():
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    last_image = images[-1] if images else None
    '''
    O sistema:
    - Lê a pasta uploads/
    - Obtém os nomes dos arquivos
    - Usa o último da lista
    '''

    return render_template('viewer.html', image=last_image)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# 🔹 Adaptador ASGI (necessário para Uvicorn)
asgi_app = WsgiToAsgi(app)
