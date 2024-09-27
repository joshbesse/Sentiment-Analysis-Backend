from .AnalyzerMaker import AnalyzerMaker
from .LogisticRegressionAnalyzer import LogisticRegressionAnalyzer

class LogisticRegressionAnalyzerMaker(AnalyzerMaker):
    def make_analyzer(self):
        return LogisticRegressionAnalyzer()
