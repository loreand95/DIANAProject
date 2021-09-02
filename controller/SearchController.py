from flask import render_template, redirect, url_for, request, abort
from repository.SearchRepository import SearchRepository
from flask import request
from utility.data_table import relations2DataTable

def index():
    return render_template('search/form_page.html') 

def search():

    #Retrieve params
    
    genes = request.form.get('genes')
    mrnas = request.form.get('mrnas')

    mirtarbase = request.form.get("mirtarbase")
    rna22 = request.form.get('rna22')
    targetscan = request.form.get('targetscan')
    pictar = request.form.get('pictar')

    targetName = request.form.get('targetName')

    #Sanitize and check

    isGeneResearch = targetName == 'gene'
    genes = genes.split(',')
    mrnas = mrnas.split(',')
    rankParam = 0

    databases = []
    if(mirtarbase):
        databases.append('miRTarBase')
    
    if(rna22):
        databases.append('TargetScan')
    
    if(targetscan):
        databases.append('RNA22')
    
    if(pictar):
        databases.append('PicTar')
    
    if(isGeneResearch):
        source = genes
        target = mrnas
    else:
        source = mrnas
        target = genes

    # Query
    relations = SearchRepository.findRelations(mrnas, genes, databases)

    # Conversion
    data = relations2DataTable(relations, isGeneResearch)

    return render_template('search/results_page.html', source = source, target = target, data = data) 
