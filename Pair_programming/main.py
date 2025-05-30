from Database.mysql_connector import DBConnection
from DTO.error import Base as ErrorBase
from DTO.warning import Base as WarnBase
from DTO.info import Base as InfoBase
from Read_Logfiles.read import LogReader
from Read_Logfiles.process import LogProcessor
 
def main():
    db = DBConnection(user='root', password='Vikas1234@', host='localhost', database='log_analysis')
    session = db.get_session()
 
    # Create tables
    ErrorBase.metadata.create_all(db.engine)
    WarnBase.metadata.create_all(db.engine)
    InfoBase.metadata.create_all(db.engine)
 
    reader = LogReader('./log_processor/input')
    processor = LogProcessor(reader, session)
    processor.process_logs()
 
if __name__ == '__main__':
    main()


 
    