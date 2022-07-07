import module
import tutor
import ReaderWriter
import timetable
import random
import math

class Scheduler:

	def __init__(self,tutorList, moduleList):
		self.tutorList = tutorList
		self.moduleList = moduleList
		self.counter = 0

	#Using the tutorlist and modulelist, create a timetable of 5 slots for each of the 5 work days of the week.
	#The slots are labelled 1-5, and so when creating the timetable, they can be assigned as such:
	#	timetableObj.addSession("Monday", 1, Smith, CS101, "module")
	#This line will set the session slot '1' on Monday to the module CS101, taught by tutor Smith. 
	#Note here that Smith is a tutor object and CS101 is a module object, they are not strings.
	#The day (1st argument) can be assigned the following values: "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
	#The slot (2nd argument) can be assigned the following values: 1, 2, 3, 4, 5 in task 1 and 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 in tasks 2 and 3. 
	#Tutor (3rd argument) and module (4th argument) can be assigned any value, but if the tutor or module is not in the original lists, 
	#	your solution will be marked incorrectly. 
	#The final, 5th argument, is the session type. For task 1, all sessions should be "module". For task 2 and 3, you should assign either "module" or "lab" as the session type.
	#Every module needs one "module" and one "lab" session type. 
	
	#moduleList is a list of Module objects. A Module object, 'm' has the following attributes:
	# m.name  - the name of the module
	# m.topics - a list of strings, describing the topics that module covers e.g. ["Robotics", "Databases"]

	#tutorList is a list of Tutor objects. A Tutor object, 't', has the following attributes:
	# t.name - the name of the tutor
	# t.expertise - a list of strings, describing the expertise of the tutor. 

	#For Task 1:
	#Keep in mind that a tutor can only teach a module if the module's topics are a subset of the tutor's expertise. 
	#Furthermore, a tutor can only teach one module a day, and a maximum of two modules over the course of the week.
	#There will always be 25 modules, one for each slot in the week, but the number of tutors will vary.
	#In some problems, modules will cover 2 topics and in others, 3.
	#A tutor will have between 3-8 different expertise fields. 

	#For Task 2 and 3:
	#A tutor can only teach a lab if they have at least one expertise that matches the topics of the lab
	#Tutors can only manage a 'credit' load of 4, where modules are worth 2 and labs are worth 1.
	#A tutor can not teach more than 2 credits per day.

	#You should not use any other methods and/or properties from the classes, these five calls are the only methods you should need. 
	#Furthermore, you should not import anything else beyond what has been imported above. 

	# Returns a true or false value depending on if the given tutor can teach the given module
	def canTeachModule(self, tut, mod):
		for topic in mod.topics:
			if topic not in tut.expertise:
				return False
		return True
	
	# Returns a true or false value depending on if the given tutor can teach the given lab
	def canTeachLab(self, tut, lab):
		for topic in lab.topics:
			if topic in tut.expertise:
				return True
		return False
	
	# Returns a list of tutor objects that can teach the given module (lecture or lab depending on lessonType input)
	def lessonTutors(self, mod, tutList, lessonType):
		listOfTutors = []
		if lessonType == "module":
			for tut in tutList:
				if self.canTeachModule(tut, mod):
					listOfTutors.append(tut)
		else:
			for tut in tutList:
				if self.canTeachLab(tut, mod):
					listOfTutors.append(tut)
		return listOfTutors
	
	# Returns a list of module objects that can taught by a tutor
	def teachableModules(self, tut, modList):
		listOfModules = []
		for mod in modList:
			if self.canTeachModule(tut, mod):
				listOfModules.append(mod)
		return listOfModules

	# Returns a string version of a tutor module object pairs for printing
	def stringTutModPairs(self, tutModPairs):
		s = ""
		for tutModPair in tutModPairs:
			s += "({}, {}): {}\n".format(tutModPair[0][0].name, tutModPair[0][1], tutModPair[1].name)
		return s
	
	# Returns a string version of a schedule for printing
	def scheduleToString(self, timeableObj):
		newString = ""
		for day in timeableObj.schedule:
			newString += "\n" + str(day) + ": "
			for slot in timeableObj.schedule[day]:
				newString += "(" + timeableObj.schedule[day][slot][0].name + ", " + timeableObj.schedule[day][slot][1].name + ", " + timeableObj.schedule[day][slot][2] + "); "
		return newString

	# Returns a true or false value depending if a tutor can teach a lecture/class depending on how many credits
	# the tutor is already using (total of 4 credits per tutor)
	def validTutor(self, tut, tutorCredits, lessonType):
		value = 2 if lessonType == "module" else 1
		if tutorCredits[tut.name] + value <= 4:
			return True
		return False

	# DFS search recursive function that generates a list of tutor module objects that is the final matching to
	# be put into the schedule in the form ((module, lessonType), tutor)
	def createMatching(self, adjList, modPairList, tutorCredits, tutModPairs, slots):
		if len(tutModPairs) >= slots:
			return tutModPairs
		elif self.counter > 20000:
			return None
		else:
			for tut in adjList[(modPairList[0][0].name, modPairList[0][1])]:
				if self.validTutor(tut, tutorCredits, modPairList[0][1]):
					tutorCredits[tut.name] += 2 if modPairList[0][1] == "module" else 1
					tutModPairs.append((modPairList[0], tut))
					result = self.createMatching(adjList, modPairList[1:], tutorCredits, tutModPairs, slots)
					if result is not None:
						return result
					tutorCredits[tut.name] -= 2 if modPairList[0][1] == "module" else 1
					tutModPairs.pop()
		self.counter += 1
		return None
	
	# Returns a true or false value depending on whether a given matching is valid (all modules are paired to a tutor
	# and no tutor has more than 4 credits used).
	def validMatching(self, matching, tutList):
		tutorCredits = {}

		for tut in tutList:
			tutorCredits[tut.name] = 0
		
		modPairUsedList = []

		for (modPair, tut) in matching:
			tutorCredits[tut.name] += 2 if modPair[1] == "module" else 1
			if tutorCredits[tut.name] > 4:
				print(tut.name)
				return False
			
			for modPairUsed in modPairUsedList:
				if modPair[0].name == modPairUsed[0].name and modPair[1] == modPairUsed[1]:
					print(modPair[0].name, modPair[1])
					return False
			modPairUsedList.append(modPair)
		return True

	# Creates a simple schedule for tasks 1 and 2 from a given matching where it inserts them horizontally from
	# Monday slot 1, Tuesday slot 1, ... , Friday slot 5 or 10. To guarantee a valid schedule.
	def simpleSchedule(self, matching, timetableObj):
		sortedMatching = sorted(matching, key=lambda x: x[1].name)
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

		dayNumber = 0
		sessionNumber = 1
		for (modPair, tut) in sortedMatching:
			timetableObj.addSession(days[dayNumber], sessionNumber, tut, modPair[0], modPair[1])
			dayNumber += 1

			if dayNumber >= len(days):
				dayNumber = 0
				sessionNumber += 1
		
		return timetableObj

	# Assigns all the modules into the optimal order filling in Monday Slot 1
	# to Thursday Slot 6, and Friday slot 1. Orders them by pairs first then
	# ordered by the number of labs the tutor teaches so the module with the least confilicts
	# is likely to be put on Friday.
	
	# Function also returns a matching of labs which are ordered pairs first then singles
	# As important to assign pairs first to minimize cost of labs.
	def minCostSchedule(self, matching, timetableObj):
		moduleMatchingPairs = []
		moduleMatchingSingles = []
		labMatchingPairs1 = []
		labMatchingPairs2 = []
		labMatchingSingles = []

		tutorMatchingsLabs = {}
		tutorMatchingsMods = {}

		tutorCountLab = {}
		tutorCountMod = {}
		for tut in self.tutorList:
			tutorMatchingsLabs[tut.name] = []
			tutorMatchingsMods[tut.name] = []
			tutorCountMod[tut.name] = 0
			tutorCountLab[tut.name] = 0
		
		for (modPair, tut) in sorted(matching, key=lambda x: x[1].name):
			if modPair[1] == "module":
				tutorCountMod[tut.name] += 1
				tutorMatchingsMods[tut.name].append((modPair, tut))
				if len(tutorMatchingsMods[tut.name]) == 2:
					moduleMatchingPairs.append(tutorMatchingsMods[tut.name][0])
					moduleMatchingPairs.append(tutorMatchingsMods[tut.name][1])
					tutorMatchingsMods[tut.name] = []
			else:
				tutorCountLab[tut.name] += 1
				tutorMatchingsLabs[tut.name].append((modPair, tut))
				if tutorCountLab[tut.name] == 2:
					labMatchingPairs1.append(tutorMatchingsLabs[tut.name][0])
					labMatchingPairs1.append(tutorMatchingsLabs[tut.name][1])
					tutorMatchingsLabs[tut.name] = []
				elif tutorCountLab[tut.name] == 4:
					labMatchingPairs2.append(tutorMatchingsLabs[tut.name][0])
					labMatchingPairs2.append(tutorMatchingsLabs[tut.name][1])
					tutorMatchingsLabs[tut.name] = []

		for name in tutorMatchingsLabs:
			if tutorMatchingsLabs[name] != []:
				labMatchingSingles.append(tutorMatchingsLabs[name][0])
		
		for name in tutorMatchingsMods:
			if tutorMatchingsMods[name] != []:
				moduleMatchingSingles.append(tutorMatchingsMods[name][0])

		moduleMatchingPairs.sort(key=lambda x: tutorCountLab[x[1].name], reverse=True)
		moduleMatchingSingles.sort(key=lambda x: tutorCountLab[x[1].name], reverse=True)

		labMatchingPairs1.sort(key=lambda x: tutorCountLab[x[1].name], reverse=True)

		labMatchingPairs2.sort(key=lambda x: tutorCountLab[x[1].name], reverse=True)
		labMatchingPairs2.reverse()

		# The lab pairs
		labMatchingPairs = labMatchingPairs1 + labMatchingPairs2

		# The lab singles ordered by the number of things the tutor teaches
		# prioritizing lectures so the most conflict singles are put in as early as possible
		# a fail first technique.
		labMatchingSingles.sort(key=lambda x: tutorCountLab[x[1].name], reverse=True)
		labMatchingSingles.sort(key=lambda x: tutorCountMod[x[1].name], reverse=True)

		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

		# assigns the lectures to their slots
		dayNumber = 0
		sessionNumber = 1
		moduleMatching = moduleMatchingPairs + moduleMatchingSingles
		(lastModulePair, lastTut) = moduleMatching.pop()
		for (modPair, tut) in moduleMatching:
			timetableObj.addSession(days[dayNumber], sessionNumber, tut, modPair[0], modPair[1])
			dayNumber += 1

			if dayNumber >= len(days)-1:
				dayNumber = 0
				sessionNumber += 1
		
		# assigns the last lecture to the first slot on Friday
		timetableObj.addSession(days[4], 1, lastTut, lastModulePair[0], lastModulePair[1])
		
		return timetableObj, labMatchingPairs + labMatchingSingles

	# Function returns a true or false value depending on if a tutor can be placed on a day
	# i.e. have they already taught two credits that day or not.
	def valid(self, modPair, tut, timetableObj, days, dayNum):
		value = 2 if modPair[1] == "module" else 1
		for session in timetableObj.schedule[days[dayNum]]:
			if timetableObj.schedule[days[dayNum]][session][0].name == tut.name:
				value += 2 if timetableObj.schedule[days[dayNum]][session][2] == "module" else 1

				if value > 2:
					return False
		
		return True
	
	# Finishes the schedule by assigning the labs in the order they were given to the first
	# available slot in the timetable. Backtracking in case of the event no more labs can be
	# entered.
	def specialSchedule(self, matching, timetableObj, days, dayNum, slot, currentCost):
		if dayNum == 5:
			return timetableObj
		else:
			for (modPair, tut) in matching:
				# if that slot has been assigned carry on to the next slot
				if timetableObj.sessionAssigned(days[dayNum], slot):
					dayNum, slot = (dayNum, slot + 1) if slot < 10 else (dayNum + 1, 1)
					return self.specialSchedule(matching, timetableObj, days, dayNum, slot, currentCost)
				else:
					# check if the tutor can actually be put here depending on the credits they
					# are teaching that day
					if self.valid(modPair, tut, timetableObj, days, dayNum):

						timetableObj.addSession(days[dayNum], slot, tut, modPair[0], modPair[1])
						newMatching = [(mP, t) for (mP, t) in matching if modPair[0].name != mP[0].name or modPair[1] != mP[1]]

						dayNum, slot = (dayNum, slot + 1) if slot < 10 else (dayNum + 1, 1)

						result = self.specialSchedule(newMatching, timetableObj, days, dayNum, slot, currentCost)
						if result is not None:
							return result
						dayNum, slot = (dayNum, slot - 1) if slot > 1 else (dayNum - 1, 10)
						del timetableObj.schedule[days[dayNum]][slot]
		return None
	
	# general schedule method for all 3 tasks
	def generalSchedule(self, n, timetableObj, hardWay):
		assert n == 1 or n == 2 or n == 3, "Hmmm WTF"
		isLab, slots = (True, 50) if n == 2 or n == 3 else (False, 25)

		# creates the list of module, lecture / module, lab pairs
		modPairList = []
		for mod in self.moduleList:
			modPairList.append((mod, "module"))
			if isLab:
				modPairList.append((mod, "lab"))

		toReverse = False if n == 1 or n == 2 else hardWay

		# sorts the tutor list by the number of modules a tutor can teach (less it can teach earlier in the list)
		tutList = sorted(self.tutorList, key=lambda x: len(self.teachableModules(x, self.moduleList)), reverse=toReverse)
		# sorts the module list by the number of tutors that can teach the module (fewer tutors means earlier in the list)
		modPairList.sort(key=lambda x: len(self.lessonTutors(x[0], tutList, x[1])))


		adjacencyList = {}
		tutorCredits = {}

		# all tutors currently teaching nothing so their credits are 0
		for tut in tutList:
			tutorCredits[tut.name] = 0

		# creates the adjacency list representation of the graph
		# one side being the modules the other side being the list of tutors that can teach the module
		for modPair in modPairList:
			adjacencyList[(modPair[0].name, modPair[1])] = self.lessonTutors(modPair[0], tutList, modPair[1])

		# finds a matching for lectures/labs to tutors
		matching = self.createMatching(adjacencyList, modPairList, tutorCredits, [], slots)
		if matching is None and hardWay:
			self.counter = 0
			return self.generalSchedule(n, timetableObj, False)
		self.counter = 0

		# checks if this matching is valid
		assert self.validMatching(matching, tutList), "Fuck bad matching"

		# For tasks 1 and 2 simple schedule is the only one required as cost is a non factor
		if n == 1 or n == 2:
			timetableObj =  self.simpleSchedule(matching, timetableObj)
		# For task 3 a special schedule to minimize the cost
		else:
			days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
			timetableObj, matching = self.minCostSchedule(matching, timetableObj)	
			timetableObj = self.specialSchedule(matching, timetableObj, days, 0, 1, 0)
		
		return timetableObj

	#This method should return a timetable object with a schedule that is legal according to all constraints of task 1.
	def createSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(1)
		#Here is where you schedule your timetable

		timetableObj = self.generalSchedule(1, timetableObj, False)

		#Do not change this line
		return timetableObj

	#Now, we have introduced lab sessions. Each day now has ten sessions, and there is a lab session as well as a module session.
	#All module and lab sessions must be assigned to a slot, and each module and lab session require a tutor.
	#The tutor does not need to be the same for the module and lab session.
	#A tutor can teach a lab session if their expertise includes at least one topic covered by the module.
	#We are now concerned with 'credits'. A tutor can teach a maximum of 4 credits. Lab sessions are 1 credit, module sessiosn are 2 credits.
	#A tutor cannot teach more than 2 credits a day.
	def createLabSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(2)
		#Here is where you schedule your timetable

		timetableObj = self.generalSchedule(2, timetableObj, False)

		#Do not change this line
		return timetableObj

	#It costs £500 to hire a tutor for a single module.
	#If we hire a tutor to teach a 2nd module, it only costs £300. (meaning 2 modules cost £800 compared to £1000)
	#If those two modules are taught on consecutive days, the second module only costs £100. (meaning 2 modules cost £600 compared to £1000)

	#It costs £250 to hire a tutor for a lab session, and then £50 less for each extra lab session (£200, £150 and £100)
	#If a lab occurs on the same day as anything else a tutor teaches, then its cost is halved. 

	#Using this method, return a timetable object that produces a schedule that is close, or equal, to the optimal solution.
	#You are not expected to always find the optimal solution, but you should be as close as possible. 
	#You should consider the lecture material, particular the discussions on heuristics, and how you might develop a heuristic to help you here. 
	def createMinCostSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(3)
		#Here is where you schedule your timetable

		timetableObj = self.generalSchedule(3, timetableObj, True)

		#Do not change this line
		return timetableObj

	#This simplistic approach merely assigns each module to a random tutor, iterating through the timetable. 
	def randomModSchedule(self, timetableObj):

		sessionNumber = 1
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		dayNumber = 0
		for module in self.moduleList:
			tut = self.tutorList[random.randrange(0, len(self.tutorList))]

			timetableObj.addSession(days[dayNumber], sessionNumber, tut, module, "module")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 6:
				sessionNumber = 1
				dayNumber = dayNumber + 1

	#This simplistic approach merely assigns each module and lab to a random tutor, iterating through the timetable.
	def randomModAndLabSchedule(self, timetableObj):

		sessionNumber = 1
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		dayNumber = 0
		for module in self.moduleList:
			tut = self.tutorList[random.randrange(0, len(self.tutorList))]

			timetableObj.addSession(days[dayNumber], sessionNumber, tut, module, "module")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 11:
				sessionNumber = 1
				dayNumber = dayNumber + 1

		for module in self.moduleList:
			tut = self.tutorList[random.randrange(0, len(self.tutorList))]

			timetableObj.addSession(days[dayNumber], sessionNumber, tut, module, "lab")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 11:
				sessionNumber = 1
				dayNumber = dayNumber + 1
