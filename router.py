def select_database(database):

    if database == "alternative": return "postgresql://postgres:password@localhost/flask1"
    if database == "default": return "postgresql://postgres:password@localhost/flask"
    raise Exception("invalid database router")
