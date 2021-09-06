from repository.Neo4jConnection import Neo4jConnection
import uuid
from flask import json

FILE_PATH = 'src/static/saved-search.json'

class SearchRepository:

    def findRelations(source, target, databases):

        queryString = SearchRepository.__findRelationsQuery(source,target,databases)
        print(queryString)
        
        res = None
        with Neo4jConnection.driver.session() as session:
            res = session.run(queryString).data()
        
        return res

    def __findRelationsQuery(source, target,databases):

        sourceList = source[:]
        targetList = target[:]

        query = 'MATCH p=(m:microRNA)-[s]->(t:Target) WHERE ('

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

        if(databases):
            query += ") AND ("
            for count,database in enumerate(databases):
                query += f"type(s) = '{database}' "
                if(count+1 < len(databases)):
                    query += ' OR '

        query += ") RETURN p"

        return query

    def saveSearch(data):

        data['id'] = str(uuid.uuid4()) #Random ID

        #Write to file
        with open(FILE_PATH, 'r+') as f:

            searches = json.loads(f.read()) # File to JSON
        
            searches[data['id']] = data # Add ID

            #Overwrite
            f.seek(0)
            f.write(json.dumps(searches))
            f.truncate()

    def getAllSearch():
        
        #Write to file
        with open(FILE_PATH, 'r') as f:

            searches = json.loads(f.read()) # File to JSON
        
            return searches