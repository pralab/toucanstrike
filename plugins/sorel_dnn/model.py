import os

from secml_malware.models.c_classifier_sorel_net import CClassifierSorel


def load_model(model_path=None):
	path = os.path.join(os.path.dirname(__file__), 'model.pth') if model_path is None else model_path
	net = CClassifierSorel(path)
	return net
