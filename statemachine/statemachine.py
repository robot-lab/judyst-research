class StateMachine:

    def __init__(self):
        self.handlers = {}
        self.start_state = None
        self.end_states = []
        self.error_states = []

    def add_state(self, name, handler, end_state=None):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.end_states.append(name)

    def set_start(self, name):
        self.start_state = name.upper()

    def set_error(self, name):
        self.error_states.append(name.upper())

    def run(self, cargo):
        try:
            handler = self.handlers[self.start_state]
        except Exception:
            raise ValueError("Must call .set_start() before .run()")

        if not self.end_states:
            raise ValueError("At least one state must be an end_state")

        while True:
            if not cargo:
                # print("Not found")
                break
            new_state, cargo = handler(cargo)
            new_state = new_state.upper()
            if new_state in self.end_states:
                # print("Reached", new_state)
                if new_state in self.error_states:
                    print("Reached error state")
                break
            else:
                handler = self.handlers[new_state.upper()]
