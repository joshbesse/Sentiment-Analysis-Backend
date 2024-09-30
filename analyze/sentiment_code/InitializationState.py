from .AnalyzerState import AnalyzerState

class InitializationState(AnalyzerState):
    def get_state(self):
        return "Initialization"
    
    def perform_action(self):
        print("\nInitialization: preparing analysis")
    
    def change_state(self):
        from .ProcessingState import ProcessingState
        return ProcessingState()