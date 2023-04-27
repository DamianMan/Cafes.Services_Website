from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

import sqlite3 as sal
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap
import os
SECRET_KEY = os.urandom(32)




app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap(app)

db = SQLAlchemy(app)
#Conncetion to the database
connection = sal.connect('cafes.db', check_same_thread=False)
cur = connection.cursor()



#Form
class Form(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = StringField("📍Position on the Map", validators=[DataRequired(), URL()])
    img_url = StringField("Insert a Cafe Image", validators=[DataRequired(), URL()])
    location = StringField("Location", validators=[DataRequired()])
    has_sockets = SelectField("🔌 Power Sockets", choices=['❓',('✅'),('❌' )], validators=[DataRequired()])
    has_toilet = SelectField("🧻 Restroom", choices=['❓',('✅'),('❌' )], validators=[DataRequired()])
    has_wifi = SelectField('📶 WiFi', choices=['❓',('✅'),('❌' )], validators=[DataRequired()])
    can_take_calls = SelectField('🖥️📞 audio/call video', choices=[('❓'),('✅'),('❌' )], validators=[DataRequired()])
    seats = StringField("Seats", validators=[DataRequired()])
    coffe_price = StringField('Coffe Price', validators=[DataRequired()])
    submit = SubmitField('Add Cafe')



@app.route("/", methods=['GET'])
def home():
    all_data = cur.execute("SELECT * FROM 'cafe'")
    list_data = all_data.fetchall()
    print(list_data)




    return render_template("index.html", cafes=list_data)


@app.route("/show_cafe/<int:id>", methods=["GET", "POST"])
def show_cafe(id):
    all_data = cur.execute("SELECT * FROM 'cafe'")

    list_data = all_data.fetchall()


    return render_template('show_cafe.html', id=id, cafes=list_data)


@app.route("/add_cafe", methods=["GET", "POST"])
def add_cafe():
    all_data = cur.execute("SELECT * FROM 'cafe'")

    list_data = all_data.fetchall()

    form = Form()
    if request.method == "POST" and form.validate_on_submit():
        id = len(list_data) + 1
        name = form.name.data
        map_url = form.map_url.data
        img_url = form.img_url.data
        location = form.location.data
        has_sockets = form.has_sockets.data
        has_toilet = form.has_toilet.data
        has_wifi = form.has_wifi.data
        can_take_calls = form.can_take_calls.data
        seats = form.seats.data
        coffee_price = form.coffe_price.data

        sqlite_insert = """INSERT INTO 'cafe'(id,name,map_url,img_url,location,has_sockets,
                                                has_toilet,has_wifi,can_take_calls,seats,coffee_price)
                                                VALUES(?,?,?,?,?,?,?,?,?,?,?);"""
        data_tuple = (id, name, map_url, img_url, location, has_wifi,has_sockets,has_toilet, can_take_calls,
                      seats,coffee_price)
        cur.execute(sqlite_insert, data_tuple)
        connection.commit()
        return redirect(url_for('home'))


    return render_template("add_cafe.html", form=form)

@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    all_data = cur.execute("SELECT * FROM 'cafe'")

    list_data = all_data.fetchall()
    sql_delete_query = """DELETE FROM 'cafe' WHERE id = ?"""
    cur.execute(sql_delete_query, (id,))
    connection.commit()

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

