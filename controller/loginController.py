# aqui importamos la instancia de la aplicacion flask y la coleccion de usuarios 
from app import app, db
from flask import render_template, request, redirect, url_for, session
from mongoengine import Document, StringField, IntField, ReferenceField
import json
import urllib.request


###### Modelo
class Usuarios(db.Document):
    correo = db.StringField(required=True)
    contraseña = db.StringField(required=True)
 
    
@app.route("/")
def Login():
    return render_template ("login.html")
@app.route("/", methods=["GET", "POST"])
def login():
    mensaje = None
    if request.method == "POST":
        correo = request.form.get("correo")
        contraseña = request.form.get("contraseña")
        recaptcha_response = request.form.get("g-recaptcha-response") 
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values ={
            'secret': '6Lfk2MYpAAAAACamgvV3nWjGQvB46OTnEAvwiQjj',
            'response': recaptcha_response 
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
        
        if result['success']:
            usuario = Usuarios.objects(correo=correo, contraseña=contraseña).first()
            if usuario:
                session["correo"] = correo
                return redirect(url_for("home"))
            else:
                mensaje = "Datos no válidos"
        else:
            mensaje = "Captcha no válido"

    return render_template("login.html", mensaje=mensaje)


@app.route("/salir")
def salir():
    session.clear()
    mensaje="Se ha cerrado sesion"
    return render_template("login.html",mensaje=mensaje)