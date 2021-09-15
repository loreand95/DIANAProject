from flask import render_template, redirect, url_for, request, flash,abort,json
from neo4j.work.simple import Query
from repository.SearchRepository import SearchRepository
from flask import request
from utility.data_table import relations2DataTable
import re

def index():
    return render_template('search/form_page.html') 

def search():
    error = { 'isValidForm' : True}
    #Retrieve params
    
    source = request.form.get('source')

    mirtarbase = request.form.get("mirtarbase")
    rna22 = request.form.get('rna22')
    targetscan = request.form.get('targetscan')
    pictar = request.form.get('pictar')

    targetName = request.form.get('targetName')

    isGeneTarget = targetName == 'genes'

    #Sanitize and check
    if(isGeneTarget):
        source = _sanitizeMrnas(source,error)
    else:
        source = _sanitizeGenes(source,error)

    databases = _sanitizeDatabases(mirtarbase,rna22,targetscan,pictar,error)
    
    if(not error['isValidForm']):
        return redirect(url_for('search_bp.index'))

    query = {
        "source": source,
        "databases":databases,
        "isGeneTarget":isGeneTarget
    }

    return render_template('search/results_page.html', query = query) 

def _sanitizeGenes(genes,error):
    genes = genes.replace("\n","")
    genes = genes.replace("\r","")
    genes = genes.replace(" ","")
    genes = re.match("(\d+)(,\s*\d+)*",genes)

    if(not genes):
        error['isValidForm'] = False
        flash('Invalid genes', 'error')
        return None

    return genes.group().split(',')

def _sanitizeMrnas(mrnas,error):
    mrnas = mrnas.replace("\n","")
    mrnas = mrnas.replace("\r","")
    mrnas = mrnas.replace(" ","")
    mrnas = re.match("(mmu-[A-Za-z0-9_-]+)(\,(mmu-[A-Za-z0-9_-]+))*",mrnas)

    if(not mrnas):
        error['isValidForm'] = False
        flash('Invalid mRNAs', 'error')
        return None

    return mrnas.group().split(',')

def _sanitizeDatabases(mirtarbase,rna22,targetscan,pictar,error):
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
        error['isValidForm'] = False
        flash('Select at least one database', 'error')

    return databases
