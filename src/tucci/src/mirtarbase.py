from dotenv import load_dotenv
import sys
import csv
from dbhelper import db_connect, create_db_info, create_relation_info
from ncbi import get_gene_by_id

load_dotenv()

# Check for command line arguments
if len(sys.argv) == 1:
    FILE_PATH = '../data/mirtarbase/mmu_MTI.csv'
    SPECIES = 'mmu'
elif len(sys.argv) == 3:
    FILE_PATH = sys.argv[1]
    SPECIES = sys.argv[2]
elif len(sys.argv) != 3 :
    print("Usage: python " + sys.argv[0] + " <path> <species>")
    exit()

# Data file
data_file = FILE_PATH

# Species prefix
species = SPECIES

# Open a connection to the db
session = db_connect()

# Create the DB_info node
create_db_info('miRTarBase', 'http://mirtarbase.mbc.nctu.edu.tw/')

# miRTarBase data source link
source_db_link = 'http://mirtarbase.mbc.nctu.edu.tw/cache/download/6.1/mmu_MTI.xls'

# Min and max value of the score
min_value = 0
max_value = 0

# Process data
with open(data_file, newline='') as csvfile:

    # Skip the first line containing CSV headers
    csvfile.readline()

    # Initialize the csv reader
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:

        # Avoid malformed lines


        # Avoid data from other species
        if not row[1].startswith(species):
            continue

        # Select the data we need
        params = {
            'miRNA'    : row[1],
            'target'   : row[3],
            'geneID'   : row[4],
            'relation' : 'miRTarBase',
            'score'    : row[8]
        }

        # Save min and max value
        try:
            score = float(params['score'])
            if score < min_value: min_value = score
            if score > max_value: max_value = score
        except:
            pass

        # Check if we can find a matching microRNA
        r = session.run("MATCH (m:microRNA)"
                        "WHERE m.name =~ ('(?i)'+$miRNA)"
                       "RETURN m", params)
        try:
            r.peek()
        except exceptions.ResultError:
            print("Cannot find microRNA node: %s" % params['miRNA'])
            continue

        # Check if we can find a matching target using the geneID
        r = session.run("MATCH (t:Target {geneid:$geneID}) RETURN t", params)
        try:
            r.peek()
        except exceptions.ResultError:

            # Try to find the new gene info on NCBI
            gene = get_gene_by_id(params['geneID'])
            if gene is None:
                print("Cannot find Target node with geneID: %s" %
                      params['geneID'])
                continue
            session.run("MERGE (t:Target {"
                          "name:$name,"
                          "species: $species,"
                          "geneid:$id,"
                          "ens_code:$embl,"
                          "ncbi_link:$id"
                        "})", gene)

        # Execute the query
        r = session.run("MATCH"
                          "(m:microRNA),"
                          "(t:Target {geneid:$geneID})"
                        "WHERE m.name =~ ('(?i)'+$miRNA)"
                        "MERGE (m)-[r:miRTarBase "
                          "{name:$relation,"
                          "score:$score,"
                          "source_microrna:$miRNA,"
                          "source_target:$target}]->(t)",
                        params).consume()

        # Check if the relationship was created
        if not r.counters.contains_updates:
            print("Duplicate entry: %s" % r.parameters)
        else:
            print(params)

# Create the Relation_general_info node
create_relation_info('miRTarBase', source_db_link, min_value, max_value, 0)

# Close the db session
session.close()
