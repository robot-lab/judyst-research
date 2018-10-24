from statemachine import statamachine as fsm


positive_adjectives = ["great", "super", "fun", "entertaining", "easy"]
negative_adjectives = ["boring", "difficult", "ugly", "bad"]


def start_transitions(txt):
    splitted_txt = txt.split(maxsplit=1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt, "")
    if word == "Python":
        new_state = "Python_state"
    else:
        new_state = "error_state"
    return new_state, txt


def python_state_transitions(txt):
    splitted_txt = txt.split(maxsplit=1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt, "")
    if word == "is":
        new_state = "is_state"
    else:
        new_state = "error_state"
    return new_state, txt


def is_state_transitions(txt):
    splitted_txt = txt.split(maxsplit=1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt, "")
    if word == "not":
        new_state = "not_state"
    elif word.lower() in positive_adjectives:
        new_state = "pos_state"
    elif word.lower() in negative_adjectives:
        new_state = "neg_state"
    else:
        new_state = "error_state"
    return new_state, txt


def not_state_transitions(txt):
    splitted_txt = txt.split(maxsplit=1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt, "")
    if word.lower() in positive_adjectives:
        new_state = "neg_state"
    elif word.lower() in negative_adjectives:
        new_state = "pos_state"
    else:
        new_state = "error_state"
    return new_state, txt


def main():
    state_machine = fsm.StateMachine()
    state_machine.add_state("Start", start_transitions)
    state_machine.add_state("Python_state", python_state_transitions)
    state_machine.add_state("is_state", is_state_transitions)
    state_machine.add_state("not_state", not_state_transitions)
    state_machine.add_state("neg_state", None, end_state=1)
    state_machine.add_state("pos_state", None, end_state=1)
    state_machine.add_state("error_state", None, end_state=1)
    state_machine.set_start("Start")
    state_machine.run("Python is great")
    state_machine.run("Python is difficult")
    state_machine.run("Perl is ugly")


if __name__ == "__main__":
    main()
