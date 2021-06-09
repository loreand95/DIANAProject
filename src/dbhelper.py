def db_connect():
    """
    Connect to the DB and return a Session object.
    """

    # Open a connection to the db
    from neo4j import GraphDatabase, basic_auth, exceptions
    driver = GraphDatabase.driver(
        "bolt://localhost:7687",
        auth=basic_auth("neo4j", "password")
    )
    return driver.session()

def create_db_info(name, link):
    """
    Create, if it does not exist, a DB_info node.

    Parameters
    ----------
    name : str
        DB name
    link : str
        Link to the DB official web site
    """

    # Connect to the DB
    session = db_connect()

    # Prepare the statement parameters
    params = {
        'name' : name,
        'link' : link
    }

    # Execute a MERGE statement
    session.run("MERGE (d:DB_info {"
                  "name:{name},"
                  "link:{link}"
                "})", params)

    # Close the session
    session.close()

def create_relation_info(name, source_db_link, min_value, max_value, cut_off):
    """
    Create (or update) a Relation_general_info node.

    Parameters
    ----------
    name : str
        Name of the relation
    source_db_link : str
        Web link to the data source
    min_value : float
        Minimum observed value of the score
    max_value : float
        Maximum observed value of the score
    cut_off : float
        Cut off value of the score
    """

    # Connect to the DB
    session = db_connect()

    # Prepare the statement parameters
    params = {
        'name'           : name,
        'source_db_link' : source_db_link,
        'min_value'      : min_value,
        'max_value'      : max_value,
        'cut_off'        : cut_off
    }

    # Execute the MERGE statement
    session.run("MERGE (r:Relation_general_info {"
                  "name:{name},"
                  "source_db_link:{source_db_link},"
                  "min_value:{min_value},"
                  "max_value:{max_value},"
                  "cut_off:{cut_off}"
                "})", params)

    # Close the session
    session.close()