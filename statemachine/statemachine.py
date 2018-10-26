class StateMachine:

    def __init__(self, verbose=None):
        self.verbose = verbose

        self.handlers = {}
        self.start_state = None
        self.end_states = []
        self.error_end_states = []

    def add_state(self, name, handler, end_state=None):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.end_states.append(name)

    def set_start(self, name):
        self.start_state = name.upper()

    def set_error_end(self, name):
        name = name.upper()
        if name not in self.end_states:
            raise ValueError(f"State {name} must be in end_state")
        self.error_end_states.append(name)

    def run(self, cargo):
        try:
            handler = self.handlers[self.start_state]
        except Exception:
            raise ValueError("Must call .set_start() before .run()")

        if not self.end_states:
            raise ValueError("At least one state must be an end_state")

        while True:
            if not cargo:
                if self.verbose:
                    print("Not found")
                break
            new_state, cargo = handler(cargo)
            new_state = new_state.upper()
            if new_state in self.end_states:
                if self.verbose:
                    print("Reached", new_state)
                if new_state in self.error_end_states:
                    if self.verbose:
                        print("Reached error state")
                    pass
                break
            else:
                handler = self.handlers[new_state.upper()]
