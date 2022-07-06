from flask import Flask, render_template, request, session, redirect, url_for

from backendContents.agente_web import AgenteMalware
from backendContents.entorno_web import Red

class Endpoints():
    @staticmethod
    def home():
        return render_template("home.html")

    @staticmethod
    def introduceDatosGet():
        return render_template("introduceDatos.html") 

    @staticmethod
    def introduceDatosPost():
        session["red"] = Red(NNODOS=request.form['nnodos'], seed=request.form['seed'], ratio_riesgo=request.form['ratio_riesgo'])

        redirect_to = request.args.get('redirect_to', default='/introduceDatos')        
        return redirect(redirect_to)

    @staticmethod
    def inicio_meta():
        if session["red"] is None:
            return render_template("inicio-meta.html", a="no")
        else:
            return render_template("inicio-meta.html", a="yes")

    @staticmethod
    def seleccionaGrafo():
        return render_template("seleccionaGrafo.html")

    @staticmethod
    def ejecutaAlgoritmo():
        return render_template("ejecutaAlgoritmo.html")

    @staticmethod
    def muestraResultados():
        return render_template("muestraResultados.html")
