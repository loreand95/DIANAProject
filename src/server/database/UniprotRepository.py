from database.GraphConnection import GraphConnection
from model.Uniprot import Uniprot

class UniprotRepository(GraphConnection):

    def store(self,uniprot:Uniprot):
        with self.driver.session() as session:
            session.run("MERGE (n:Target {"
                                    "name: $name,"
                                    "species: $species,"
                                    "geneid: $id,"
                                    "ens_code: $embl,"
                                    "ncbi_link: $id"
                                    "})", uniprot.__dict__
                        )