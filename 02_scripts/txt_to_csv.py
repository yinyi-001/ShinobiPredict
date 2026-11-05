import os
import csv

input_folder =  r"D:\Code\ShinobiPredict\yolov5\runs\detect\exp5\labels"
output_csv = r"D:\Code\ShinobiPredict\01_datasets\naruto_trial\battle_data.csv"

with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
	writer = csv.writer(file)
	#表头： 帧号、类别、x中心、y中心、宽度、高度
	writer.writerow(['Frame', 'Class', 'X_Center', 'Y_Center', 'Width', 'Height'])

	#定义一个函数来提取帧号，让sotred函数按帧号排序
	def get_frame_num(f):
		return int(f.split('_')[-1].replace('.txt',''))

	
	for filename in sorted(os.listdir(input_folder), key=get_frame_num) :#使其按时间顺序排好
		if filename.endswith(".txt"):
			#从文件名中提取帧数，例如video_03_7.txt 提出7
			frame_num = int(filename.split('_')[-1].replace('.txt', ''))#split在_位置断开，-1取最后一段"7.txt"

			file_path = os.path.join(input_folder, filename)
			with open(file_path, 'r') as f:
				lines = f.readlines()
				#如果一个txt里有多个鸣人（影分身），每一行都存一条记录
				for line in lines:
					data = line.strip().split() #去掉首尾的空白符；split无参数就以空白符为刀开切
					if len(data) == 5: #确保是标准的YOLO格式
						writer.writerow([frame_num] + data)

print(f"清洗完成！数据已经保存到：{output_csv}")