import copy
import math
import random
from itertools import combinations

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
        #check = set(self.members.name).issubset(value.members.name)

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
        newteam.overlap += len(set(people[personi].partners) & set(people))/2

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


def round_robin(teamcount,teamsize, all_people):
    # initial setup
    og_all_people = all_people
    numval = teamsize * teamcount
    # if we need empty seats, create empty people
    for i in range(numval - len(all_people)):
        og_all_people.append(Person("empty", -random.random(), [], []))
    # 4 x count grid, each column is a team
    team_grid = [[0 for x in range(teamsize)] for y in range(teamcount)]
    round = 0
    all_teams = []
    first_team = [1]
    check = False

    while check is False:
        people_list = og_all_people[:]
        people_ind = 0
        end = people_list[len(people_list) - round:len(people_list)]
        # each set of teams gets a total unhappiness score, 
        # and a check for if they're breaking the rules
        team_set = []
        rule_broken = False
        total_unhappiness = 0
        total_overlap = 0
        if len(end) != 0:
            people_list[1:1] = end
        # For each round, change the team setup
        for j in range(teamsize):
            odd = j % 2
            for i in range(teamcount):
                if people_ind < len(people_list):
                    if odd == 0:
                        team_grid[i][j] = people_list[people_ind]
                    # assign backwards for proper round robin
                    elif odd == 1:
                        team_grid[teamcount - 1 - i][j] = people_list[people_ind]
                    people_ind = people_ind + 1
        # Then create teams based on each column
        for i in range(teamcount):
            team = make_team(i,team_grid[i],round)
            total_unhappiness += team.unhappiness
            total_overlap += team.overlap
            if team.rule_break:
                rule_broken = True
            # If this is the first team, keep it separate so we know when we go back to it
            if i == 0 and round == 0:
                first_team = copy.deepcopy(team)
            # if we hit that team stop
            else:
                check = (team == first_team)
            if check is True:
                break
            team_set.append(team)
        # Increment rounds 
        round = round + 1
        # Any formation that requires a rule to be broken doesn't get considered
        if not rule_broken and len(team_set) != 0:
            all_teams.append([copy.deepcopy(team_set),total_unhappiness,total_overlap])
    return all_teams

def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]

def brute_force(iterations, teamsize, teamcount, all_people):
    new_all_people = copy.deepcopy(all_people)
    # if we need empty seats, create empty people
    #for i in range(numval - len(all_people)):
     #   new_all_people.append(Person("empty", -random.random(), [], []))
    it_teams = []
    it_unhappy = 0
    it_overlap = 0
    counter = 0
    while counter < iterations:
        it_break = False
        random.shuffle(new_all_people)
        split = list(divide_chunks(new_all_people,4))
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
    # do main things
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

    all_people = [person1,person2,person3,person4,person5,person6,person7,person8,person9,person10,
                  person11,person12,person13,person14]

    round_robin_people = copy.deepcopy(all_people)
    random_people = copy.deepcopy(all_people)

    team1 = make_team(1, [person1, person2, person3], 1)
    print(team1.get_teamstr())


    # give the number of teams & people to assign
    all_teams = round_robin(4,4,round_robin_people)
    # sort by overlap ascending then by badness ascending
    all_teams.sort(key=lambda x: (x[2],x[1]))

    random_teams = []
    for i in range(10000):
        random_team = brute_force(5,4,4,random_people)
        random_teams.append(random_team)
    random_teams.sort(key=lambda x: (x[2],x[1]))

    # Print out the teams and however many we can have
    round = 0
    for teamset in all_teams:
        round += 1
        r_string = "Round: " + str(round) + ", Overlap: " + str(teamset[2]) + ", Unhappiness: " + str(teamset[1])
        print(r_string)
        for team in teamset[0]:
            print(team.get_teamstr())

    units = 5
    # BRUTE FORCE
    print("Total Overlap: " + str(random_teams[0][2]) + ", Unhappiness: " + str(random_teams[0][1]))
    un = 0
    for team_set in random_teams[0][0]:
        u_string = "Unit: " + str(un)
        print(u_string)
        un += 1
        for team in team_set:
            print(team.get_teamstr())



if __name__ == '__main__':
    main()