from flask import Flask
from flask import request
from flask import jsonify

import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore

from hashlib import sha256

def ash256(a):
    return sha256(a.encode()).hexdigest()

cred = credentials.Certificate('creds.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
 

app = Flask(__name__)

@app.route('/api/v1/<user>/<passw>', methods = ['POST', 'PATCH'])
def login(user, passw):
    passHash = ash256(passw)
    if request.method == 'POST':
        docs = db.collection('users').where('username', '==', user).stream()
        for doc in docs:
            if doc.to_dict()["passHash"] == passHash:
                return doc.to_dict()
    if request.method == 'PATCH':
        docs = db.collection(u'users').where('username', '==', user).stream()
        for doc in docs:
            temp = doc.to_dict()
            temp["passHash"] = passHash
            db.collection(u'users').document(doc.id).update(
                temp
            )
        return temp


if __name__ == "__main__":
    app.run(debug= True)