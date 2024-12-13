
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
    # a team is equal if the members of the team are the same
    def __eq__(self, value):
        check = True
        for member in self.members:
            if not any(person.id == member.id for person in value.members):
                check = False
        #check = set(self.members.name).issubset(value.members.name)

        return check
    
    def get_unhappiness(self):
        unhappiness = 0

        for personi in range(len(self.members)):
            # check the preferences and update the unhappiness and whether the team breaks the rules
            for pref in self.members[personi].preference:
                for person in self.members:
                    if person.name == pref[0]:
                        unhappiness += pref[1]

        return unhappiness
    
    def get_rulebreak(self):
        rule_break = False

        for personi in range(len(self.members)):
            # check the preferences and update the unhappiness and whether the team breaks the rules
            for pref in self.members[personi].preference:
                for person in self.members:
                    if person.name == pref[0]:
                        if pref[1] == 0:
                            self.rule_break = True

        return rule_break

    def get_teamstr(self): # to help with printing
        finalstr = "Rule break!" if self.get_rulebreak() else ""
        finalstr = "Team " + str(self.teamnum) + ", Unit " + str(self.unitnum) + " ["
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