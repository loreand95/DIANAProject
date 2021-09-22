from dotenv import load_dotenv
import sys
import os
import csv
import re
from pathlib import Path
from dbhelper import db_connect, create_db_info, create_relation_info
from ncbi import get_geneid_by_refseq, get_gene_by_id
import time

load_dotenv()

if len(sys.argv) == 1:
    FILE_PATH = '../data/pictar/picTarMiRNAChicken_mm7.bed'
    RELATION = 'PicTar13'
elif len(sys.argv) == 3:
    FILE_PATH = sys.argv[1]
    RELATION = sys.argv[2]
elif len(sys.argv) != 3 :
    print("Usage: python " + sys.argv[0] + " <path> <relation>")
    exit()

def miRNA2accession(miRNA):
    """
    Converts a microRNA to the corresponding accession code.

    Parameters
    ----------
    miRNA : str
        microRNA name
    """

    # EDITED : File path, and create file
    res = session.run("MATCH (m:microRNA) WHERE m.name=$id RETURN m.accession as accession",id=miRNA)

    for result in res:
       return result[0]
    return None


# Open a connection to the db
session = db_connect()

# Create the DB_info node
create_db_info('PicTar', 'http://pictar.mdc-berlin.de/')

# PicTar data sources link
source_db_link = 'http://genome.ucsc.edu/cgi-bin/hgTables'

# Min and max value of the score
min_value = 0
max_value = 0

file = open(FILE_PATH)
totLine = len(file.readlines())

with open(FILE_PATH, 'r') as bed:
	# Parse data from bed
    bed = csv.reader(bed, delimiter='\t')

    next(bed) # EDITED - Skip header

    for row in bed:
        start_time = time.time()
        t_m = row[4].split(':') # EDITED : row[3]

		# Select the data we need
        params = {
            'miRNA'     : t_m[1],
            'target'    : t_m[0],
            'accession' : miRNA2accession(t_m[1]),
            'geneID'    : get_geneid_by_refseq(t_m[0]),
            'relation'  : RELATION,
            'score'     : row[5]
        }

        # Save min and max value
        try:
            score = float(params['score'])
            if score < min_value: min_value = score
            if score > max_value: max_value = score
        except:
            pass
        # continue # TO ASK - Remove?

        if params['geneID'] is None:
            continue

        
        # Check if we can find a matching microRNA
        r = session.run("MATCH (m:microRNA {accession:$accession}) RETURN m", params) # EDITED {accension}
       
        try:
            r.peek()
        except exceptions.ResultError:
            print("Cannot find microRNA node: %s %s" %
                  (params['miRNA'], params['accession']))
            continue

        # Check if we can find a matching target using the geneID
        r = session.run("MATCH (t:Target {geneid:$geneID}) RETURN t", params) # EDITED {geneID}
        try:
            r.peek()
        except exceptions.ResultError:
            print("Cannot find Target node with geneID: %s and RefSeq: %s" %
                  (params['geneID'], t_m[0]))

            # Try to find the new gene info on NCBI
            gene = get_gene_by_id(params['geneID'])
            if gene is None:
                continue
            session.run("MERGE (t:Target {"
                          "name:$name,"
                          "species:$species,"
                          "geneid:$id,"
                          "ens_code:$embl,"
                          "ncbi_link:$id"
                        "})", gene) # EDITED 

        # Execute the query
        r = session.run("MATCH"
                            "(m:microRNA {accession:$accession}),"
                            "(t:Target {geneid:$geneID})"
                            "MERGE (m)-[r:PicTar "
                                "{name:$relation,"
                                "score:$score,"
                                "source_microrna:$miRNA,"
                                "source_target:$geneID}]->(t)",
                        params).consume() # EDITED 

        avanz = bed.line_num*100/totLine
        end_time = time.time() - start_time



# Create the Relation_general_info node
create_relation_info(RELATION, source_db_link, min_value, max_value, 0)

# Close the session
session.close()
