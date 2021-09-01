from DataTable import DataTable
from flask import Flask
from neo4j import GraphDatabase
import os
import time
from Relation import Relation
from flask import render_template
from flask import request

app = Flask(__name__)

driver = GraphDatabase.driver(
        'neo4j://localhost:7687',
        auth=('neo4j','test')
)

@app.route('/')
def results():
    return render_template('index.html') 

@app.route('/query', methods=['POST'])
def query():

    #retrieve params
    genes = request.form['genes']
    mrnas = request.form['mrnas']
    targetName = request.form['targetName']

    #sanitize

    isGeneResearch = targetName == 'gene'
    genes = genes.split(',')
    mrnas = mrnas.split(',')
    rankParam = 0

    relations = findRelations(mrnas, genes, rankParam)
    data = createDataTable(relations, isGeneResearch)

    if(isGeneResearch):
        source = genes
        target = mrnas
    else:
        source = mrnas
        target = genes



    return render_template('results.html', source = source, target = target, data = data) 


def createDataTable(relations, isGeneResearch):

    data = {}
    for row in relations:
        mRNA = row['p'][0]['name']
        database = row['p'][1]
        geneId = row['p'][2]['geneid']

        if(isGeneResearch):
            source = geneId
            target = mRNA
        else:
            source = mRNA
            target = geneId

        if( not source in data):
            #new gene
            data[source] = {}
            data[source][target] = {}
            data[source][target][database] = True
        else:
            #gene already exists
            if( not target in data[source]):
                data[source][target] = {}
                
            data[source][target][database] = True

    return data
    

def findRelations(source, target, rank):

    queryString = queryBuilding(source,target)
    print(queryString)
    
    res = None
    with driver.session() as session:
        res = session.run(queryString).data()
    
    return res

def createTable(data):

    for element in data:
        print(data[element])
    return "<h1>ok</h1>"

def queryBuilding(source, target):

    sourceList = source[:]
    targetList = target[:]

    query = 'MATCH p=(m:microRNA)-[]->(t:Target) WHERE ('

    #Source 
    query += f"m.name='{sourceList[0]}'"
    sourceList.pop(0)

    for mRNA in sourceList:
        query += f" OR m.name='{mRNA}'" 

    #Target
    query += f") AND (t.geneid='{targetList[0]}'"
    targetList.pop(0)

    for target in targetList:
        query += f" OR t.geneid='{target}'" 

    query += ') RETURN p'

    return query