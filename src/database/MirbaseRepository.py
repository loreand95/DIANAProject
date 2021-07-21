from database.GraphConnection import GraphConnection
from model.Mirbase import Mirbase

class MirbaseRepository(GraphConnection):

    def store(self,miRNA:Mirbase):
        with self.driver.session() as session:
            session.run("MERGE (m:microRNA {"
                            "name: $id,"
                            "accession: $accession,"
                            "species: $species,"
                            "mirbase_link: $accession})", miRNA.__dict__)