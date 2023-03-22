class View:
	def set_save_interval() -> int:
			answer = 0
			print("How many repositories do you want each save?")
			answer = int(input())
			return answer				
  
	def set_start() -> int:
		answer = 0
		print("At what number of repositories do you want to start?")
		answer = int(input())
		return answer 
	
	def set_stop() -> int:
			answer = 0
			print("At which number of repositories do you want to stop?")
			answer = int(input())
			return answer
	
	def set_input_file_name():
		answer = ""
		print("'What is the name of the file you want to get urls from?")
		answer = input()
		return answer
	
	def set_input_file_delimiter():
		answer = ""
		print("'What delimiter does that file use?")
		answer = input()
		return answer
	
	