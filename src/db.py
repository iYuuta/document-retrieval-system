from sqlalchemy import create_engine, Column, Integer, text, Text, ARRAY, Float
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker
from src.document import Document as RagDocument
from dotenv import load_dotenv
import os

load_dotenv()
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
db = os.getenv("POSTGRES_DB")
DATABASE_URL = f"postgresql://{user}:{password}@localhost:5432/{db}"
try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
except OperationalError:
    print("Error: Could not connect to the database at startup.")
    exit()
Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    embedding = Column(ARRAY(Float))

Session = sessionmaker(bind=engine)

def insert_doc(doc: RagDocument):
    session = Session()
    try:
        for chunk, vector in zip(doc.chunks, doc.vectors):
            doc_obj = Document(content=chunk, embedding=vector)
            session.add(doc_obj)
        session.commit()
        return True
    except OperationalError:
        print("Error: Database connection failed during insert.")
        session.rollback()
        return False
    except SQLAlchemyError as e:
        print("Error during insert:", e)
        session.rollback()
        return False
    finally:
        try:
            session.close()
        except Exception:
            print("Error: couldn't clean up the db session.")
    
def get_docs():
    docs = []
    try:
        session = Session()
        docs = session.query(Document).all()
    except OperationalError:
        print("Error: Database connection failed")
    except SQLAlchemyError as e:
        print("Error: ", e)
    finally:
        try:
            session.close()
        except:
            print("Error: couldn't clean up the db session")
    return docs