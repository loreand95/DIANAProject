def relations2Table(relations, isGeneResearch):

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
            data[source][target][database] = 1
        else:
            #gene already exists
            if( not target in data[source]):
                data[source][target] = {}

            if(not database in data[source][target]):
                data[source][target][database] = 0
            
            data[source][target][database] = data[source][target][database]+1

    return data