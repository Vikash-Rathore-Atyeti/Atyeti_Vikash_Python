import os,json,shutil,re
from datetime import datetime
from collections import Counter
from DAO.Dao import LogDAO
 
class LogProcessor:
    def __init__(self, reader, session):
        self.dao = LogDAO(session)
        self.reader = reader
 
    def process_logs(self):
        archive_dir = os.path.join('Log_processor', 'Archive')
        output_root = os.path.join('Log_processor', 'output')
 
        for file, path in self.reader.get_files():
            try:
                with open(path, encoding='utf-8-sig') as f:
                    lines = [l.strip() for l in f if l.strip()]
                content = lines[1:-1]  # Remove header and footer
 
                levels = {'info': [], 'error': [], 'warning': []}
                counts = Counter()
 
                for line in content:
                    # Match format: "YYYY-MM-DD HH:MM:SS LEVEL [Component] - Message"
                    match = re.match(
                        r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} (INFO|ERROR|WARNING)\s+\[(.*?)\] - (.+)',
                        line
                    )
                    if match:
                        level = match.group(1).lower()  # info, error, warning
                        component = match.group(2)
                        message = f"[{component}] - {match.group(3).strip()}"
                        if level in levels:
                            levels[level].append(message)
                            counts[level] += 1
 
                # Insert counts into DB (normalize warning → warn)
                for log_type, count in counts.items():
                    normalized_type = 'warning_logs' if log_type == 'warning' or 'warn' else log_type
                    self.dao.insert_log(normalized_type, file, count)
 
                # Create timestamped folder and save JSON
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                output_dir = os.path.join(output_root, timestamp)
                os.makedirs(output_dir, exist_ok=True)
 
                json_data = {
                    "file_name": file,
                    "date_of_creation": timestamp,
                    "log_levels": {
                        ('warn' if lvl == 'warning' else lvl): {
                            "messages": msgs,
                            "count": len(msgs)
                        }
                        for lvl, msgs in levels.items()
                    }
                }
                json_path = os.path.join(output_dir, file.replace('.txt', '.json'))
                with open(json_path, 'w', encoding='utf-8') as jf:
                    json.dump(json_data, jf, indent=2)
 
                # Move .txt file to archive
                original_txt = os.path.join(self.reader.log_dir, file)
                if os.path.exists(original_txt):
                    shutil.move(original_txt, os.path.join(archive_dir, file))
 
                # Move corresponding .zip file to archive if it exists
                zip_name = file.rsplit('.', 1)[0] + '.zip'
                original_zip = os.path.join(self.reader.log_dir, zip_name)
                if os.path.exists(original_zip):
                    shutil.move(original_zip, os.path.join(archive_dir, zip_name))
 
            except Exception as e:
                print(f"Error processing {file}: {e}")