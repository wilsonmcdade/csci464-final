import copy
import math
import random

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
        self.unhappiness = 0
        self.rule_break = False
        self.overlap = 0
    # a team is equal if the members of the team are the same
    def __eq__(self, value):
        check = True
        for member in self.members:
            if not any(person.id == member.id for person in value.members):
                check = False

        return check

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
        # check for what overlap there is before adding the people to the partners list
        newteam.overlap += len(set(people[personi].partners) & set(people))

        for notperson in without_person:
            people[personi].partners.append(notperson)
        # check the preferences and update the unhappiness and whether the team breaks the rules
        for pref in people[personi].preference:
            for person in people:
                if person.name == pref[0]:
                    newteam.unhappiness += pref[1]
                    if pref[1] == 0:
                        newteam.rule_break = True

    # that should update all the people
    return newteam

def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]

def random_semester(iterations, teamsize, all_people):
    new_all_people = copy.deepcopy(all_people)
    it_teams = []
    it_unhappy = 0
    it_overlap = 0
    counter = 0
    while counter < iterations:
        it_break = False
        random.shuffle(new_all_people)
        split = list(divide_chunks(new_all_people,teamsize))
        team_set = []
        for i in range(len(split)):
            new_team = make_team(i,split[i],counter)
            it_unhappy += new_team.unhappiness
            it_overlap += new_team.overlap
            if new_team.rule_break:
                it_break = True
                break
            else:
                team_set.append(new_team)
        if it_break is False:
            it_teams.append(copy.deepcopy(team_set))
            counter += 1

    return [it_teams,it_unhappy,it_overlap]



def main():
    # maximum people per team
    teamsize = 4
    # number of units
    units = 4

    # people format: "name", id, [previous partners], [("disliked name", 0 or 1)]
    person1 = Person("person1", 0, [], [("person7",0)])
    person2 = Person("person2", 1, [], [("person8",1)])
    person3 = Person("person3", 2, [], [])
    person4 = Person("person4", 3, [], [])
    person5 = Person("person5", 4, [], [])
    person6 = Person("person6", 5, [], [])
    person7 = Person("person7", 6, [], [])
    person8 = Person("person8", 7, [], [])
    person9 = Person("person9", 8, [], [])
    person10 = Person("person10", 9, [], [])
    person11 = Person("person11", 10, [], [])
    person12 = Person("person12", 11, [], [])
    person13 = Person("person13", 12, [], [])
    person14 = Person("person14", 13, [], [])
    person15 = Person("person15", 2, [], [])
    person16 = Person("person16", 3, [], [])
    person17 = Person("person17", 4, [], [])
    person18 = Person("person18", 5, [], [])
    person19 = Person("person19", 6, [], [])
    person20 = Person("person20", 7, [], [])
    person21 = Person("person21", 8, [], [])
    person22 = Person("person22", 9, [], [])
    person23 = Person("person23", 10, [], [])
    person24 = Person("person24", 11, [], [])
    person25 = Person("person25", 12, [], [])
    person26 = Person("person26", 13, [], [])

    all_people = [person1,person2,person3,person4,person5,person6,person7,person8,person9,person10,
                  person11,person12,person13,person14,person15,person16,person17,person18,person19,
                  person20,person21,person22,person23,person24,person25,person26]

    numval = math.ceil(len(all_people) / teamsize) * teamsize
    empties = []
    # if we need empty seats, create empty people
    for i in range(numval - len(all_people)):
        name = "empty" + str(i)
        # don't allow more than one empty in a team
        all_people.append(Person(name, -random.random(), [], copy.deepcopy(empties)))
        empties.append((name,0))

    random_teams = []
    
    for i in range(100000):
        random_team = random_semester(units,teamsize,all_people)
        random_teams.append(random_team)
    # sort by overlap then by unhappiness
    random_teams.sort(key=lambda x: (x[2],x[1]))

    # print out the info nicely
    print("Total Overlap: " + str(random_teams[0][2]) + ", Unhappiness: " + str(random_teams[0][1]))
    un = 1
    for team_set in random_teams[0][0]:
        u_string = "Unit: " + str(un)
        print(u_string)
        un += 1
        for team in team_set:
            print(team.get_teamstr())



if __name__ == '__main__':
    main()