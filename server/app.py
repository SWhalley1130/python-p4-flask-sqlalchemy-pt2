#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet, Owner

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    response=make_response(
        '<h1>Welcome to the pet/owner directory!</h1>', 
        200
    )
    return response

@app.route('/pets/<int:id>')
def pets_by_id(id):
    pet=Pet.query.filter(Pet.id==id).first()

    if not pet:
        response_body='<h1>404 Pet not found</h1>'
        response=make_response(response_body, 404)
        return response

    response_body=f'''<h1>Information for {pet.name}</h1>
                    <h2>Pet Species is {pet.species}</h2>
                    <h2>Pet Owner is {pet.owner.name}<h2>'''
    response=make_response(response_body,200)
    return response

@app.route('/owner/<int:id>')
def owner_by_id(id):
    owner=Owner.query.filter(Owner.id==id).first()

    if not owner:
        rb='<h1>404 Owner not found</h1>'
        r=make_response(rb,404)
        return r
    
    rb=f'<h1>Information for {owner.name}</h1>'
    pets=[pet for pet in owner.pets]
    if not pets:
        rb+=f'<h2>Has no pets at this time.'
    else:
        for pet in pets:
            rb+=f'<h2>Has pet {pet.species} named {pet.name}.</h2>'
    r=make_response(rb, 200)
    return r


if __name__ == '__main__':
    app.run(port=5555, debug=True)
