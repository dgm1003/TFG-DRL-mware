from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = b'papopi'

@app.route('/', methods=["GET"])
def home():
    return render_template("home.html")


@app.route('/introduceDatos', methods=["GET"])
def introduceDatos():
    return render_template("introduceDatos.html")


@app.route('/introduceDatos/inicio-meta', methods=["GET"])
def inicio_meta():
    return render_template("inicio-meta.html")

@app.route('/seleccionaGrafo', methods=["GET"])
def seleccionaGrafo():
    return render_template("seleccionaGrafo.html")

@app.route('/ejecuta', methods=["GET"])
def ejecutaAlgoritmo():
    return render_template("ejecutaAlgoritmo.html")

@app.route('/resultados', methods=["GET"])
def muestraResultados():
    return render_template("muestraResultados.html")