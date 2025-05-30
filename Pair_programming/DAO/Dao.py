from DTO.error import ErrorLog
from DTO.info import InfoLog
from DTO.warning import WarnLog
import logging
 
class LogDAO:
    def __init__(self, session):
        self.session = session
 
    def insert_log(self, log_type, file_name, count):
        try:
            model_map = {
                'error_logs': ErrorLog(log_file = file_name, error_frequency = count),
                'info_logs': InfoLog(log_file = file_name, info_frequency = count),
                'warning_logs': WarnLog(log_file = file_name, warning_frequency = count),
            }
            entry = model_map.get(log_type)
            if entry:
                self.session.add(entry)
                self.session.commit()
               
            else:
                logging.warning(f"Unknown log type: {log_type}")
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error inserting log: {e}")