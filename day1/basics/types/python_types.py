def get_full_name1(first_name, last_name):
    full_name = first_name.title() + " " + last_name.title()
    return full_name


print(get_full_name1("john", "doe"))


def get_full_name2(first_name: str, last_name: str):
    full_name = first_name.title() + " " + last_name.title()
    return full_name


print(get_full_name2("john", "doe"))


def add(first: int | list[int, str, float], sec: int = None):
    s = 0
    for item in first:
        s += item
    return s + sec


print(add([22, 34, 54, 32], 2))

# Classes as types
class Person:
    def __init__(self, name: str):
        self.name = name


def get_person_name(one_person: Person):
    return one_person.name

a = Person("Ashu")
print(get_person_name(a))
