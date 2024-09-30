class AnalyzerContext:
    def __init__(self, state):
        self.state = state
    
    def perform_action(self):
        self.state.perform_action()

    def change_state(self):
        self.state = self.state.change_state()