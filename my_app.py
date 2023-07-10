import io
from flask import Flask, jsonify, request, send_file, send_from_directory, render_template
import base64
from pymongo import MongoClient
import ssl

app = Flask(__name__)

# Conexión a la base de datos de MongoDB
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
mongo = MongoClient('mongodb+srv://Luis:Lomaximoluis02@cluster0.f6yp4mn.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true')
db = mongo["ElMana"]
db_platos = db["platos"]

# Variable global para almacenar los platos seleccionados
cart_items = []

@app.route("/platos", methods=["POST"])
def create_plato():
    # Obtener los datos del plato desde la solicitud
    nombre = request.form.get("nombre")
    descripcion = request.form.get("descripcion")
    imagen = request.files.get("imagen")
    precio = float(request.form.get("precio"))

    # Leer los datos binarios de la imagen
    imagen_binaria = imagen.read()

    # Codificar la imagen en base64
    imagen_codificada = base64.b64encode(imagen_binaria).decode("utf-8")

    # Guardar el plato en la base de datos
    plato = {
        "nombre": nombre,
        "descripcion": descripcion,
        "imagen": imagen_codificada,
        "precio": precio
    }
    db_platos.insert_one(plato)

    return "Plato creado exitosamente"

@app.route("/platos", methods=["GET"])
def get_platos():
    platos = db_platos.find()
    platos_list = []
    
    for plato in platos:
        nombre = plato["nombre"]
        descripcion = plato["descripcion"]
        imagen_codificada = plato["imagen"]
        precio = plato["precio"]
        
        plato_dict = {
            "nombre": nombre,
            "descripcion": descripcion,
            "imagen": imagen_codificada,
            "precio": precio
        }
        
        platos_list.append(plato_dict)
    
    return jsonify(platos_list)

@app.route("/cart", methods=["POST"])
def cart():
    global cart_items

    nombre = request.form.get("nombre")
    cantidad = int(request.form.get("cantidad"))

    plato = db_platos.find_one({"nombre": nombre})

    if plato:
        # Verificar si el plato ya está en el carrito
        existing_item = next((item for item in cart_items if item["nombre"] == nombre), None)

        if existing_item:
            # El plato ya está en el carrito, incrementar la cantidad
            existing_item["cantidad"] += cantidad
        else:
            # Agregar el plato al carrito
            cart_items.append({"nombre": nombre, "cantidad": cantidad})

        return "Plato agregado al carrito exitosamente"
    else:
        return "Plato no encontrado"

@app.route("/cart", methods=["GET"])
def get_cart():
    global cart_items

    platos_en_carta = []
    subtotal = 0.0

    for item in cart_items:
        plato = db_platos.find_one({"nombre": item["nombre"]})

        if plato:
            plato_en_carta = {
                "nombre": item["nombre"],
                "imagen": plato["imagen"],
                "cantidad": item["cantidad"],
                "precio": plato["precio"]
            }

            platos_en_carta.append(plato_en_carta)
            subtotal += plato["precio"] * item["cantidad"]

    return jsonify({"platos_en_carta": platos_en_carta, "subtotal": subtotal})


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/menu")
def menu():
    platos = db_platos.find()
    return render_template("menu.html", platos=platos)

@app.route("/carta")
def carta():
    return render_template("carta.html")

@app.route("/mapa")
def mapa():
    return render_template("mapa.html")

if __name__ == "__main__":
    app.run(debug=True, port=7000)
