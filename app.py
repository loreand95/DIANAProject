from flask import Flask, redirect, url_for
from routes.search_bp import search_bp
from flask import render_template

app = Flask(__name__)

app.register_blueprint(search_bp, url_prefix='/search')

@app.route('/')
def index():
    return redirect(url_for('search_bp.index'))