from dotenv import load_dotenv
import sys
import os
import ncbi
import uniprot
import ensembl
from dbhelper import db_connect, create_db_info, create_relation_info

load_dotenv()

# Check for command line arguments
if len(sys.argv) == 1:
    FILE_PATH = '../data/rna22/mus_musculus_ensembl65'
    RELATION = 'RNA22v2'
elif len(sys.argv) == 3:
    FILE_PATH = sys.argv[1]
    RELATION = sys.argv[2]
elif len(sys.argv) != 3 :
    print("Usage: python " + sys.argv[0] + " <path> <relation>")
    exit()

mirbase_aliases = '../data/mirbase/aliases.txt'

# Data folder
data_folder = FILE_PATH

# Species
species = {
    'mmu' : 'Mus musculus'
}

# Open a connection to the db
session = db_connect()

# Create the DB_info node
create_db_info('RNA22', 'https://cm.jefferson.edu/rna22/')

# RNA22v2 data source link
source_db_link = 'https://cm.jefferson.edu/data-tools-downloads/rna22-full-sets-of-predictions/'

# Min and max value of the score
min_value = 0
max_value = 0

counterFile=0
# Process files
for file in os.listdir(data_folder):
    counterFile=counterFile+1
    # Species prefix
    species_prefix = file.split('_')[0]

    print(os.path.join(data_folder, file))
    with open(os.path.join(data_folder, file), 'r',errors='ignore') as f:
        counterLine=0
        # Process data in files
        for line in f:
            counterLine=counterLine+1
            if "\x00" in line:
                os.remove(os.path.join(data_folder, file))
                continue
            # Select the data we need
            data = line.split()
         
            params = {
                'miRNA'     : data[0],
                'miRNAname' : data[0].replace('_','-'),
                'target'    : data[1].split('_')[0],
                'relation'  : RELATION,
                'score'     : data[5]
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
                            "WHERE m.name =~ ('(?i)'+$miRNAname)"
                           "RETURN m", params)
            try:
                r.peek()
            except:

                found = False

                # Try to find the microRNA in the mirbase aliases
                with open(mirbase_aliases, 'r') as f:
                    for line in f:
                        if params['miRNAname'] + ';' in line:
                            r = session.run("MATCH (m:microRNA "
                                            "{accession:'%s'}) RETURN m" %
                                            line.split()[0])
                            try:
                                params['miRNAname'] = r.single()['m']['name']
                            except:
                                print("microRNA found in mirbase"
                                      "aliases but not in DB: %s ...adding it" %
                                      params['miRNAname'])

                                miRNA = {
                                    'name'         : params['miRNAname'],
                                    'species'      : species[species_prefix],
                                    'accession'    : line.split()[0]
                                }

                                session.run("CREATE (m:microRNA {"
                                                "name: $name,"
                                                "species: $species,"
                                                "accession: $accession,"
                                                "mirbase_link: $accession})",
                                            miRNA)

                            found = True

                if not found:
                    print("Cannot find microRNA node: %s" %
                          params['miRNAname'])
                    continue

            # Check if we can find a matching target using the Ensembl
            r = session.run("MATCH (t:Target {ens_code:$target}) RETURN t",
                            params)
            try:
                r.peek()
            except:
                gene = None

                # Try to find the new gene info on NCBI
                gene = ncbi.get_gene_by_ens(params['target'])

                # Try to find the Ensembl on UniProt
                if gene is None:
                    gene = uniprot.get_gene_by_ens(params['target'])

                # Try to find the Ensembl on ensembl.org
                if gene is None:
                    gene = ensembl.get_gene_by_id(params['target'])
                    if gene is not None and gene['species'] == '':
                        gene['species'] = species[species_prefix]

                if gene is None:
                    print("Cannot find Target node with Ensembl: %s" %
                          params['target'])
                    continue

                print("Inserting new gene:", gene)
                session.run("MERGE (t:Target {"
                              "name:$name,"
                              "species:$species,"
                              "geneid:$id,"
                              "ens_code:$embl,"
                              "ncbi_link:$id"
                            "})", gene)

            # Execute the query
            r = session.run("MATCH"
                              "(m:microRNA),"
                              "(t:Target)"
                            "WHERE m.name =~ ('(?i)'+$miRNAname)"
                            "MERGE (m)-[r:RNA22 "
                              "{name:$relation,"
                              "score:$score,"
                              "source_microrna:$miRNA,"
                              "source_target:$target}]->(t)",
                            params).consume()

            # Check if the relationship was created
            if r.counters.contains_updates:
                print(params)

# Create the Relation_general_info node
create_relation_info(RELATION, source_db_link, min_value, max_value, 0)

# Close the db session
session.close()
