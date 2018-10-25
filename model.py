from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.optimizers import Adam, RMSprop



def mlp(n_obs, n_action, n_hidden_layer=1, n_neuron_per_layer=64,
        activation='relu', loss='mse'):
  """ A multi-layer perceptron """
  model = Sequential()
  model.add(Dense(n_neuron_per_layer, input_dim=n_obs[0][0], activation=activation)) ## n_obs[0][0] for training and testing
  for _ in range(n_hidden_layer):
    model.add(Dense(n_neuron_per_layer, activation=activation))
  model.add(Dense(n_action, activation='linear'))
  model.compile(loss=loss, optimizer=Adam())
  print(model.summary())
  return model

def lstm(inp_sh, outp_sh = 2, n_hidden_layer=2, n_neuron_per_layer=32,
        activation='tanh', loss='mae'):
  model = Sequential()
  model.add(LSTM(n_neuron_per_layer, return_sequences=True, dropout=0.2, recurrent_dropout=0.2,
          input_shape=inp_sh)
  for i in range(n_hidden_layer):  
    model.add(LSTM(n_neuron_per_layer, return_sequences=True, dropout=0.2, recurrent_dropout=0.2)

  model.add(Dense(outp_sh, activation=activation))

  model.compile(loss=loss, optimizer=RMSprop(), metrics=['mse'])

  return model