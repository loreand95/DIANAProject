from flask import render_template, redirect, url_for, request, flash,abort,jsonify,json,Response
from repository.SearchRepository import SearchRepository
from utility.data_table import relations2DataTable

def index():
    return jsonify(SearchRepository.getAllSearch())

def store():
    data = request.get_json()

    SearchRepository.saveSearch(data)
    
    return Response(status=201, mimetype='application/json')

def table():

    data = request.get_json()

    isGeneResearch = data['isGeneResearch']
    mrnas = data['mrnas']
    genes = data['genes']
    databases = data['databases']
        
    # Query
    relations = SearchRepository.findRelations(mrnas, genes, databases)

    # Conversion
    data = relations2DataTable(relations, isGeneResearch)

    return jsonify(data)    
