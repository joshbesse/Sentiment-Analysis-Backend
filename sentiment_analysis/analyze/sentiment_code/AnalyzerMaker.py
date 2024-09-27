from abc import ABC, abstractmethod

class AnalyzerMaker(ABC):
    @abstractmethod
    def make_analyzer(self):
        pass 