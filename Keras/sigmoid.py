from keras.models import Sequential
from keras.layers import Dense, Activation

# 初始化模型
model = Sequential()
# 定义输入形状
# input_shape(samples, time_steps, fetures)
# feature 一个原始样本的特维度数量 （3：ax, ay, az）
# time_steps:输入的时间序列长度（多少个连样本预测一个输出） （20，两秒的数据，20个，每一秒10个）
model.add()