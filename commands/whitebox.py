import argparse

import cmd2
from secml_malware.models import CClassifierEnd2EndMalware, MalConv

from prompts import error_prompt, success_prompt
from state import global_state
from utils import create_correct_whitebox_attack
from constants import *


def get_white_box_parser():
	wb_parser = argparse.ArgumentParser()
	wb_parser.add_argument('--type', choices=BYTE_ATTACKS, help='how content should be injected')
	wb_parser.add_argument('--inject', help='how many bytes to inject')
	wb_parser.add_argument('--chunk', help='how many bytes to optimize at each round', default=128)
	wb_parser.add_argument('--iterations', help='how many iterations of the optimization process', default=50)
	wb_parser.add_argument('--threshold', help='the detection threshold to bypass', default=0)
	return wb_parser


def whitebox(args):
	if global_state.target is None:
		error_prompt('You have first to set a target.')
		return

	if args.type is None:
		error_prompt('You have to set an attack type.')
		error_prompt(f'Chose from this list: {BYTE_ATTACKS}')
		return

	if args.inject is None:
		if args.type != PARTIAL_DOS and args.type != HEADER_FIELDS:
			error_prompt('You have to set an injection amount.')
			return
		else:
			args.inject = 58

	args.net = global_state.target
	attack = create_correct_whitebox_attack(args)

	global_state.attack = attack

	success_prompt(f'Set up attack: {args.type}')
