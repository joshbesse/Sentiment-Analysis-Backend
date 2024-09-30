from .AnalyzerMaker import AnalyzerMaker
from .BERTAnalyzer import BERTAnalyzer

class BERTAnalyzerMaker(AnalyzerMaker):
    def make_analyzer(self):
        return BERTAnalyzer()