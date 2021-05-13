import argparse
import os
import numpy as np
from secml.array import CArray

from prompts import error_prompt, success_prompt, info_prompt, separator_prompt
from state import global_state
from utils import create_wrapper_for_global_target


def get_predict_parser():
	infer_parser = argparse.ArgumentParser()
	infer_parser.add_argument('--path', help='the file to be scored. Leave unset to predict already loaded file list',
							  default=None)
	return infer_parser


def predict(args):
	if global_state.target is None:
		error_prompt('First you need to set a target.')
		return
	if args.path is None:
		if global_state.data_paths is None:
			error_prompt('You have to give an input path.')
			return
		paths = global_state.data_paths
	elif not os.path.isfile(args.path):
		error_prompt(f'{args.path} does not exists.')
		return
	else:
		paths = [args.path]
	net = create_wrapper_for_global_target()

	stats = {
		'detected': 0,
		'total': 0,
		'confidence': 0,
	}

	for p in paths:
		with open(p, 'rb') as handle:
			code = handle.read()
		info_prompt(f'Computing prediction for {p}')
		code = CArray(np.frombuffer(code, dtype=np.uint8)).atleast_2d()
		y_pred, confidence = net.predict(code, return_decision_function=True)
		y_pred = y_pred.item()
		score = confidence[0, 1].item()
		stats['detected'] += int(y_pred != 0)
		stats['total'] += 1
		stats['confidence'] += score
		info_prompt(f'predicted label: {y_pred}')
		info_prompt(f'confidence: {score}')
		print('-' * 20)
	if stats['total'] >= 1:
		separator_prompt()
		success_prompt('Prediction stats:')
		success_prompt(f'Detected: {stats["detected"]} / {stats["total"]}')
		success_prompt(f'Detection Rate: {stats["detected"] / stats["total"] * 100} %')
		success_prompt(f'Mean confidence: {stats["confidence"] / stats["total"]}')
