from app import app , categorias
from flask import Flask , render_template
import pymongo

@app.route("/obtenerCategoria")
def obtenerCategoria():
    listaCategoria=categorias.find()
    return render_template("listaProductos.html")