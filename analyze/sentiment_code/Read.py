import os

class Read:
    def file_to_list(self, file):
        words = []
        try:
            current_directory = os.path.dirname(__file__)
            file_path = os.path.join(current_directory, file)
            
            with open(file_path, 'r') as current_file:
                for line in current_file:
                    words.append(line.strip())
        except FileNotFoundError:
            print(f"File not found: {file}")
        return words