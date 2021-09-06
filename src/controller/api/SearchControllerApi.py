from flask import render_template, redirect, url_for, request, flash,abort,jsonify,json,Response
from repository.SearchRepository import SearchRepository

def index():
    return jsonify(SearchRepository.getAllSearch())

def store():
    data = request.get_json()

    SearchRepository.saveSearch(data)
    
    return Response(status=201, mimetype='application/json')