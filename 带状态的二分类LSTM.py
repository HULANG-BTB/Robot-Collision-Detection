# 有状态的循环神经网络模型中，在一个 batch 的样本处理完成后，
# 其内部状态（记忆）会被记录并作为下一个 batch 的样本的初始
# 状态。这允许处理更长的序列，同时保持计算复杂度的可控性。

from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np

data_dim = 16
timesteps = 8
num_classes = 1
batch_size = 32

# 期望输入数据尺寸: (batch_size, timesteps, data_dim)
# 请注意，我们必须提供完整的 batch_input_shape，因为网络是有状态的。
# 第 k 批数据的第 i 个样本是第 k-1 批数据的第 i 个样本的后续。
model = Sequential()
model.add(LSTM(32, return_sequences=True, stateful=True,
               batch_input_shape=(batch_size, timesteps, data_dim)))
model.add(LSTM(32, return_sequences=True, stateful=True))
model.add(LSTM(32, stateful=True))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# 生成虚拟训练数据 x 数据 y 结果
x_train = np.random.random((batch_size * 10, timesteps, data_dim))
y_train = np.random.random((batch_size * 10, num_classes))

print(x_train)
print(y_train)
# 生成虚拟验证数据 x 数据 y 结果
x_val = np.random.random((batch_size * 3, timesteps, data_dim))
y_val = np.random.random((batch_size * 3, num_classes))
'''
# 开始训练模型
model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=20,
          shuffle=False)
score = model.evaluate(x_val, y_val, batch_size = batch_size)
print(score)
'''