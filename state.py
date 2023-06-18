from ctypes import Union
import os
from secml_malware.attack.blackbox.c_blackbox_problem import CBlackBoxProblem
from secml_malware.attack.blackbox.c_wrapper_phi import CWrapperPhi
from secml_malware.attack.whitebox import CEnd2EndMalwareEvasion
from secml_malware.models import CClassifierEnd2EndMalware


class State:
	def __init__(self):
		self.attack: Union([None, CBlackBoxProblem, CEnd2EndMalwareEvasion]) = None
		self.target: Union([None, CWrapperPhi, CClassifierEnd2EndMalware]) = None
		self.data_paths: Union([None, str]) = None
		self.goodware_folder: Union([None, str]) = None
		self.plugin_path: str = os.path.join(os.path.dirname(__file__), 'plugins')
		if not os.path.isdir(self.plugin_path):
			os.mkdir(self.plugin_path)

	def reset(self):
		self.attack = None
		self.target = None
		self.data_paths = None
		self.goodware_folder = None


global_state = State()
