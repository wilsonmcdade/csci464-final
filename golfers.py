from operator import itemgetter

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


def round_robin(teamcount, all_people,teamsize):
    # initial setup
    # 4 x count grid, each column is a team
    team_grid = [[0 for x in range(teamsize)] for y in range(teamcount)]
    people_ind = 0
    round = 0
    all_teams = []

    # Round 1
    for j in range(teamsize):
        for i in range(teamcount):
            if people_ind < len(all_people):
                team_grid[i][j] = all_people[people_ind]
                people_ind = people_ind + 1

    for i in range(teamcount):
        team = make_team(i,team_grid[i],round)
        all_teams.append(team)

    # From here we need to shift everything except 1 to the right until the teams come out the same

    return all_teams

    

def main():
    # do main things
    person1 = Person("person1", 0, [], [])
    person2 = Person("person2", 1, [], [])
    person3 = Person("person3", 2, [], [])
    person4 = Person("person4", 0, [], [])
    person5 = Person("person5", 1, [], [])
    person6 = Person("person6", 2, [], [])
    person7 = Person("person7", 0, [], [])
    person8 = Person("person8", 1, [], [])
    person9 = Person("person9", 2, [], [])
    person10 = Person("person10", 0, [], [])
    person11 = Person("person11", 1, [], [])
    person12 = Person("person12", 2, [], [])
    person13 = Person("person13", 1, [], [])
    person14 = Person("person14", 2, [], [])

    all_people = [person1,person2,person3,person4,person5,person6,person7,person8,person9,person10,person11,person12,person13,person14]

    team1 = make_team(1, [person1, person2, person3], 1)
    print(team1.get_teamstr())

    round_robin(7,all_people,2)


if __name__ == '__main__':
    main()