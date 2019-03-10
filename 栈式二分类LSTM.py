# 在这个模型中，我们将 3 个 LSTM 层叠在一起，
# 使模型能够学习更高层次的时间表示。

# 前两个 LSTM 返回完整的输出序列，但最后一个
# 只返回输出序列的最后一步，从而降低了时间维
# 度（即将输入序列转换成单个向量）。

# 对于带状态的LSTM模型而言，在LSTM中传入参数stateful=True即可

from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.preprocessing.sequence import TimeseriesGenerator
import numpy as np

# 读取文件 返回一个n行3列的list
def readData(file_in, file_out) :
    x_train_origin = []
    y_train = []
    # 读取输入数据
    x_file = open(file_in, "r")
    for line in x_file:
        x_train_origin.append([float(x) for x in line.split()])
    x_file.close()
    # 输入数据预处理 每5组数据 构成一个滑动窗口
    x_train = []
    for i in range(5, len(x_train_origin)) :
        x_train.append([x_train_origin[i-4], x_train_origin[i-3], x_train_origin[i-2], x_train_origin[i-1], x_train_origin[i]])
    # 读取输出数据
    y_file = open(file_out, "r")
    for line in y_file:
        y_train.append([float(x) for x in line.split()])
    y_file.close()
    return np.array(x_train), np.array(y_train)

if __name__ == "__main__":

    # 输入数据尺寸的定义
    # input_shape的三个维度samples, time_steps, features
    # features: 是一个原始样本的特征维数， 对你的样本 3 ax ay az
    # time_steps: 是输入时间序列的长度，即用多少个连续样本预测一个输出。如果你希望用连续m个序列（每个序列即是一个原始样本），那么就应该设为m。
    # 当然，特殊情况是m=1
    # samples：经过格式化后的样本数。假设原始样本(3000*6), 你选择features=6, time_steps=m,则samples=3000/m

    # data_dim表示维度
    #   |-----  一个一阶的张量[1,2,3]的shape是(3,)
    #   |-----  一个二阶的张量[[1,2,3],[4,5,6]]的shape是(2,3)
    #   |-----  一个三阶的张量[[[1],[2],[3]],[[4],[5],[6]]]的shape是(2,3,1)
    # timesteps 多少个连续的样本预测一个输出 n 每秒钟5个数据的接收 设置为5
    # train_epochs 整数，训练终止时的epoch值，训练将在达到该epoch值时停止，当没有设置initial_epoch时，它就是训练的总轮数，否则训练的总轮数为epochs - inital_epoch
    data_dim = 3
    data_timesteps = 5
    train_epochs = 1000 
    train_batch_size = 5
    # 期望输入数据尺寸: (batch_size, timesteps, data_dim)
    model = Sequential()
    # 输入 5 3
    # 输出 5 32
    model.add(LSTM(32, return_sequences=True, input_shape=(data_timesteps, data_dim)))  # 返回维度为 32 的向量序列
    model.add(LSTM(32, return_sequences=True))  # 返回维度为 32 的向量序列
    model.add(LSTM(32))  # 返回维度为 32 的单个向量
    model.add(Dense(1, activation='sigmoid')) # 返回维度为1的单个向量 达到二分类的目的
    # 定义损失函数
    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    # 读取训练数据
    x_train, y_train = readData("trainInput.txt", "trainOutput.txt")

    # 读取测试数据
    x_test, y_test = readData("trainInput.txt", "trainOutput.txt")

    # 开始训练数据
    model.fit(x_train, y_train,
              batch_size = train_batch_size,
              epochs = train_epochs)

    # 数据测试 得到最终得分
    score = model.evaluate(x_test, y_test, batch_size = train_batch_size)
    print(score)