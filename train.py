from __future__ import absolute_import
from __future__ import print_function
import numpy as np
import os
import nn_utils.network_utils as network_utils
import config.nn_config as nn_config
from keras.utils.np_utils import accuracy

config = nn_config.get_neural_net_configuration()
inputFile = config['model_file']
cur_iter = 0
model_basename = config['model_basename']
model_filename = model_basename + str(cur_iter)

#Load up the training data
print ('Loading training data')
#X_train is a tensor of size (num_train_examples, num_timesteps, num_frequency_dims)
#y_train is a tensor of size (num_train_examples, num_timesteps, num_frequency_dims)
X_train = np.load(inputFile + '_x.npy')
#y_train = np.load(inputFile + '_y.npy')
y_train = np.ones(X_train[0])
'''
X_test = np.load(inputFile + '_x.npy')
y_test = np.load(inputFile + '_y.npy')
'''
print ('Finished loading training data')



#Figure out how many frequencies we have in the data
freq_space_dims = X_train.shape[2]
hidden_dims = config['hidden_dimension_size']

#Creates a lstm network
model = network_utils.create_cxlygz(num_frequency_dimensions=freq_space_dims, num_hidden_dimensions=hidden_dims)
#You could also substitute this with a RNN or GRU
#model = network_utils.create_gru_network()

#Load existing weights if available
if os.path.isfile(model_filename):
	model.load_weights(model_filename)

num_iters = 25			#Number of iterations for training
epochs_per_iter = 25	#Number of iterations before we save our model
batch_size = 5			#Number of training examples pushed to the GPU per batch.
						#Larger batch sizes require more memory, but training will be faster
print ('Starting training!')
while cur_iter < num_iters:
	print('Iteration: ' + str(cur_iter))
	#We set cross-validation to 0,
	#as cross-validation will be on different datasets 
	#if we reload our model between runs
	#The moral way to handle this is to manually split 
	#your data into two sets and run cross-validation after 
	#you've trained the model for some number of epochs
	history = model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=epochs_per_iter, verbose=1, validation_split=0.2, show_accuracy=True)
	cur_iter += epochs_per_iter
print ('Training complete!')
#model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=nb_epoch, validation_data=(X_test, y_test), show_accuracy=True)
#score, acc = model.evaluate(X_test, y_test, batch_size=batch_size, show_accuracy=True)
#acc = accuracy(y_test, np.round(np.array(model.predict({'input': X_test}, batch_size=batch_size)['output'])))
model.save_weights(model_basename + str(cur_iter))
