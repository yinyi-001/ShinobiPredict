import sys
# print(sys.executable)
import cv2
import os

#1、设置视频路径和输出图片的文件夹
# video_path = r"D:\Code\ShinobiPredict\reference-download-complete\01-generate_data\example - naruto\C_naruto_a.mp4"
# output_folder = r"D:\Code\ShinobiPredict\reference-download-complete\01-generate_data\example - naruto\output_images"

# 1、1）检查有没有拖入视频文件
if len(sys.argv) < 2:
	print("请拖入视频文件到脚本上！")
	sys.exit()
# 2）获取输入文件的完整路径
video_path = sys.argv[1]
video_name = os.path.splitext(os.path.basename(video_path))[0]  # 获取视频文件名（不带扩展名）

base_images_dir = r"D:\Code\ShinobiPredict\01_datasets\naruto_action_trial\images_all"
output_folder = os.path.join(base_images_dir, video_name)

#创建输出文件夹（如果不存在）
if not os.path.exists(output_folder):
	os.makedirs(output_folder)

#2、读取视频文件
cap = cv2.VideoCapture(video_path)
# 检查和输出帧率与保存地址
if not cap.isOpened():
	print(f"无法打开视频文件{video_path}，请检查路径是否正确！")
	sys.exit()

fps = cap.get(cv2.CAP_PROP_FPS)
print(f"视频帧率: {fps} FPS")
print(f"输出图片保存路径: {output_folder}")


frame_count = 0
save_interval = 8 #每隔5帧保存一张图片

while True:
	ret, frame = cap.read()
	if not ret:
		break #视频读取完毕，退出循环

	#每隔save_interval帧保存一张图片，防止图片过多重复
	if frame_count % save_interval == 0:
		img_name = f"{output_folder}/frame_{frame_count:04d}.jpg"
		cv2.imwrite(img_name, frame)

	frame_count += 1

cap.release()
print(f"视频拆帧完成！共截取{frame_count // save_interval}张图片。")