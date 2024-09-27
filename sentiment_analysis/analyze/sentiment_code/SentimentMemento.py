class SentimentMemento:
    def __init__(self, text, result):
        self.text = text
        self.result = result 

    def get_saved_text(self):
        return self.text 
    
    def get_saved_result(self):
        return self.result 