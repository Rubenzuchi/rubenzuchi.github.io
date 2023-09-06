from cs50 import SQL
from flask import Flask,render_template, request

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///notas.db")

@app.route("/")
def index():
    tabla = db.execute("SELECT * FROM notas")
    return render_template("index.html", tabla=tabla)

@app.route("/selectividad", methods=["GET", "POST"])
def selectividad():
    if request.method == "POST":
        notas = request.form.getlist("notas")
        nota1 = float(notas[0])
        nota2 = float(notas[1])
        examen1 = float(notas[2])
        examen2 = float(notas[3])
        examen3 = float(notas[4])
        examen4 = float(notas[5])
        opt1 = float(notas[6])
        opt2 = float(notas[7])
        nota_final = (((nota1 + nota2) / 2) * 0.6) + (((examen1 + examen2 + examen3 + examen4) / 4) * 0.4) + (((opt1 + opt2) / 2) * 0.2)
        tabla = db.execute("SELECT curso, universidad, peticion, grado, centro, area, general FROM notas WHERE general <= ? ORDER BY general DESC", nota_final)

    else:
        nota1 = ""
        nota2 = ""
        examen1 = ""
        examen2 = ""
        examen3 = ""
        examen4 = ""
        opt1 = ""
        opt2 = ""
        nota_final = ""
        tabla = db.execute("SELECT curso, universidad, peticion, grado, centro, area, general FROM notas ORDER BY grado")

    return render_template("selectividad.html", nota1=nota1, nota2=nota2, examen1=examen1, examen2=examen2, examen3=examen3, examen4=examen4, opt1=opt1, opt2=opt2, nota_final=nota_final, tabla=tabla)

@app.route("/carreras", methods=["GET", "POST"])
def carreras():
    if request.method == "POST":
        carrera = request.form.get("carrera")
        tabla = db.execute("SELECT * FROM notas WHERE grado LIKE ?", "%" + carrera + "%")
        return render_template("carreras.html", tabla=tabla)
    else:
        return render_template("carreras.html")
