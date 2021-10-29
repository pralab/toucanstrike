import argparse
import os

import numpy as np
from secml.array import CArray
from secml_malware.attack.blackbox.c_blackbox_problem import CBlackBoxProblem
from secml_malware.attack.blackbox.ga.c_base_genetic_engine import CGeneticAlgorithm
from secml_malware.attack.whitebox import CEnd2EndMalwareEvasion
from secml_malware.models import CClassifierEnd2EndMalware, CClassifierEmber, End2EndModel

from prompts import error_prompt, crash_prompt, info_prompt, success_prompt, separator_prompt
from state import global_state
from utils import create_wrapper_for_global_target


def strategy_check():
	if type(global_state.target) == CClassifierEmber and isinstance(global_state.attack, CClassifierEnd2EndMalware):
		error_prompt('Can\'t use end-to-end attack against not differentiable model!')
		return False
	return True


def blackbox_attack(output_path=None):
	engine = CGeneticAlgorithm(global_state.attack)
	stats = _create_stats()
	for fp in global_state.data_paths:
		with open(fp, 'rb') as handle:
			code = handle.read()
		x = CArray(np.frombuffer(code, dtype=np.uint8)).atleast_2d()
		y = CArray([1])
		try:
			adv_ds = _perform_optimization(engine, fp, stats, x, y)
			if output_path is not None:
				name = os.path.basename(fp)
				new_path = os.path.join(output_path, name + '_adv')
				engine.write_adv_to_file(adv_ds.X[0, :], path=new_path)
				success_prompt(f'Adv malware created at {new_path}')

		except Exception as e:
			crash_prompt("Damn, something went wrong!")
			crash_prompt(f"Exception details: {e}")
			raise e

	print_run_results(stats)


def _create_stats():
	stats = {
		'evasion': 0,
		'total': 0,
		'adv_score': 0,
		'before_score': 0
	}
	return stats


def whitebox_attack(output_path=None):
	stats = _create_stats()
	for file_path in global_state.data_paths:
		with open(file_path, 'rb') as handle:
			bytecode = handle.read()
		net: CClassifierEnd2EndMalware = global_state.target
		attack: CEnd2EndMalwareEvasion = global_state.attack
		x = End2EndModel.bytes_to_numpy(bytecode, net.get_input_max_length(), net.get_embedding_value(),
										net.get_is_shifting_values())
		x = CArray(x).atleast_2d()
		y = CArray([1])
		try:
			adv_ds = _perform_optimization(attack, file_path, stats, x, y)
			if output_path is not None:
				name = os.path.basename(file_path)
				new_path = os.path.join(output_path, name + '_adv')
				attack.create_real_sample_from_adv(file_path, adv_ds.X[0, :], new_path)
				success_prompt(f'Adv malware created at {new_path}')

		except Exception as e:
			crash_prompt("Damn, something went wrong!")
			crash_prompt(f"Exception details: {e}")
			raise e

	print_run_results(stats)


def print_run_results(stats):
	separator_prompt()
	success_prompt('Adversarial attack concluded!')
	success_prompt(f'# Evasions: {stats["evasion"]} / {stats["total"]}')
	success_prompt(f'Detection Rate: {(1 - stats["evasion"] / stats["total"]) * 100} %')
	success_prompt(f'Mean Original Score: {stats["before_score"] / stats["total"]}')
	success_prompt(f'Mean Adv Score: {stats["adv_score"] / stats["total"]}')


def _perform_optimization(attack, file_path, stats, x, y):
	print('-' * 10)
	info_prompt(f'Processing {file_path}...')
	y_pred, adv_score, adv_ds, f_obj = attack.run(x, y)
	y_pred = y_pred.item()
	score = adv_score[0, 1].item()
	stats['evasion'] += (1 - y_pred)
	stats['total'] += 1
	stats['adv_score'] += score
	net = create_wrapper_for_global_target()
	_, original_score = net.predict(x, return_decision_function=True)
	stats['before_score'] += original_score[0, 1]
	info_prompt(f'Results for {file_path}')
	info_prompt(f'Final label: {y_pred}')
	info_prompt(f'Initial score: {original_score}')
	info_prompt(f'Final score: {score}')
	return adv_ds


def run(args):
	if global_state.target is None:
		error_prompt('You must first set a target to attack (`target` command).')
		return
	if global_state.attack is None:
		error_prompt('You must first set an attack strategy (`whitebox` or `blackbox` commands).')
		return
	if global_state.data_paths is None:
		error_prompt('You must first set which samples to use (`data` command).')
		return
	if not strategy_check():
		return
	if args.output is not None:
		if not os.path.isdir(args.output):
			os.mkdir(args.output)
			success_prompt(f'Folder {args.output} created!')

	if isinstance(global_state.attack, CEnd2EndMalwareEvasion):
		whitebox_attack(args.output)
	elif isinstance(global_state.attack, CBlackBoxProblem):
		blackbox_attack(args.output)


def get_run_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('--output',
						help='specifies the folder where to save the resulting adversarial malware. '
							 'Name will be "name_adv". Leave blank to not save them',
						default=None)
	return parser
