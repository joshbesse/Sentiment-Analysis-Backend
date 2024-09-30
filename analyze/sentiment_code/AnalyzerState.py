from abc import ABC, abstractmethod

class AnalyzerState(ABC):
    @abstractmethod
    def get_state(self):
        pass 

    @abstractmethod
    def perform_action(self):
        pass 

    @abstractmethod
    def change_state(self):
        pass 