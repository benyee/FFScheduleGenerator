from copy import deepcopy
from random import randint
from schedule_generator import *

##############################################################################
##############################################################################
##### Tweak this part to adjust for different # of teams/weeks/divisions #####
##############################################################################
##############################################################################

num_weeks = 13
weeks = range(num_weeks)
num_teams = 10
teams = range(num_teams)

# Each team plays within their division twice, outside their division once:
schedule_requirements = [ [] for team in teams]
for team in teams:
  for team2 in teams:
    if team == team2:
      continue
    schedule_requirements[team] += [team2,]
    if team < 5 and team2 < 5:
      schedule_requirements[team] += [team2,]
    elif team >= 5 and team2 >= 5:
      schedule_requirements[team] += [team2,]
  assert len(schedule_requirements[team]) == num_weeks

print schedule_requirements

##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################

it_num = 0
max_its = 100000
valid_schedule = False
#Loop runs until a valid schedule is found or we hit max iterations
while not valid_schedule and it_num < max_its:
  print "Attempt number:", it_num
  valid_schedule = True

  #Reinitialize everything:
  schedule = [[ '' for week in weeks ] for team in teams]
  remaining_requirements = deepcopy(schedule_requirements)

  #Schedule games week by week:
  for week in weeks:
    temp_teams = deepcopy(teams)

    #Generate list of possible opponents for each team:
    possible_opponents = [ [] for team in teams ]
    for team in teams:
      for opponent in remaining_requirements[team]:
        if not week or opponent != schedule[team][week-1]:
          if opponent not in possible_opponents[team]:
            possible_opponents[team] += [opponent,]

    #Try to generate a schedule for the week:
    for team in temp_teams:
      b = len(possible_opponents[team])
      #Make sure the schedule is still possible:
      if not b:
        valid_schedule = False
        break

      #Schedule a matchup:
      opponent = possible_opponents[team][randint(0,b-1)]
      schedule[team][week] = opponent
      schedule[opponent][week] = team

      #Remove from requirements:
      remaining_requirements[team].remove(opponent)
      remaining_requirements[opponent].remove(team)

      #We don't need to schedule a game for the opponent:
      temp_teams.remove(opponent)

      #Remove these two teams from everybody's possible opponents:
      for team2 in temp_teams:
        if team2 <= team:
          continue
        if opponent in possible_opponents[team2]:
          possible_opponents[team2].remove(opponent)
        if team in possible_opponents[team2]:
          possible_opponents[team2].remove(team)

    if not valid_schedule:
      break
  it_num += 1

  #Check to see if two teams play each other twice in a 3-week span:
  for week in range(2,num_weeks):
    for team in teams:
      if schedule[team][week] == schedule[team][week-2]:
        valid_schedule = False
        break
    if not valid_schedule:
      break

  if valid_schedule:
    print "Schedule found!"
    print schedule
