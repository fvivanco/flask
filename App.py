from flask import Flask, render_template, request,flash, redirect,url_for#sirve para redireccionar
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder="template")

#Mysql connection
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_DB"] = "flaskcontact"
mysql = MySQL(app)

#inicializar una sesion(son datos que guardan nuestra aplicacion de servidor para luegop poder reutilizarlos)
#settings
app.secret_key = "mysecretkey"#guardamos dentro de la memoria de la aplicacion
@app.route("/")
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts")
    data = cur.fetchall()
#    print(data)
    return render_template("index.html", contacts = data)#creo la variable contacts que le pasará al index.html la data

@app.route("/addcontact", methods = ["POST"])
def agregar_contacto():
    if request.method == "POST":
        fullname =request.form["fullname"]
        phone =request.form["phone"]
        email =request.form["email"]
        cur = mysql.connection.cursor() #obtenemos la conexion
        cur.execute("INSERT INTO contacts (fullname, phone, email) VALUES (%s,%s,%s)", (fullname, phone, email))#escribimos la consulta
        mysql.connection.commit()#ejecutamos la consulta
        flash("Contacto agregado")
        return redirect(url_for("Index"))

@app.route("/edit/<id>")
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("Select *FROM contacts WHERE id = {0}".format(id))
    data = cur.fetchall()
    return render_template("edit-contact.html",contact = data[0])

@app.route("/update/<id>", methods=["POST"])
def update_contact(id):
    if request.method=="POST":
        fullname = request.form["fullname"]
        phone = request.form["phone"]
        email = request.form["email"]
        a=request.form
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE contacts
        SET fullname = %s,
        email = %s,
        phone = %s
        Where id = %s
    """,(fullname,email,phone,id))
    mysql.connection.commit()
#    print("hola",a)
    flash("CONTACTO ACTUALIZADO SATISFACTORIAMENTE")
    return redirect(url_for("Index"))

@app.route("/delete/<string:id>")#recibe un parametro string de tipo id
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contacts WHERE id ={0}".format(id))
    mysql.connection.commit()
    print(id)
    flash("Contacto removido satisfactoriamente")
    return redirect(url_for("Index"))

if __name__ == "__main__":
    app.run(port = 3000, debug=True)