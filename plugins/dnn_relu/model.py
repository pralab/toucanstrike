"""
Coull, Scott E., and Christopher Gardner.
"Activation analysis of a byte-based deep neural network for malware classification."
2019 IEEE Security and Privacy Workshops (SPW). IEEE, 2019.
"""

import os

import torch
from secml.settings import SECML_PYTORCH_USE_CUDA
from secml_malware.models import CClassifierEnd2EndMalware
from secml_malware.models.basee2e import End2EndModel

use_cuda = torch.cuda.is_available() and SECML_PYTORCH_USE_CUDA


class DnnRelu(End2EndModel):

	def __init__(self):
		super(DnnRelu, self).__init__(10, 102400, 0, True)

		self.embedding_1 = torch.nn.Embedding(num_embeddings=257, embedding_dim=10)
		self.conv1d_1 = torch.nn.Conv1d(in_channels=10, out_channels=96, kernel_size=(11,), stride=(1,), groups=1,
										bias=True)
		self.conv1d_2 = torch.nn.Conv1d(in_channels=96, out_channels=128, kernel_size=(5,), stride=(1,), groups=1,
										bias=True)
		self.conv1d_3 = torch.nn.Conv1d(in_channels=128, out_channels=256, kernel_size=(5,), stride=(1,), groups=1,
										bias=True)
		self.conv1d_4 = torch.nn.Conv1d(in_channels=256, out_channels=256, kernel_size=(5,), stride=(1,), groups=1,
										bias=True)
		self.conv1d_5 = torch.nn.Conv1d(in_channels=256, out_channels=256, kernel_size=(5,), stride=(1,), groups=1,
										bias=True)
		self.dense_1 = torch.nn.Linear(in_features=512, out_features=1, bias=True)

	def embedd_and_forward(self, x):
		conv1d_1 = self.conv1d_1(x)
		conv1d_1_activation = torch.relu(conv1d_1)
		max_pooling1d_1 = torch.max_pool1d(conv1d_1_activation, kernel_size=(4,), stride=(4,), padding=0,
										   ceil_mode=False)
		conv1d_2 = self.conv1d_2(max_pooling1d_1)
		conv1d_2_activation = torch.relu(conv1d_2)
		max_pooling1d_2 = torch.max_pool1d(conv1d_2_activation, kernel_size=(4,), stride=(4,), padding=0,
										   ceil_mode=False)
		conv1d_3 = self.conv1d_3(max_pooling1d_2)
		conv1d_3_activation = torch.relu(conv1d_3)
		max_pooling1d_3 = torch.max_pool1d(conv1d_3_activation, kernel_size=(+4,), stride=(4,), padding=0,
										   ceil_mode=False)
		conv1d_4 = self.conv1d_4(max_pooling1d_3)
		conv1d_4_activation = torch.relu(conv1d_4)
		max_pooling1d_4 = torch.max_pool1d(conv1d_4_activation, kernel_size=(4,), stride=(4,), padding=0,
										   ceil_mode=False)
		conv1d_5 = self.conv1d_5(max_pooling1d_4)
		conv1d_5_activation = torch.relu(conv1d_5)
		global_max_pooling1d_1 = torch.max_pool1d(input=conv1d_5_activation, kernel_size=conv1d_5_activation.size()[2:])
		global_average_pooling1d_1 = torch.avg_pool1d(input=conv1d_5_activation,
													  kernel_size=conv1d_5_activation.size()[2:])
		global_max_pooling1d_1_flatten = global_max_pooling1d_1.view(global_max_pooling1d_1.size(0), -1)
		global_average_pooling1d_1_flatten = global_average_pooling1d_1.view(global_average_pooling1d_1.size(0), -1)
		concatenate_1 = torch.cat((global_max_pooling1d_1_flatten, global_average_pooling1d_1_flatten), 1)
		dense_1 = self.dense_1(concatenate_1)
		activation_1 = torch.sigmoid(dense_1)
		return activation_1

	#
	# def forward(self, x):
	# 	return self._emb_forward(self.embed(x))

	def embed(self, input_x, transpose=True):
		"""
		It embeds an input vector into MalConv embedded representation.
		"""
		if isinstance(input_x, torch.Tensor):
			x = input_x.type(torch.LongTensor)
		else:
			x = torch.autograd.Variable(torch.from_numpy(input_x).type(torch.LongTensor))
		x = x.squeeze(dim=1)
		if use_cuda:
			x = x.cuda()
		emb_x = self.embedding_1(x)
		if transpose:
			emb_x = torch.transpose(emb_x, 1, 2)
		return emb_x


def load_model(model_path=None):
	linear = CClassifierEnd2EndMalware(DnnRelu())
	path = os.path.join(os.path.dirname(__file__), 'model.pth') if model_path is None else model_path
	linear.load_pretrained_model(path)
	return linear
