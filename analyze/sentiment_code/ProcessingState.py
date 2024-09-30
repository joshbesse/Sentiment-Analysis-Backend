class ProcessingState:
    def get_state(self):
        return "Processing"
    
    def perform_action(self):
        print("\nProcessing: analyzing sentiment")

    def change_state(self):
        from .CompletedState import CompletedState
        return CompletedState()