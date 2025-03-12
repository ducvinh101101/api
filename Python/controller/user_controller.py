from app import app
from model.user_model import user_model
from flask import request
obj = user_model()
@app.route('/user/signup')
def signup():
    return obj.user_login()
@app.route('/user/signin', methods=['POST'])
def signin():
    return obj.user_signin(request.form)
@app.route('/user/update', methods=['PUT'])
def update():
    return obj.user_update(request.form)
@app.route('/user/delete/<string:id>', methods=['DELETE'])
def delete(id):
    return obj.user_delete(id)

