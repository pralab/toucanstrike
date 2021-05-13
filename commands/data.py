import argparse
import os

import magic

from prompts import error_prompt, success_prompt
from state import global_state


def get_data_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('path', help='path to a single file or folder containing files')
	parser.add_argument('--magic', default=None, help='if set, it specifies the magic to consider.')
	parser.add_argument('--contains', default=None, help='if set, it keeps file based on substring match.')
	parser.add_argument('--remove', default=None, help='if set, it removes files based on substring match.')
	parser.add_argument('--limit', default=None, help='if set, it limits the number of retrieved files.')
	parser.add_argument('--goodware', action='store_true', help='if set, it must be a folder of goodware files.')
	return parser


def data(args):
	path = args.path
	if path is None:
		error_prompt('You have to set a path to a file or folder.')
		return
	if not os.path.isfile(path) and not os.path.isdir(path):
		error_prompt('{path} does not point to a file or folder.')
		return
	if args.goodware:
		if os.path.isdir(args.path):
			global_state.goodware_folder = args.path
			success_prompt('Goodware folder path correctly loaded!')
			return
		error_prompt("Goodware must be specified as a folder, not single files!")
		return
	if os.path.isfile(path):
		file_list = [path]
	else:
		file_list = sorted([os.path.join(path, f) for f in os.listdir(path)])
	if args.magic:
		file_list = [f for f in file_list if args.magic in magic.from_file(f)]
	if args.contains is not None:
		file_list = [f for f in file_list if args.contains in f]
	if args.remove is not None:
		file_list = [f for f in file_list if args.remove not in f]
	if args.limit is not None:
		limit = int(args.limit)
		file_list = file_list[:limit]
	global_state.data_paths = file_list
	success_prompt('File path correctly loaded!')
