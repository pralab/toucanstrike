import sys

from colorama import Fore, Style

from constants import banner
from interface import ToucanStrikeInterface


def print_banner():
	print(f'{Fore.YELLOW}{banner}{Style.RESET_ALL}')
	print('Weaponize secml-malware for fun and profit!')
	print('Type `help` for the list of available commands.')


if __name__ == '__main__':
	print_banner()
	terminal = ToucanStrikeInterface()
	print("test 1")
	sys.exit(terminal.cmdloop())
	print("test 1")

