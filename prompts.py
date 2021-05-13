from colorama import Fore, Style

from constants import ERROR_PROMPT, SUCCESS_PROMPT, INFO_PROMPT, CRASH_PROMPT, SEPARATOR_PROMPT


def error_prompt(message):
	output = f'{coloured(Fore.RED, ERROR_PROMPT)}: {message}'
	print(output)


def success_prompt(message):
	print(f'{coloured(Fore.GREEN, SUCCESS_PROMPT)}: {message}')


def info_prompt(message):
	print(f'{coloured(Fore.YELLOW, INFO_PROMPT)}: {message}')


def separator_prompt():
	print(f'{coloured(Fore.WHITE, SEPARATOR_PROMPT)}')


def crash_prompt(message):
	print(f'{coloured(Fore.RED, CRASH_PROMPT)}: {message}')


def coloured(color, message):
	return f'{color}{message}{Style.RESET_ALL}'


def get_default_prompt():
	return coloured(Fore.RED, 'toucanstrike> ')
