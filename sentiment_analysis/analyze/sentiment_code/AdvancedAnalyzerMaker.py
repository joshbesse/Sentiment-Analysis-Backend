from .AnalyzerMaker import AnalyzerMaker
from .AdvancedAnalyzer import AdvancedAnalyzer

class AdvancedAnalyzerMaker(AnalyzerMaker):
    def make_analyzer(self):
        return AdvancedAnalyzer()