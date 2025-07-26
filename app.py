from flask import Flask,jsonify,render_template,request,redirect,url_for
import sqlite3

app = Flask(__name__)

def obtener_conexion():
    conexion = sqlite3.connect("tareas.db")
    conexion.row_factory = sqlite3.Row
    return conexion


@app.route("/")
def index():
    conexion = obtener_conexion()
    tareas = conexion.execute("SELECT * FROM tarea").fetchall()
    conexion.close()
    return render_template("index.html",tareas=tareas,title="Todas las tareas")

@app.route("/pendientes")
def pendientes():
    conexion = obtener_conexion()
    tareas = conexion.execute("SELECT * FROM tarea WHERE done = 0").fetchall()
    conexion.close()
    return render_template("index.html",tareas=tareas,title="Tareas pendientes")

@app.route("/realizadas")
def realizadas():
    conexion = obtener_conexion()
    tareas = conexion.execute("SELECT * FROM tarea WHERE done = 1").fetchall()
    conexion.close()
    return render_template("index.html",tareas=tareas,title="Tareas realizadas")

@app.route("/add", methods=["POST"])
def add_tarea():
    titulo = request.form["title"]
    if titulo:
        conexion = obtener_conexion()
        conexion.execute("INSERT INTO tarea (title,done) VALUES (?,?)",(titulo,0))
        conexion.commit()
        conexion.close()
    return redirect(url_for("index"))

@app.route("/hecha/<int:tarea_id>")
def marcar_hecha(tarea_id):
    conexion = obtener_conexion()
    conexion.execute("UPDATE tarea SET done = 1 WHERE id = ?",(tarea_id,))
    conexion.commit()
    conexion.close()
    return redirect(request.referrer or url_for("index"))


@app.route("/eliminar/<int:tarea_id>")
def eliminar_tarea(tarea_id):
    conexion = obtener_conexion()
    conexion.execute("DELETE FROM tarea WHERE id = ?",(tarea_id,))
    conexion.commit()
    conexion.close()
    return redirect(request.referrer or url_for("index"))











# 127.0.0.1:5000/todas_tareas
# misitio.com/api/tareas
# misitio.com/api/pendientes
# misitio.com/api/realizadas

@app.route("/api/tareas")
def api_tareas():
    conexion = obtener_conexion()
    tareas = conexion.execute("SELECT * FROM tarea").fetchall()
    conexion.close()
    return jsonify([ dict(tarea) for  tarea in tareas])

@app.route("/api/pendientes")
def api_pendientes():
    conexion = obtener_conexion()
    tareas = conexion.execute("SELECT * FROM tarea WHERE done = 0").fetchall()
    conexion.close()
    return jsonify([ dict(tarea) for  tarea in tareas])

@app.route("/api/realizadas")
def api_realizadas():
    conexion = obtener_conexion()
    tareas = conexion.execute("SELECT * FROM tarea WHERE done = 1").fetchall()
    conexion.close()
    return jsonify([ dict(tarea) for  tarea in tareas])



if __name__ == "__main__":
    app.run(debug=False)