from .AnalyzerState import AnalyzerState

class CompletedState(AnalyzerState):
    def get_state(self):
        return "Completed"
    
    def perform_action(self):
        print("\nCompleted: analysis finished")

    def change_state(self):
        from .InitializationState import InitializationState
        return InitializationState()

