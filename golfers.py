

class Person:
    def __init__(self, name, id, partners, preferences):
        self.name = name
        self.id = id
        self.partners = partners
        self.preference = preferences # list of tuples (name of undesired partener, X)
        # where X = 0 means absolute rule
        # where X = 1 means (negative) preference


class Team:
    def __init__(self, teamnum, members, unitnum):
        self.teamnum = teamnum
        self.members = members # list of people
        self.unitnum = unitnum

    def get_teamstr(self): # to help with printing
        finalstr = "Team " + str(self.teamnum) + " ["
        first = True
        for member in self.members:
            if first:
                finalstr = finalstr + member.name
                first = False
            else:
                finalstr = finalstr + ", " + member.name
        finalstr = finalstr + "]"
        return finalstr


def make_team(teamnum, people, unitnum):
    newteam = Team(teamnum, people, unitnum)
    for personi in range(len(people)):
        without_person = people.copy()
        without_person.pop(personi)
        for notperson in without_person:
            people[personi].partners.append(notperson)
    # that should update all the people
    return newteam



def main():
    # do main things
    person1 = Person("person1", 0, [], [])
    person2 = Person("person2", 1, [], [])
    person3 = Person("person3", 2, [], [])
    team1 = make_team(1, [person1, person2,  person3], 1)
    print(team1.get_teamstr())


if __name__ == '__main__':
    main()