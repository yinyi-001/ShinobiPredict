import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt 

# ===============================
# 1.准备数据 （把Excel 变成网络能吃的矩阵）
# ===============================

print ("正在加载数据...")
cvs_path = r"D:\Code\ShinobiPredict\01_datasets\naruto_trial\battle_data.csv"
df = pd.read_csv(cvs_path)

#只提取 X 和 Y 的坐标， 。values 表示把 DataFrame 转化为 Numpy 数组
data = df[['X_Center', 'Y_Center']].values

# 用前 10 帧的数据，去预测第 11 帧（这里是实现预测的功能啊，使用LSTM)
seq_length = 10
X = []
Y = []

for i in range(len(data) - seq_length):
	# data[ i : i + n] 表示取从第 i 帧开始的 n 帧数据
	X.append(data[i : i + seq_length]) #输入：过去 10 帧的坐标
	Y.append(data[i + seq_length])	   #答案：下一帧的坐标

# 把 Python 列表转化 Pytorch 认识的张量
# dtype=torch.float32 表示数据类型是 32 位浮点数,显卡计算时，32位浮点数的速度最快
#torch.tensor() 是把 numpy 数组转化为张量的函数,相比于普通的NumPy数组，还拥有自动求导的功能
X = torch.tensor(np.array(X), dtype=torch.float32)
Y = torch.tensor(np.array(Y), dtype=torch.float32)
print (f"数据加载完成！总共切出了{len(X)}个样本。")

#================================
# 2. 搭建神经网络
#================================
class TrajectoryLSTM(nn.Module): #继承自父类nn.module
	def __init__(self): #双下划线法，说明这个函数是系统构造函数，区分其他名叫init的函数
		super(TrajectoryLSTM, self).__init__() #先构建父类的__init__
		self.lstm = nn.LSTM(input_size=2, hidden_size=32, batch_first=True)
		#m 每个时间点输入2个数字 X, Y；内部有32个“脑细胞”记忆；格式规定，说明输入的数据第一维是批次大小，第二维是时间长度（10帧）
		self.fc = nn.Linear(32, 2)
		#全连接层：翻译官作用，把32维的压缩成2维

	#前向传播 （解决数据怎么流动）
	def forward(self, x):
		out, _ = self.lstm(x)
		# 把数据给LSTM后，得到 out 每一个时间步的记忆输出，_ （另一个输出，不需要，忽略）
		out = self.fc(out[:, -1, :])
		# 很重要的 python 切片
		# ：取所有样本， -1 取最后一个时间步（第10帧）的记忆（其记忆已经包含前9帧，最适合预测第11帧）
		# ：取这32维记忆的全部特征
		# self.fc 把提炼出来的最后一次记忆喂给全连接层，输出X，Y的预测值
		return out 

# 实例化模型
model = TrajectoryLSTM()
# ===============================
# 3.开始训练
# ================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#把模型和数据全部都推到显卡上去，让他操作
model.to(device)
X, Y = X.to(device), Y.to(device)

#损失函数用 均方误差 MSE(Mean Squared Error) ，优化器用 Adam
criterion = nn.MSELoss()
#model.parameters() 把模型里所有矩阵参数拉出给优化器
#lr = learing rate 学习率， 每次微调参数的步长
optimzier = optim.Adam(model.parameters(), lr=0.005)

print ("开始训练神经网络...")
epochs = 200
for epoch in range(epochs) :
	#开启模型的Dropout
	model.train()
	optimzier.zero_grad() # 清空上一轮误差

	#1.前向传播：让他猜
	predictions = model(X)

	#2.计算误差： 猜得有多离谱
	loss = criterion(predictions, Y)

	#3.反向传播：找谁背锅
	loss.backward()

	#4.调整参数：更新矩阵
	optimzier.step()

	if(epoch + 1) % 20 == 0:
		print(f"第{epoch+1}轮训练,当前误差(Loss):{loss.item():.6f}")

# =================================
# 4.验收成果（画图对比）
# =================================
print("训练完成！正在生成图表...")

#关闭模型的Dropout
model.eval()
#告诉模型现在不计算误差，不调参数，开始测试
with torch.no_grad() :
	# 用训练好的模型预测一次
	#显卡不能画图，所以拿出来给cpu，转化为普通numpy数组，才能交给matplotlib画出对比图
	test_pred = model(X).cpu().numpy()
	test_real = Y.cpu().numpy()

#Matpltolib(python最著名的画图库) pyplot
#处理输出中文乱码的问题
plt.rcParams['font.sans-serif'] = ['SimHei'] #指定默认黑体
plt.rcParams['axes.unicode_minus'] = False # 解决输出图像方块的问题
#铺开一张12 x 6 寸的画纸
plt.figure(figsize=(12,6))
#画蓝线：真实走位
# [:, 0] ，   : 取所有行， 0 取第0列
plt.plot(test_real[:, 0], label='Real X Trajectory (真实轨迹)', color = 'blue', alpha=0.8)
#画红线：AI预测走位
plt.plot(test_pred[:, 0], label='Predicted X Trajectory (AI预测)', color='red', alpha=0.8)

plt.title("Naruto X-Coordinate Trajectory Prediction (LSTM)")
plt.xlabel("Frame Time")
plt.ylabel("X Center (0 to 1)")
plt.legend()	#在角落放一个图例
plt.grid(True)	#画上背景网格线，方便看坐标

#保存图片
save_path = r"D:\Code\ShinobiPredict\01_datasets\naruto_trial\trajectory_plot.png"
plt.savefig(save_path)	#一定要写，保存图片
print(f"图表已保存到：{save_path}")