from flask import Flask
from app.user import user_bp

app = Flask(__name__)

# Register Blueprint
app.register_blueprint(user_bp, url_prefix='/user')

@app.route('/')
def home():
    return "user control"

if __name__ == '__main__':
    app.run(debug=True, port=8080)
