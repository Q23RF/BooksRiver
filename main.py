from flask import Flask, render_template, request, flash
import os

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/google_sign_in', methods=['POST'])
def google_sign_in():
    token = request.json['id_token']
    
    try:
        id_info = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_OAUTH2_CLIENT_ID
        )
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
    except ValueError:
        # Invalid token
        raise ValueError('Invalid token')
 
    print('登入成功')
    return jsonify({}), 200


app.run(host='0.0.0.0', port=81)
