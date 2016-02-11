import pandas as pd
import numpy as np
import operator

def commify(num):
	    if type(num) not in [type(0), type(0L)]:
	        raise TypeError("Parameter must be an integer.")
	    if num < 0:
	        return '-' + comify(-num)
	    result = ''
	    while num >= 1000:
	        num, r = divmod(num, 1000)
	        result = ",%03d%s" % (r, result)
	    return "%d%s" % (num, result)

def percentify(num):
	perc = round(num * 100, 2)
	return '%d%%' % perc

class Poples(object):
	def __init__(self, num_teams):
		self.populations = pd.read_csv('country_pop.csv')
		self.country_array = np.array(self.populations['country_name'])
		self.teams = {}
		self.num_teams = num_teams
		self.create_teams()
		self.countries = {}
		self.submitted_teams = 0
		self.length = 1

	def return_pop(self, country):
		temp = self.populations[self.populations.country_name==country]
		return int(np.array(temp['2014']))

	def rand_country(self, size):
		return list(np.random.choice(self.country_array, size=size, replace=False))

	def end_game(self):
			correct_order = self.order_countries()
			top_score = 0
			winner = None
			print 'The correct order is:'
			for country in correct_order:
				population = commify(self.countries[country])
				print '%s with a population of %s' % (country, population)
			for name in self.teams:
				team = self.teams[name]
				team.set_score(correct_order)
				if team.score > top_score:
					winner = name
					top_score = team.score
				print '%s scored %s with %d exact matches' % (name, percentify(team.score), team.matches)
			print 'The winner of this round is %s with a score of %s' % (winner, percentify(top_score))

	def play_game(self):
		self.length = int(raw_input('Enter the number of countries for this round:'))
		countries = self.rand_country(self.length)
		print 'The countries for this round are:'
		for country in countries:
			print country
			self.countries[country] = self.return_pop(country)
		while self.submitted_teams < self.num_teams:
			team_submit = raw_input('Enter a team name to submit picks:')
			if team_submit not in self.teams:
				print '%s is not a team name, please choose a team playing this round' % team_submit
			elif self.teams[team_submit].picks != []:
				print '%s has already picked' % team_submit
			else:
				print 'The countries for this round are:'
				for country in countries:
					print country
					self.countries[country] = self.return_pop(country)
				print 'Please put these countries in order of population.'
				self.submit(team_submit)
		self.end_game()
		self.reset_game()
		self.play_game()
		
	def order_countries(self):
		sort = sorted(self.countries.items(), key=operator.itemgetter(1))
		countries = []
		for i in xrange(self.length):
			countries.append(sort.pop()[0])
		return countries
		
	def submit(self, team_name):
		print 'Setting order for %s\nEnter a country from the list, or type "go back"' % team_name
		team = self.teams[team_name]
		while len(team.picks) < self.length:
			choice = raw_input('%s %d:' % (team_name, len(team.picks)+1))
			if choice == 'go back':
				print 'Last choice removed - %s' % team.picks.pop()
			elif choice in team.picks:
				print 'This country has already been selected'
			elif choice not in self.countries:
				print 'This country is not in the list'
			else:
				team.picks.append(choice)
				print 'Picks for %s:' % team_name, team.picks
		finish = raw_input('Is %s done picking (Y/N)?' % team_name)
		if finish == 'go back' or finish.upper() == 'N':
			print 'Last choice removed - %s' % team.picks.pop()
			self.submit(team_name)
		self.submitted_teams += 1

	def create_teams(self):
		for n in xrange(self.num_teams):
			title = 'Team %d' % (n+1)
			name = raw_input("Enter %s's name: " % title)
			team = Team(name)
			self.teams[name] = team

	def reset_game(self):
		self.countries = {}
		self.submitted_teams = 0
		self.length = 1
		for team in self.teams:
			self.teams[team].reset()

class Team(object):
	def __init__(self, name):
		self.name = name
		self.score = 0
		self.picks = []
		self.matches = 0

	def set_score(self, answers):
		diff = 0
		length = len(self.picks)
		maximum = 0
		for n, pick in enumerate(self.picks):
			maximum += max((length - n), n - 1)
			actual_index = answers.index(pick)
			this_diff = abs(n - actual_index)
			if this_diff == 0:
				self.matches += 1
			else:
				diff += this_diff
		self.score = 1 - diff / float(maximum)

	def reset(self):
		self.score = 0
		self.picks = []
		self.matches = 0

if __name__ == '__main__':
	print 'Welcome to Poples, where players place populations of people in progression'
	while True:
		number_of_teams = int(raw_input("Enter the number of teams: "))
		if number_of_teams < 1:
			print 'We need at least one team to play!!'
		else:
			break
	game = Poples(number_of_teams)
	game.play_game()
# print type(return_pop('China'))
# print commify(return_pop('China'))
# print commify(return_pop('United States'))
# print commify(return_pop('Kenya'))