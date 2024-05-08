from app import app, db
from flask import render_template, request, redirect, url_for, session, flash
import os
from bson.objectid import ObjectId
from mongoengine.errors import ValidationError
from models.model import productos,categorias,usuarios





@app.route("/home")
def home():
    if "correo" in session:
        todosProductos = []
        listaProductos = productos.objects()
        
        return render_template("listarProductos.html", productos=listaProductos)
    else:
        mensaje ="Debe ingresar con sus datos"
        return render_template("login.html", mensaje=mensaje)
    
@app.route("/vistaAgregarProducto")
def vistaAgregarProducto():
    mensaje = None
    if "correo" in session:
        listaCategorias = categorias.objects()
        return render_template("formulario.html", categorias=listaCategorias)
    else:
        mensaje = "Debe ingresar con sus datos"
        return render_template("login.html", mensaje=mensaje)


@app.route('/vistaAgregarProducto', methods=['POST'])
def agregarProducto():
    if request.method == 'POST':
        codigo = int(request.form['codigo'])
        nombre = request.form['nombre']
        precio = int(request.form['precio'])
        categoria = request.form['categoria']
        foto = request.files['imagen']
        

        producto = productos(codigo=codigo,nombre=nombre,precio=precio, categoria=categoria)
        print(producto.nombre)
        producto.save() 
        
        nombreFoto = os.path.join(app.config["UPLOAD_FOLDER"], str(producto.id)) + ".jpg"

        # nombreFoto = (os.path.join(app.config["UPLOAD_FOLDER"]))/{producto.id}+".jpg"
        
        
        nombreFoto = os.path.join(app.config["UPLOAD_FOLDER"], f"{producto.id}.jpg")

        foto.save(nombreFoto)
        
        


        flash('Producto agregado correctamente', 'success') 
        return redirect(url_for('home'))

    else:
        listaProductos = productos.objects().all()
        return render_template('home', productos=listaProductos)



@app.route("/editar_producto/<producto_id>", methods=["GET"])
def editar_producto(producto_id):
    if "correo" in session:
        try:
            producto = productos.objects(id=ObjectId(producto_id)).first()
            if producto:
                listaCategorias = categorias.objects()
                return render_template("EditarProducto.html", producto=producto, categorias=listaCategorias)
            else:
                return "Producto no encontrado."
        except ValidationError as error:
            print("Error al editar el producto", error)
            mensaje = "Error al editar el producto"
    else:
        mensaje = "Debe ingresar con sus datos"
        return render_template("login.html", mensaje=mensaje)

@app.route("/actualizar_Producto/<producto_id>", methods=["POST"])
def actualizar_producto(producto_id):
    if "correo" in session:
        try:
            codigo = int(request.form["codigo"])
            nombre = request.form["nombre"]
            precio = int(request.form["precio"])
            idCategoria = request.form["categoria"]
            foto = request.files["imagen"]

            producto_actualizado = {
                "codigo": codigo,
                "nombre": nombre,
                "precio": precio,
                "categoria": categorias.objects.get(id=idCategoria)
            }

            productos.objects(id=producto_id).update(**producto_actualizado)

            if foto:
                nombreFoto = f"{producto_id}.jpg"
                foto.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreFoto))

            return redirect(url_for("home"))

        except ValidationError as error:
            print("Error al actualizar el producto", error)
            mensaje = "Error al actualizar el producto"
    else:
        mensaje = "Debe ingresar con sus datos"
        return render_template("login.html", mensaje=mensaje)
    
    
    



@app.route("/eliminar_producto/<producto_id>", methods=["POST"])
def eliminar_producto(producto_id):
    if "correo" in session:
        try:
            resultado = productos.objects(id=producto_id).delete()
            if resultado == 1:
                return redirect(url_for("home"))
            else:
                return "Producto no encontrado."
        except ValidationError as error:
            print("Error al eliminar el producto", error)
            mensaje = "Error al eliminar el producto"
    else:
        mensaje = "Debe ingresar con sus datos"
        return render_template("login.html", mensaje=mensaje)