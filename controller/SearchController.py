from flask import render_template, redirect, url_for, request, flash,abort
from repository.SearchRepository import SearchRepository
from flask import request
from utility.data_table import relations2DataTable
import re

def index():
    return render_template('search/form_page.html') 

def search():
    isValidForm = True
    #Retrieve params
    
    genes = request.form.get('genes')
    mrnas = request.form.get('mrnas')

    mirtarbase = request.form.get("mirtarbase")
    rna22 = request.form.get('rna22')
    targetscan = request.form.get('targetscan')
    pictar = request.form.get('pictar')

    targetName = request.form.get('targetName')

    #Sanitize and check
    genes = _sanitizeGenes(genes,isValidForm)
    mrnas = _sanitizeMrnas(mrnas,isValidForm)

    databases = _sanitizeDatabases(mirtarbase,rna22,targetscan,pictar,isValidForm)
    
    isGeneResearch = targetName == 'gene'
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

def _sanitizeGenes(genes,isValidForm):
    genes = genes.replace("\n","")
    genes = genes.replace("\r","")
    genes = genes.replace(" ","")
    genes = re.match("(\d+)(,\s*\d+)*",genes)

    if(not genes):
        isValidForm = False
        flash('Invalid genes', 'error')
        return None

    return genes.group().split(',')

def _sanitizeMrnas(mrnas,isValidForm):
    mrnas = mrnas.replace("\n","")
    mrnas = mrnas.replace("\r","")
    mrnas = mrnas.replace(" ","")
    mrnas = re.match("(mmu-miR-[A-Za-z0-9_-]+)(\,(mmu-miR-[A-Za-z0-9_-]+))*",mrnas)

    if(not mrnas):
        isValidForm = False
        flash('Invalid mRNAs', 'error')
        return None

    return mrnas.group().split(',')

def _sanitizeDatabases(mirtarbase,rna22,targetscan,pictar,isValidForm):
    databases = []
    if(mirtarbase):
        databases.append('miRTarBase')
    
    if(rna22):
        databases.append('RNA22')
    
    if(targetscan):
        databases.append('TargetScan')
    
    if(pictar):
        databases.append('PicTar')

    if(not databases):
        isValidForm = False
        flash('Select at least one database', 'error')

    return databases
