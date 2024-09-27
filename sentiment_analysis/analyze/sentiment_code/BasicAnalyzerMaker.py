from .AnalyzerMaker import AnalyzerMaker
from .BasicAnalyzer import BasicAnalyzer

class BasicAnalyzerMaker(AnalyzerMaker):
    def make_analyzer(self):
        return BasicAnalyzer()
