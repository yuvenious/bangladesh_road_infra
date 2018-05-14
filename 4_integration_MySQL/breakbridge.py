"""
BREAK BRIDGES!
"""
from sqlalchemy import create_engine

db = create_engine("mysql://epa1351group1:epa1351@localhost/world")
query = ("insert into Simio (Q) values (1)")
db.execute(query)
