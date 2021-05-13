import os

from secml_malware.models import CClassifierEmber


def load_model(model_path=None):
	path = os.path.join(os.path.dirname(__file__), 'model.txt') if model_path is None else model_path
	gbdt = CClassifierEmber(tree_path=path)
	return gbdt
