from flask import render_template, redirect, url_for, request, abort
from repository.SearchRepository import SearchRepository
from flask import request
from utility.data_table import relations2DataTable

def index():
    return render_template('search/form_page.html') 

def search():

    #retrieve params
    genes = request.form['genes']
    mrnas = request.form['mrnas']
    targetName = request.form['targetName']

    #sanitize

    isGeneResearch = targetName == 'gene'
    genes = genes.split(',')
    mrnas = mrnas.split(',')
    rankParam = 0

    relations = SearchRepository.findRelations(mrnas, genes, rankParam)
    data = relations2DataTable(relations, isGeneResearch)

    if(isGeneResearch):
        source = genes
        target = mrnas
    else:
        source = mrnas
        target = genes

    return render_template('search/results_page.html', source = source, target = target, data = data) 
