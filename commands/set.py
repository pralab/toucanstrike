import argparse

from secml_malware.attack.blackbox.c_blackbox_problem import CBlackBoxProblem
from secml_malware.attack.whitebox.c_end2end_evasion import CEnd2EndMalwareEvasion

from prompts import error_prompt, success_prompt
from state import global_state

wb_atk_map = {
	'inject': {
		'CContentShiftingEvasion': 'preferable_extension_amount',
		'CExtendDOSEvasion': 'pe_header_extension',
		'CPaddingEvasion': 'how_many',
	},
	'iterations': {},
	'is_debug': {},
	'random_init': {},
	'threshold': {},
	'chunk': {
		'CContentShiftingEvasion': 'chunk_hyper_parameter',
		'CExtendDOSEvasion': 'chunk_hyper_parameter',
	},
}

bb_atk_map = {
	'reg_par': 'regularization_parameter',
	'query_budget': 'iterations',
	'threshold': 'threshold',
	'is_debug': 'is_debug',
	'population_size': 'population_size',
}


def get_set_atk_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('key', help='The attack parameter to set.')
	parser.add_argument('value', help='The value for the specified parameter.')
	return parser


def do_set_atk(args):
	if global_state.attack is None:
		error_prompt('You must first define an attack to set its parameters.')
		return
	atk = global_state.attack
	if isinstance(atk, CEnd2EndMalwareEvasion):
		if args.key in wb_atk_map:
			atk_type = type(global_state.attack)
			if atk_type.__name__ not in wb_atk_map[args.key]:

				if not hasattr(atk, args.key):
					error_prompt(f'Key {args.key} not defined for object.')
					error_prompt(f'You can set: {wb_atk_map.keys()}.')

				setattr(atk, args.key, args.value)
				success_prompt(f'Correctly set {args.key} <- {args.value}')
			else:
				setattr(atk, wb_atk_map[args.key][atk_type.__name__], args.value)
				success_prompt(f'Correctly set "{args.key}" to {args.value}')
		else:
			error_prompt(f'Unable to set "{args.key}". Key not found or not-editable from here.')
	elif isinstance(atk, CBlackBoxProblem):
		if args.key in bb_atk_map:
			atk_type = type(global_state.attack)
			setattr(atk, bb_atk_map[args.key], args.value)
			success_prompt(f'Correctly set {args.key} <- {args.value}')
		else:
			error_prompt('Unable to set {args.key}. Key not found or not-editable from here.')
