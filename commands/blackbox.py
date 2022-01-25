import argparse

from constants import *
from prompts import error_prompt, success_prompt
from state import global_state
from utils import create_byte_based_black_box_attack, create_gamma_black_box_attack, \
	create_wrapper_for_global_target


def get_black_box_parser():
	bb_parser = argparse.ArgumentParser()
	bb_parser.add_argument('--type', choices=BYTE_ATTACKS + GAMMA_ATTACKS, help='how content should be injected')
	bb_parser.add_argument('--inject', help='how many bytes to inject or how many sections inject')
	bb_parser.add_argument('--query_budget', help='how many queries can be sent to the detector', default=50)
	bb_parser.add_argument('--threshold', help='the detection threshold to bypass', default=0)
	bb_parser.add_argument('--population_size', help='how many variants to consider at each iteration', default=10)
	bb_parser.add_argument('--reg_par', help='the regularization parameter. Used by gamma', default=1e-6)
	bb_parser.add_argument('--cache_file',
						   help='where to save the extracted sections. Used by gamma. None for no caching',
						   default=None)
	bb_parser.add_argument('--goodware_folder',
						   help='where to take the goodware. Used by gamma. Leave None if already set using data --goodware',
						   default=None)
	return bb_parser


def blackbox(args):
	if global_state.target is None:
		error_prompt('You have first to set a target.')
		return

	if args.type is None:
		error_prompt('You have to set an attack type.')
		error_prompt(f'Chose from this list: {BYTE_ATTACKS + GAMMA_ATTACKS}')
		return

	if args.inject is None:
		if args.type != PARTIAL_DOS and args.type != HEADER_FIELDS:
			error_prompt('You have to set an injection amount.')
			return
		else:
			args.inject = 58

	if 'gamma' in args.type:
		if args.goodware_folder is None:
			if global_state.goodware_folder is None:
				error_prompt('GAMMA needs to harvest samples from goodware, set --goodware_folder.')
				return
			args.goodware_folder = global_state.goodware_folder

	args.model = create_wrapper_for_global_target()
	attack = create_byte_based_black_box_attack(args) if 'gamma' not in args.type else create_gamma_black_box_attack(
		args)

	global_state.attack = attack

	success_prompt(f'Set up attack: {args.type}')
