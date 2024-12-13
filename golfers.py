

class Person:
    def __init__(self, name, id, partners, preferences):
        self.name = name
        self.id = id
        self.partners = partners
        self.preference = preferences # list of tuples (name of undesired partener, X)
        # where X = 0 means absolute rule
        # where X = 1 means (negative) preference

    def get_personstr(self):
        finalstr = "Person: " + self.name + ", ID: " + str(self.id) + ",\t\t Partners: ["
        first = True
        for partner in self.partners:
            if first:
                finalstr = finalstr + partner[0].name + ", " + str(partner[1]) + ")"
                first = False
            else:
                finalstr = finalstr + ", (" + partner[0].name + ", " + str(partner[1]) + ")"
        finalstr = finalstr + "], Preferences: ["

        first = True
        for pref in self.preference:
            if first:
                finalstr = finalstr + pref[0] + str(pref[1])
                first = False
            else:
                finalstr = finalstr + ", " + pref[0] + str(pref[1])
        finalstr = finalstr + "]"
        
        return finalstr


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
            people[personi].partners.append((notperson,unitnum))
    # that should update all the people
    return newteam

"""
Evaluate goodness of team pairings 
Looks at previous partnerships and rule breakage
TODO: Add a smarter grading algorithm to handle some of the constraints we've chosen
"""
def evaluate(teams):
    scores = list()
    for team in teams:
        badness = 0
        for person in team.members:
            for pref in person.preference:
                if pref[0] in team.members:
                    badness += pref[1]
            for partner in person.partners:
                if team.unitnum > partner[1]:
                    if partner[0] in team.members:
                        badness += 1

        scores.append(badness)

    return scores

def main():
    # do main things
    person1 = Person("person1", 0, [], [])
    person2 = Person("person2", 1, [], [])
    person3 = Person("person3", 2, [], [])
    team1 = make_team(1, [person1, person2,  person3], 1)
    person1.partners.append((person2, 0))
    print(evaluate([team1]))
    for m in team1.members:
        print(m.get_personstr())
    print(team1.get_teamstr())


if __name__ == '__main__':
    main()