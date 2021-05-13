import inspect
import os
import pkgutil
import sys
import types
from colorama import Fore, Style
from constants import banner
from interface import ToucanStrikeInterface
from prompts import success_prompt, crash_prompt


def print_banner():
	print(f'{Fore.YELLOW}{banner}{Style.RESET_ALL}')
	print('Weaponize secml-malware for fun and profit!')
	print('Type `help` for the list of available commands.')


if __name__ == '__main__':
	print_banner()
	terminal = ToucanStrikeInterface()
	sys.exit(terminal.cmdloop())

