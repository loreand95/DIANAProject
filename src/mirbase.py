import sys
import re
from dbhelper import db_connect

"""
Store  a microRNA in the db if not already there.
Return True if the new node is created.

Parameters
----------
miRNA : dict
    microRNA properties for the new node creation.
"""
def store_miRNA(miRNA):

    # Check if the microRNA is already in the db
    r = session.run("MATCH (m:microRNA) WHERE m.name=$id RETURN m",id=miRNA.get('id'))

    res = r.single()

    if res == None:
        # Not in db... insert it
        session.run("CREATE (m:microRNA {"
                        "name: $id,"
                        "accession: $accession,"
                        "species: $species,"
                        "mirbase_link: $accession})", miRNA)
        return True
    return False

# Check command line arguments
if len(sys.argv) < 4:
    print("Usage: %s <mirbase .dat file> <species name, ex. 'Mus musculus'>"
          " <species prefix, ex. mmu>" % sys.argv[0])
    exit()

# Connect to the db
session = db_connect()


# Process the data file
with open(sys.argv[1], 'r') as f:

    # This dictionary will contain the parsed data of a single microRNA
    data = {}

    in_data_block = False

    previous_line = ''

    for line in f:

        # New microRNA found
        if line.startswith('ID') and line.split()[1].startswith(sys.argv[3]):

            in_data_block = True

            # Save the ID of the microRNA in the data dictionary
            data = {'id' : line.split()[1], 'species' : sys.argv[2]}

            # Check if the previous line contains an accession
            # This is only the case for dead mirbase entries
            if previous_line.startswith('AC'):
                data['accession'] = line.split()[1]

                # Create a new microRNA node
                if store_miRNA(data):
                    continue
                print("Duplicate entry: %s." % data['id'])

        elif in_data_block:

            # New accession found
            if line.startswith('AC'):

                data['accession'] = line.split()[1][:-1]

                # Create a new microRNA node
                if store_miRNA(data):
                    continue
                print("Duplicate entry: %s." % data['id'])

            # New product accession found
            if '/accession=' in line:

                # Add the accession to the data dictionary
                data['accession'] = re.search(r'/accession="([^"]+)"',
                                        line).group(1)

            # New product found
            elif '/product=' in line:

                # Add the product to the data dictionary
                data['id'] = re.search(r'/product="([^"]+)"',
                                        line).group(1)

                # Create a new microRNA node
                if store_miRNA(data):
                    continue
                print("Duplicate entry: %s." % data['id'])

            # End of data block
            elif line.startswith('//'):
                in_data_block = False

        # Update the previous_line variable
        previous_line = line

# Close the session
session.close()
