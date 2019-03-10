class StateMachine:
    def __init__(self, initialState):
        self.currentState = initialState
        self.currentState.run ()

    def run(self):
        self.currentState = self.currentState.next()
        self.currentState.run()
