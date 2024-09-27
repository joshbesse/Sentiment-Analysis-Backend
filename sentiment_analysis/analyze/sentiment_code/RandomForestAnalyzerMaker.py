from .AnalyzerMaker import AnalyzerMaker
from .RandomForestAnalyzer import RandomForestAnalyzer

class RandomForestAnalyzerMaker(AnalyzerMaker):
    def make_analyzer(self):
        return RandomForestAnalyzer()