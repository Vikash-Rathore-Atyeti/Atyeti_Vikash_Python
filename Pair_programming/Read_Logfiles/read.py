import os, zipfile, re

class LogReader:
    def __init__(self, log_dir):
        self.log_dir = log_dir

    def get_files(self):
        for file in os.listdir(self.log_dir):
            path = os.path.join(self.log_dir, file)

            if file.endswith('.txt') and self._valid_txt(path):
                yield file, path

            elif file.endswith('.zip'):
                with zipfile.ZipFile(path, 'r') as zf:
                    extract_dir = os.path.join(self.log_dir, f'extracted_{file}')
                    zf.extractall(extract_dir)

                for inner in os.listdir(extract_dir):
                    p = os.path.join(extract_dir, inner)
                    if not inner.endswith('.txt'):
                        print(f"Invalid File Name, {inner}")
                        continue
                    if self._valid_txt(p):
                        yield inner, p

    def _valid_txt(self, path):
        try:
            with open(path) as f:
                lines = [l.strip() for l in f if l.strip()]
            if not re.match(r'^[\w\.txt]+,(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])$', lines[0]):
                print(f"Invalid header in {os.path.basename(path)}")
                return False
            if int(lines[-1]) != len(lines) - 2:
                print(f"Footer mismatch {os.path.basename(path)}")
                return False
            return True
        except:
            print(f"Validation failed for {os.path.basename(path)}")
            return False


            