def load_model():
	"""
	Create here the model.
	If end-to-end, use End2EndModel as super class, and wrap it inside a CClassifierEnd2EndMalware.
	Otherwise, you also need to attach a load_wrapper() function to the CClassifier created by the load_model function.
	Example:
	net = YourClassifier()
	net.load_wrapper = <function that loads an CWrapperPhi object from Secml Malware>
	return net
	"""
	raise NotImplementedError("This is a dummy example for creating plugins")
