from flask import Flask, render_template,redirect,url_for,request,flash
from flask_sqlalchemy import SQLAlchemy

# ORM için gerekli olan köprü yapısı kurulumu
app = Flask(__name__)
app.secret_key = "ilhan"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/ILHAN OLCER/Desktop/TodoApp/todo.db'
db = SQLAlchemy(app)

@app.route("/")
def index():
    todos = Todo.query.all() # todoların her bir özelliği bir sözlük yapısı şeklinde liste ile dönecek.

    return render_template("index.html",todos = todos)

# dinamik url adresi oluşturulur.
@app.route("/complete/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    """if todo.complete == True:
        todo.complete = False
    else:
        todo.complete = True"""
    
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

# Todo Ekleme
@app.route("/add",methods = ["POST"])
def addTodo():
    title = request.form.get("title")
    if title != "":
        newTodo = Todo (title = title, complete = False) # Todo classa ait newTodo object oluşturuldu.
        db.session.add(newTodo) # oluşturulan object (newTodo) veri tabanına eklendi.
        db.session.commit() # veritabanında değişikliği yapıldığı için
        return redirect(url_for("index"))
    else:
        flash ("Lütfen bir To Do Giriniz !","warning")
        return redirect(url_for("index"))
    

# silme
@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))
    
# tablo için class oluşturma
class Todo (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

if __name__ == "__main__":
    db.create_all() # olusturulan tüm classlar, veri tabanına bir tablo olarak eklenir.
    app.run(debug= True)