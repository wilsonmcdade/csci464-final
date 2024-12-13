"""
Exploratory Data Analysis script
"""

from models import Person, Team, make_team

def process(file="class.txt"):
    scientists = dict()  # set of scientists as Persons
    teams = []      # All teams
    team_count = 0
    unit_count = 0
    tmp_team = [] # List of scientists

    state = 0        # 0: reading teams
                     # 1: new round
                     # 2: reading preferences

    with open(file) as f:
        for line in f:
            if state == 0:
                if line[:5] == "Round":
                    state = 0
                    unit_count += 1
                    team_count = 0
                    continue
                if line[:11] == "Preferences":
                    state = 2
                    continue
                if line == "\n":
                    team_count += 1
                    teams.append(make_team(team_count, tmp_team, unit_count))
                    tmp_team = []
                    continue

                l = line.split(" ")

                if l[0] == "": 
                    print("Error")
                if l[2].strip() in scientists.keys():
                    p = scientists[l[2].strip()]
                else:
                    p = Person(name=l[0]+" "+l[1], id=l[2].rstrip(), partners=[], preferences=[])
                tmp_team.append(p)
                scientists[p.id] = p

                continue
            elif state == 1:
                if line == "\n":
                    state = 0
                    continue

                state = 0
                continue
            elif state == 2:
                l = line.split(",")
                scientists[l[0]].preference.append((l[1].strip(),int(l[2])))
                continue

        # State machine ended without handling preferences
        if state != 2:
            teams.append(make_team(team_count, tmp_team, unit_count))

    #for s in scientists.values():
    #    print(s.get_personstr())

    #for t in teams:
        #print(t.get_teamstr())

    return teams

#process()