

class Person:
    def __init__(self, name, id, partners, preferences):
        self.name = name
        self.id = id
        self.partners = partners
        self.preference = preferences # list of tuples (name of undesired partener, X)
        # where X = 0 means absolute rule
        # where X = 1 means (negative) preference


def main():
    # do main things
    person1 = Person("person1", 0, [], [])
    print(person1)


if __name__ == '__main__':
    main()