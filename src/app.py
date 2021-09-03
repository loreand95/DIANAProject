from flask import Flask, redirect, url_for
from routes.search_bp import search_bp

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.register_blueprint(search_bp, url_prefix='/search')

@app.route('/')
def index():
    return redirect(url_for('search_bp.index'))