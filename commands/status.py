from prompts import info_prompt
from state import global_state


def status():
	info_prompt(f'Target: {global_state.target}')
	info_prompt(f'Attack: {global_state.attack}')
	info_prompt(f'Data: {global_state.data_paths}')
