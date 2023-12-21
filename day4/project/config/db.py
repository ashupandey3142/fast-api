from sqlalchemy import create_engine, MetaData

# ORMs -> object-relational mapping
# An ORM has tools to convert ("map") between objects in code and database tables ("relations").
# With an ORM, you normally create a class that represents a table in a SQL database,
# each attribute of the class represents a column, with a name and a type.
# For example a class Pet could represent a SQL table pets.
# And each instance object of that class represents a row in the database.

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
meta = MetaData()
try:
    con = engine.connect()
    print("Connected successfully!")
except Exception as e:
    print(f"Error: {e}")
finally:
    if con:
        con.close()

