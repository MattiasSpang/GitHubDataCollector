class View:

	def __init__(self):
		self.random_variable = True

	def set_save_interval(self) -> int: # can be removed as we save when a token is done. 
			answer = 0
			print("How many repositories do you want each save?")
			answer = int(input())
			return answer				
  
	def set_start(self) -> int:
		answer = 0
		print("At what number of repositories do you want to start?")
		answer = int(input())
		return answer 
	
	def set_stop(self) -> int:
			answer = 0
			print("At which number of repositories do you want to stop?")
			answer = int(input())
			return answer
	
	def set_input_file_name(self):
		answer = ""
		print("'What is the name of the file you want to get urls from?")
		answer = input()
		return answer
	
	def set_input_file_delimiter(self):
		answer = ""
		print("'What delimiter does that file use?")
		answer = input()
		return answer
	
	def change_settings(self) -> dict:

		settings = {"filename" : "default_name.csv", "startline" : 0, "endline" : 0}
		while True:
			print("Welcome to the settings menu, please select what setting to change:")
			print("OutPut File Name - write OPFN")
			print("What line in csv to start at - write SL")
			print("What line in the csv file to end on - write EL")
			print("Exit settings menu - write exit")

			answer = input()

			if answer == "OPFN":
				settings["filename"] = self.set_input_file_name()
				continue
			elif answer == "SL":
				settings["startline"] = self.set_start()
				continue
			elif answer == "EL":
				settings["endline"] = self.set_stop()
				continue
			
			if answer == "exit" or answer == "e" or answer == "stop":
				break

			print("No valid command given, please select a valid command")

		return settings
	
	def enter_settings(self) -> dict:

		settings = {"filename" : "default_name.csv", "startline" : 0, "endline" : 0}
		
		while True:
			print("Do you want to enter settings? (y,n)")
			answer = input()

			if answer == "y" or answer == "yes":
				settings = self.change_settings()
				continue
			elif answer == "n" or answer == "no":
				break

			print("No valid command given, please enter valid command.")

		return settings

		