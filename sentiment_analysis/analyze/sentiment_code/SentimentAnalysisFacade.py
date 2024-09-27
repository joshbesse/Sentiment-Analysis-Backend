from .BasicAnalyzerMaker import BasicAnalyzerMaker
from .AdvancedAnalyzerMaker import AdvancedAnalyzerMaker
from .LogisticRegressionAnalyzerMaker import LogisticRegressionAnalyzerMaker
from .RandomForestAnalyzerMaker import RandomForestAnalyzerMaker
from .BERTAnalyzerMaker import BERTAnalyzerMaker

class SentimentAnalysisFacade:
    def __init__(self):
        self.sentiment_analyzer = None 
        self.memento = None
    
    def show_description(self):
        print("\nBasic Analyzer: Lexicon-based sentiment analysis that adds 1 for positive words and -1 for negative words.")
        print("Advanced Analyzer: Lexicon-based sentiment analysis with added capacity for negation words, intensifier words, and diminisher words.")

    def select_analyzer(self, type):
        if type == "basic":
            maker = BasicAnalyzerMaker()
            self.sentiment_analyzer = maker.make_analyzer()
            print(f"\n{type} analyzer selected")
        elif type == "advanced":
            maker = AdvancedAnalyzerMaker()
            self.sentiment_analyzer = maker.make_analyzer()
            print(f"\n{type} analyzer selected")
        elif type == 'logistic_regression':
            maker = LogisticRegressionAnalyzerMaker()
            self.sentiment_analyzer = maker.make_analyzer()
            print(f'\n{type} analyzer selected')
        elif type == 'random_forest':
            maker = RandomForestAnalyzerMaker()
            self.sentiment_analyzer = maker.make_analyzer()
            print(f'\n{type} analyzer selected')
        elif type == 'BERT':
            maker = BERTAnalyzerMaker()
            self.sentiment_analyzer = maker.make_analyzer()
            print(f'\n{type} analyzer selected')
        else:
            print("\nPlease select 'basic' or 'advanced'.")

    def analyze_text(self, text):
        if self.sentiment_analyzer is None:
            print("\nPlease select an analyzer first.")
            return 
        result = self.sentiment_analyzer.analyze_sentiment(text)
        print(f"text: {text}\n sentiment: {result.get_sentiment()}\nscore: {result.get_score()}")
        return result 

    def save_analysis(self):
        if self.sentiment_analyzer is None:
            print("\nNo analysis to save.")
        else:
            self.memento = self.sentiment_analyzer.save_state()
            print("\nAnalysis saved.")
    
    def restore_analysis(self):
        if self.memento is None:
            print("\nNo saved analysis to restore.")
        else:
            self.sentiment_analyzer.restore_state(self.memento)
            print(f"\nstored input text: {self.memento.get_saved_text()}\nstored sentiment: {self.memento.get_saved_result().get_sentiment()}\nstored score: {self.memento.get_saved_result().get_score()}")