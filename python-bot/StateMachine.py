class StateMachine:
    def __init__(self, initialState):
        self.currentState = initialState
        #self.currentState.run ()

    def runBot(self):
        while True:
            self.currentState = self.currentState.next()
            self.currentState.run()
