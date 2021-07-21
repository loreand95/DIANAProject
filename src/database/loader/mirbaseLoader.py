from genericpath import exists
import sys
import re
import logging
from database.MirbaseRepository import MirbaseRepository
from decouple import config
import os.path
from model.Mirbase import Mirbase

DEFAULT_PATH = config('ROOT_PATH') +'/mirbase/miRNA.dat'

def mirbaseLoader(filePath=DEFAULT_PATH, species='Mus musculus', prefixSpecies='mmu'):
    repository = MirbaseRepository()

    # Check if file exist
    if not os.path.isfile(filePath):
        logging.exception("The file "+filePath+" doesn't exist")
        return

    # Process the data file
    with open(filePath, 'r') as f:

        # This dictionary will contain the parsed data of a single microRNA
        mirbase = Mirbase()

        in_data_block = False

        previous_line = ''

        for line in f:

            # New microRNA found
            if line.startswith('ID') and line.split()[1].startswith(prefixSpecies):

                in_data_block = True

                # Save the ID of the microRNA in the data dictionary
                mirbase.setId(line.split()[1])
                mirbase.setSpecies(species)

                # Check if the previous line contains an accession
                # This is only the case for dead mirbase entries
                if previous_line.startswith('AC'):
                    mirbase.setAccession(line.split()[1])

                    # Create a new microRNA node
                    repository.store(mirbase)

            elif in_data_block:

                # New accession found
                if line.startswith('AC'):

                    mirbase.setAccession(line.split()[1][:-1])

                    # Create a new microRNA node
                    repository.store(mirbase)

                # New product accession found
                if '/accession=' in line:

                    # Add the accession to the data dictionary
                    mirbase.setAccession(re.search(r'/accession="([^"]+)"',
                                            line).group(1))

                # New product found
                elif '/product=' in line:

                    # Add the product to the data dictionary
                    mirbase.setId(re.search(r'/product="([^"]+)"',
                                            line).group(1))

                    # Create a new microRNA node
                    repository.store(mirbase)

                # End of data block
                elif line.startswith('//'):
                    in_data_block = False

            # Update the previous_line variable
            previous_line = line