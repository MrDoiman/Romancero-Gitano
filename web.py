from flask import Flask, render_template, request, redirect
import random

app = Flask(__name__)

romances = []

def cargar_romances():
    with open("romances.txt", "r") as archivo:
        romance_actual = None
        for linea in archivo:
            if linea.startswith("Título:"):
                if romance_actual is not None:
                    romances.append(romance_actual)
                romance_actual = {"título": linea.strip().split(":")[1].strip(), "fragmentos": []}
            else:
                romance_actual["fragmentos"].append(linea.strip())

        if romance_actual is not None:
            romances.append(romance_actual)

@app.route("/", methods=["GET", "POST"])
def jugar():
    global romances

    if request.method == "GET":
        if not romances:
            cargar_romances()
            if not romances:
                return render_template("fin_juego.html")

        indice_romance = random.randint(0, len(romances) - 1)
        romance = romances[indice_romance]
        fragmentos = romance["fragmentos"]
        if len(fragmentos) <= 5:
            fragmento = "\n".join(fragmentos)
            del romances[indice_romance]
        else:
            inicio = random.randint(0, len(fragmentos) - 5)
            fin = inicio + 5
            fragmento = "\n".join(fragmentos[inicio:fin])
            romance["fragmentos"] = fragmentos[fin:]

        return render_template("juego.html", fragmento=fragmento, titulo=romance["título"])

    elif request.method == "POST":
        titulo = request.form["titulo"]

        if not romances:
            return redirect("/")

        mensaje = "Incorrecto"
        titulo_correcto = None
        for romance in romances:
            if titulo == romance["título"]:
                mensaje = "Correcto"
                romances.remove(romance)
                break
            else:
                titulo_correcto = romance["título"]

        return render_template("resultado.html", mensaje=mensaje, titulo_correcto=titulo_correcto)

if __name__ == "__main__":
    app.run()
