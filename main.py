import re

from statemachine import statemachine as fsm
from timer import Timer


key_words = [
    "статья", "статьи", "статье", "статью", "статьей", "статьёй",
    "статьи", "статей", "стаьям", "статьями", "статьях",
    "ст."
]
numbers = re.compile("([0-9]+)")


def start_transitions(txt):
    splitted_txt = txt.split(maxsplit=1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt, "")
    word = word.lower()
    if word in key_words:
        new_state = "article_state"
        print(word, end=" ")
    else:
        new_state = "start_state"
    return new_state, txt


def article_state_transitions(txt):
    splitted_txt = txt.split(maxsplit=1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt, "")
    if numbers.match(word.lower()) is not None:
        new_state = "pos_state"
        print(word)
    else:
        new_state = "error_state"
    return new_state, txt


def test_find_1(sm):
    sm.run("С учетом уточнений исковых требований в порядке статьи 49 Арбитражного процессуального кодекса Российской Федерации")


def test_find_2(sm):
    sm.run("Просит решение суда первой инстанции отменить на основании статьи 270 Арбитражного процессуального кодекса Российской Федерации")


def test_find_3(sm):
    sm.run("В соответствии с пунктом 1 статьи 721 Гражданского кодекса Российской Федерации")


def test_find_4(sm):
    sm.run("Попробуй распознать СТАТЬЮ 420 Гражданского кодекса Российской Федерации")


def test_find_5(sm):
    sm.run("Попробуй распознать СтатьЮ 421 Гражданского кодекса Российской Федерации")


def test_find_6(sm):
    sm.run("Попробуй распознать СтАтЬю 422 Гражданского кодекса Российской Федерации")


def test_not_find(sm):
    sm.run("ничего нету")


def test_reached_error_1(sm):
    sm.run("здесь находится только статья без номера")


def test_reached_error_2(sm):
    sm.run("здесь находится только статья без номера сразу, но номер 42 есть далее")


def test_real_case(sm, file_name, end=None):
    counter = 0

    with open(file_name, "r", encoding="utf-8") as file_in:
        for line in file_in:
            line = line.strip()
            if not line:
                continue
            sm.run(line)
            if end:
                counter += 1
                if counter == end:
                    break


def test_regexp(file_name, end=None):
    counter = 0

    regex = r"((стат)(ьей|ьёй|ью|ьям|ье|ьях|ьи|ья|ей|ьями)?|(ст)(\.))\s([0-9]+)"

    with open(file_name, "r", encoding="utf-8") as file_in:
        for line in file_in:
            line = line.strip()
            if not line:
                continue
            matches = re.finditer(regex, line)
            for match_num, match in enumerate(matches):
                print(f"Match {match_num + 1} was found at {match.start()}-{match.end()}: {match.group()}")
            if end:
                counter += 1
                if counter == end:
                    break


def init_state_machine():
    state_machine = fsm.StateMachine()

    state_machine.add_state("start_state", start_transitions)
    state_machine.add_state("article_state", article_state_transitions)
    state_machine.add_state("pos_state", None, end_state=True)
    state_machine.add_state("error_state", None, end_state=True)

    state_machine.set_start("start_state")
    state_machine.set_error("error_state")

    return state_machine


def main():
    sm = init_state_machine()

    # test_find_1(sm)
    # test_find_2(sm)
    # test_find_3(sm)
    # test_find_4(sm)
    # test_find_5(sm)
    # test_find_6(sm)

    # test_not_find(sm)

    # test_reached_error_1(sm)
    # test_reached_error_2(sm)

    file_name = "1 АС 897 решений за июль 2016.txt"
    # with Timer(f"Test real case document {file_name}"):
    #    test_real_case(sm, file_name)

    with Timer(f"Test real case document {file_name}"):
        test_regexp(file_name)


if __name__ == "__main__":
    main()
