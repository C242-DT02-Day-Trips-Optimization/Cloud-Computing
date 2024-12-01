from flask import Flask
from app.auth import auth_bp

app = Flask(__name__)

# Register Blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/')
def home():
    return "Login/Register"

if __name__ == '__main__':
    app.run(debug=True)
