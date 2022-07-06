
from flask import Flask, render_template, request, session
import os
import inspect
from frontendContents.endpoints import Endpoints

app = Flask(
    __name__#,
    #static_folder='../frontendContents/static',
    #template_folder='../frontendContents/templates'
)
app.secret_key = b'papopi'

@app.route('/', methods=["GET"])
def home():
    return Endpoints.home()

@app.route('/introduceDatos', methods=["GET"])
def introduceDatosGet():
    return Endpoints.introduceDatosGet()

@app.route('/introduceDatos', methods=["POST"])
def introduceDatosPost():
    return Endpoints.introduceDatosPost()

@app.route('/introduceDatos/inicio-meta', methods=["GET"])
def inicio_metaGet():
    return Endpoints.inicio_metaGet()

@app.route('/introduceDatos/inicio-meta', methods=["POST"])
def inicio_metaPost():
    return Endpoints.inicio_metaPost()

@app.route('/seleccionaGrafo', methods=["GET"])
def seleccionaGrafoGet():
    return Endpoints.seleccionaGrafoGet()

@app.route('/seleccionaGrafo', methods=["POST"])
def seleccionaGrafoPost():
    return Endpoints.seleccionaGrafoPost()

@app.route('/ejecuta', methods=["GET"])
def ejecutaAlgoritmo():
    return Endpoints.ejecutaAlgoritmo()

@app.route('/resultados', methods=["GET"])
def muestraResultados():
    return Endpoints.muestraResultados()

if __name__ == '__main__':

    app.run(
        host='127.0.0.1',
        port=8080,
        debug=True
    )