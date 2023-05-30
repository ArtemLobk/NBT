from flask import Flask, render_template, redirect, request, send_file
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///file_storage.db'
db = SQLAlchemy(app)


class File(db.Model):
    name = db.Column(db.String(255), primary_key=True)
    filename = db.Column(db.String(255))
    path = db.Column(db.String(255))


with app.app_context():
    db.create_all()


@app.route('/delete/<name>', methods=['POST'])
def delete_file(name):
    file = File.query.get(name)
    if file:
        file_path = file.path
        os.remove(file_path)

        db.session.delete(file)
        db.session.commit()

    return redirect("/")


@app.route('/download/<name>', methods=['GET'])
def download_file(name):
    file = File.query.get(name)
    if file:
        file_path = file.path
        return send_file(file_path, as_attachment=True)

    return redirect("/")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST': 
        if 'delete' in request.form:
            name = request.form['delete']
            return delete_file(name)

        nbt_file = request.files['nbt_file']
        file_path = f"uploads/{nbt_file.filename}"
        nbt_file.save(file_path)

        new_file = File(name=nbt_file.filename, filename=nbt_file.filename, path=file_path)
        db.session.add(new_file)
        db.session.commit()

        return redirect("/")

    files = File.query.all()
    return render_template('index.html', files=files)


if __name__ == '__main__':
    app.run(debug=True)
