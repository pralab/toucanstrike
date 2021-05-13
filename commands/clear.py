from prompts import success_prompt
from state import global_state

def clear():
	global_state.reset()
	success_prompt("everything has been reset!")

