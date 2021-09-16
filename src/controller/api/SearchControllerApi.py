from flask import render_template, redirect, url_for, request, flash,abort,jsonify,json,Response
from repository.SearchRepository import SearchRepository
from utility.dataConversion import relations2Table

def index():
    return jsonify(SearchRepository.getAllSearch())

def store():
    data = request.get_json()

    SearchRepository.saveSearch(data)
    
    return Response(status=201, mimetype='application/json')

def delete(id):
    SearchRepository.deleteSearch(id)
    return Response(status=200, mimetype='application/json')

def table():

    data = request.get_json()

    isGeneTarget = data.get('isGeneTarget')
    source = data.get('source')
    target = data.get('target')
    databases = data.get('databases')
        
    # Query
    relations = SearchRepository.findRelations(source, target, isGeneTarget, databases)

    # Conversion
    data = relations2Table(relations, isGeneTarget)

    return jsonify(data)    
