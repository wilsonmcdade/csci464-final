import copy
import math
import random
from eda import process
from models import Person, Team, make_team

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

def round_robin(teamcount,all_people):
    # initial setup
    og_all_people = all_people
    # team size based on the number of teams that you want vs how many people
    teamsize = math.ceil(len(all_people)/teamcount)
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
            all_teams.append([copy.deepcopy(team_set),total_unhappiness])
    return all_teams

def main():
    # do main things
    person1 = Person("person1", 0, [], [("person7",0)])
    person2 = Person("person2", 1, [], [("person8",1)])
    person3 = Person("person3", 2, [], [])
    team1 = make_team(1, [person1, person2,  person3], 1)
    person1.partners.append((person2, 0))
    #print(evaluate([team1]))
    #for m in team1.members:
    #    print(m.get_personstr())
    #print(team1.get_teamstr())

    # give the number of teams & people to assign
    #all_teams = round_robin(7,all_people)
    # sort by badness ascending
    #all_teams.sort(key=lambda x: x[1])

    # Print out the teams and however many we can have
    #round = 0
    #for teamset in all_teams:
    #    round += 1
    #    r_string = "Round: " + str(round) + ", Unhappiness: " + str(teamset[1])
    #    print(r_string)
    #    for team in teamset[0]:
    #        print(team.get_teamstr())

    classteams = process("class.txt")
    scores = evaluate(classteams)

    i = 0
    currunit = 0
    for t in classteams:
        
        if int(t.unitnum) != currunit:
            print("Unit {0}".format(t.unitnum))
            currunit = int(t.unitnum)

        print("Team Number: {0}, Badness {1}, \t\t {2}".format(t.teamnum,scores[i],t.get_teamstr()))
        i+=1

    #for t in process():
    #    print(t.get_teamstr())
    #    for p in t.members:
    #        print(p.get_personstr())

if __name__ == '__main__':
    main()