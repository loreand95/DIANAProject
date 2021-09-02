from repository.Neo4jConnection import Neo4jConnection

class SearchRepository:

    def findRelations(source, target, rank):

        queryString = SearchRepository.__queryBuilding(source,target)
        print(queryString)
        
        res = None
        with Neo4jConnection.driver.session() as session:
            res = session.run(queryString).data()
        
        return res

    def __queryBuilding(source, target):

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