#---importing  required packages 

import mariadb
import sys
import random
import numpy as np

#---making class which store information about single training session 

class Trainings_data:
	def __init__(self, trainers, courts, for_team=False):
		self.trainers = trainers
		self.date = np.datetime64("2020-11-13")+random.randint(0,680)
		self.start_hour = random.randint(6,20)+random.choice([0,0.25,0.50,0.75])
		self.duration = random.randint(1,3)
		self.for_who = random.choices(["Unisex","Male","Female","Individual", "Junior Male", "Junior Female", "Junior Unisex"],[0.1,0.1,0.1,0.4,0.1,0.1,0.1])
		self.courts=courts
		self.trainer = None
		self.court = None
		if for_team:
			self.free_slots=0
			self.for_who = for_team
		elif self.for_who=="Individual":
			self.free_slots=random.randint(0,1)
		else:
			self.free_slots=random.randint(0,4)
	
	def new_time(self):
		self.date = np.datetime64("2020-11-13")+random.randint(0,680)
	
	def set_time(self, time_day, time_hour, time_duration, team_name):
		self.date = time_day
		self.start_hour = time_hour 
		self.duration = time_duration
		self.for_who = team_name
		self.trainer = self.trainers
		self.court = self.courts
	
	def return_data(self):
		return ([self.date, self.start_hour, self.duration, self.court, self.trainer, self.for_who, self.free_slots])
	
	def check_availability(self, others):
		self.trainer = None
		self.court = None
		random.shuffle(self.trainers)
		random.shuffle(self.courts)
		unavailable_courts=[]
		unavailable_trainers=[]
		for training in others:
			x=training.return_data()
			if self.date==x[0]:
				if self.start_hour>=x[1] and self.start_hour<=x[1]+x[2]:
					pass
				elif self.start_hour+self.duration>=x[1] and self.start_hour+self.duration<=x[1]+x[2]:
					pass
				elif self.start_hour<=x[1] and self.start_hour+self.duration>=x[1]+x[2]:
					pass
				else:
					continue
				unavailable_courts.append(x[3])
				unavailable_trainers.append(x[4])
			
		for t in self.trainers:
			if t not in unavailable_trainers:
				self.trainer = t
		
		for c in self.courts:
			if c not in unavailable_courts:
				self.court = c
		
		if self.trainer and self.court:
			return(0)
		else:
			return(1)

#---trying connect to database (if impossible stop executing script)
		
try:
	conn = mariadb.connect(
		user="-------", #user_name
		password="-------", #password
		host="--------", #host_adress
		port=3306,
		database="-------" #dtabase_name
	)
except mariadb.Error as e:
	print("Connection failed")
	sys.exit(1)

#---setting cursor and prepare usefull lists	

cur = conn.cursor()
num_of_trainings=random.randint(220,375)
trainers=[] #list storing trainers id
teams=[] #list storing teams information (for every team list including name, date of last member joining, etc.)
train_harmonogram=[[18,0],[18.25,0],[18.5,0],[17.5,1],[18.25,1],[18.5,1],[19.75,1],[18,2],[18.25,2],[18.5,2],[18,3],[18.25,3],[18.5,3],[17.5,4],[17.75,4],[18,4]]
#^times of training start for every team ([start_hour, day_of_week]) 
courts=["curling sheet 1", "curling sheet 2", "curling sheet 3"] #courts names

#---importing trainers ids

cur.execute(
	"SELECT employee_id FROM employees WHERE emp_position LIKE 'Trainer'"
)

#---appending ids to list

for (employee_id) in cur:
	trainers.append(employee_id[-1])


#---importing information about teams and appending to list
	
cur.execute(
	"SELECT team , MAX(join_date) as max_date FROM players GROUP BY team;"
)

for (team, max_date) in cur:
	teams.append([team, max_date])

#refilling data (trainer_id, court_name, start_hour, day_of_week)
	
for i in range(len(teams)):
	teams[i]+=[trainers[i%8],courts[i%3],train_harmonogram[i][0],train_harmonogram[i][1]]

Trainings_list=[] #list of Training objects

#making information about team trainings from 2020-11-16 to 2022-09-24

for i in range(677):
	for tm in teams:
		if tm[1]<=np.datetime64("2020-11-16")+i and i%7==tm[5]:
			TR=Trainings_data(tm[2], tm[3], for_team=True)
			TR.set_time(i+np.datetime64("2020-11-16"), tm[4], 2, tm[0])
		
			x=TR.return_data()
			y=":"
			subquery=str((str(x[0]), str(int(x[1]))+y+str(round((x[1]%1)*4)*15), str(int(x[1]+x[2]))+y+str(round(((x[1]+x[2])%1)*4)*15), x[5], x[6] ,x[4] ,x[3]))
			query=f"INSERT INTO trainings (training_day, start_hour, end_hour, for_who, free_places, trainer, court) VALUES {subquery}"
	
			cur.execute(query)
			conn.commit()
	
			Trainings_list.append(TR)

#making information about open and inividual trainings (from 2020-11-13 to 2022-09-24)

for i in range (num_of_trainings):
	TR=Trainings_data(trainers, courts)
	bo=1
	
	while bo:
		bo=TR.check_availability(Trainings_list)
		if bo:
			TR.new_time()
	
	x=TR.return_data()
	y=":"
	subquery=str((str(x[0]), str(int(x[1]))+y+str(round((x[1]%1)*4)*15), str(int(x[1]+x[2]))+y+str(round(((x[1]+x[2])%1)*4)*15), x[5][-1], x[6] ,x[4] ,x[3]))
	query=f"INSERT INTO trainings (training_day, start_hour, end_hour, for_who, free_places, trainer, court) VALUES {subquery}"
	
	cur.execute(
		query)
	conn.commit()
	
	Trainings_list.append(TR)

#closing connection

conn.close()
