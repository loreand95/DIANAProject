from flask import Flask, redirect, url_for
from routes.search_bp import search_bp
from routes.search_full_bp import search_full_bp
from routes.api.api_search_bp import api_search_bp

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.register_blueprint(search_bp, url_prefix='/search')
app.register_blueprint(search_full_bp, url_prefix='/search/full')

### API ###
app.register_blueprint(api_search_bp, url_prefix='/api/search')

@app.route('/')
def index():
    return redirect(url_for('search_bp.index'))