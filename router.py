def select_database(database):

    if database == "alternative": return "postgresql://postgres:Pedro123.321@localhost/flask1"
    if database == "default": return "postgresql://postgres:Pedro123.321@localhost/flask"
    raise Exception("invalid database router")