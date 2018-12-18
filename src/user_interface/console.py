from chat import create_database
from chat import create_training_data
from web_controller import open_website
from web_controller import google_phrase
from programs import create_database as create_programs_database
from programs import clear_database as clear_programs_database
from programs import open_program
from programs import close_program
from programs import add_program_manually
from chat.AI_nmt.inference import answer
import subprocess
import colorama
from contextlib import contextmanager
import os
import sys



@contextmanager
def cd(newdir):
	prevdir = os.getcwd()
	os.chdir(os.path.expanduser(newdir))
	try:
		yield
	finally:
		os.chdir(prevdir)
		# outside the context manager we are back wherever we started.


def sendMessage(text):
	print(f'{colorama.Fore.LIGHTRED_EX}{text}{colorama.Fore.RESET}')
	this.list_to_say.append(text)

def print_user_options():
	print("1 - Create Database")
	print("2 - Open Program")
	print("3 - Close Program")
	print("4 - Open Website")
	print("5 - Search in Google")
	print("6 - Clear Database")
	print("7 - Manually add program to the Database")
	print("8 - Teach me how to speak")
	print("")
	print("0 - Exit")
	print("")
	print("")


class switch(object):
	value = None

	def __new__(class_, value):
		class_.value = value
		return True


def case(*args):
	return any((arg == switch.value for arg in args))

this = sys.modules[__name__]

this.list_to_say = []
this.exit_flag = []

def display_menu(shared_list_to_say, fileno, shared_exit_flag):
	this.list_to_say = shared_list_to_say
	this.exit_flag = shared_exit_flag
	os.chdir(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
	sys.stdin = os.fdopen(fileno)  # open stdin in this process

	sendMessage("Yo. I'm Ace!")

	user_choice = -1

	while user_choice != "0":
		sendMessage("")
		sendMessage("Let's go")

		print_user_options()
		user_choice = input(('You: '))


		while switch(user_choice):
			if case("1"):
				sendMessage("Creating Database...")
				try:
					create_programs_database.Execute()
				except Exception as e:
					sendMessage("Cannot create database")
					sendMessage(e)
				break

			if case("2"):
				program_to_open = input('Type name of the program: ')
				sendMessage("Opening Program... " + program_to_open)
				try:
					open_program.Execute(program_to_open)
				except Exception as e:
					sendMessage("Cannot open " + program_to_open)
					sendMessage(e)
				break

			if case("3"):
				program_to_close = input('Type name of the program: ')
				sendMessage("Closing Program... " + program_to_close)
				try:
					close_program.Execute(program_to_close)
				except Exception as e:
					sendMessage("Cannot close" + program_to_close)
					sendMessage(e)
				break

			if case("4"):
				url_to_open = input('Write the url: ')
				sendMessage("Opening website... " + url_to_open)
				try:
					open_website.Execute(url_to_open)
				except Exception as e:
					sendMessage("Cannot navigate to" + url_to_open)
					sendMessage(e)
				break

			if case("5"):
				phrase_to_search = input('What are you looking for: ')
				sendMessage("Searching in Google for... " + phrase_to_search)
				try:
					google_phrase.Execute(phrase_to_search)
				except Exception as e:
					sendMessage("Cannot find " + phrase_to_search + " in Google")
					sendMessage(e)
				break

			if case("6"):
				sendMessage("Clearing database...")
				try:
					clear_programs_database.Execute()
				except Exception as e:
					sendMessage("Cannot clear database")
					sendMessage(e)
				break

			if case("7"):
				sendMessage("Adding program...")
				try:
					add_program_manually.Execute()
				except Exception as e:
					sendMessage("Cannot add program")
					sendMessage(e)
				break

			if case("8"):

				sendMessage("Say 'yes' if you really want spend few hours looking me learning dude...")
				user_input = input(('You: '))

				if user_input == 'yes':
					sendMessage("Learning how to speak...")
					try:
						sendMessage("Gathering vocabulary")
						create_database.Execute()
						create_training_data.Execute()

						with cd(os.getcwd() + "\AI_nmt\setup"):
							sendMessage("Preparing data for train")
							subprocess.call("py .\prepare_data.py")

						with cd(os.getcwd() + "\AI_nmt"):
							sendMessage("The training begins now!")
							subprocess.call("python -c \"from train import Execute; Execute()\"")

						with cd(os.getcwd() + r"\AI_nmt\utils"):
							sendMessage("Extracting files to deploy")
							subprocess.call("python prepare_for_deployment.py")

					except Exception as e:
						sendMessage("I still cannot speak :(")
						sendMessage(e)
				break

			if case("0"):
				sendMessage("Exiting")
				this.exit_flag.append(1)
				break

			sendMessage(answer(user_choice))
			break