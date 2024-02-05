from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


# Create a new user
@app.route('/create-user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        user = User(data['name'], data['email'])
        db.session.add(user)
        db.session.commit()
        return jsonify(user.json()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Get all users
@app.route('/get-users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([user.json() for user in users]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Get user by id
@app.route('/get-user/<id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.get(id)
        return jsonify(user.json()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Delete user
@app.route('/delete-user/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify(user.json()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run()
    db.create_all()
