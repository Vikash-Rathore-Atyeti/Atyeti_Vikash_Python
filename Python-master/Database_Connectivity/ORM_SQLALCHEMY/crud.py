from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import sessionmaker,declarative_base


# create_engine – Connects SQLAlchemy to your database.
# Column – Defines a column in a database table.
# Integer, String – Specify the data types for columns.
# sessionmaker – Creates sessions to interact with the database.
# declarative_base – Base class used to define ORM models (tables).

DATABASE_URL = "mysql+pymysql://root:1234@localhost/sampledb"

# create engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# user model
class Orgnization(Base):
    __tablename__='orgnization'

    id=Column(Integer,primary_key=True)
    name=Column(String(100),unique=True)
    city=Column(String(100))

    def __repr__(self):
        return f"<Org(id={self.id},name={self.name},city={self.city})>"

# DDL : create table
Base.metadata.create_all(engine)

# CREATE
new_org=Orgnization(name="abc",city="pune")
session.add(new_org)
session.commit()
print(f"Inserted:{new_org}")

# READ

orgs = session.query(Orgnization).all()
print("All orgs")
for u in orgs:
    print(u)

#UPDATE

org_to_update = session.query(Orgnization).filter_by(name='abc').first()
if org_to_update:
    org_to_update.name='Atyeti'
    session.commit()
    print(f"Updated :{org_to_update}")

#DELETE

org_to_delete = session.query(Orgnization).filter_by(city='pune').first()
if org_to_delete:
    session.delete(org_to_delete)
    session.commit()
    print(f"Deleted :{org_to_delete}")