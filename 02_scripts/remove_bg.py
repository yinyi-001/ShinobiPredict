import os
from rembg import remove, new_session
from PIL import Image

#输入输出文件的地址
input_folder = r"D:\Code\ShinobiPredict\reference-download-complete\01-generate_data\example - naruto\output_images"
output_folder = r"D:\Code\ShinobiPredict\reference-download-complete\01-generate_data\example - naruto\output_images_no_bg"

#如果不存在就新建
if not os.path.exists(output_folder):
	os.makedirs(output_folder)

#开始循环
session = new_session("silueta")  # 创建一个新的会话
count = 0
for filename in os.listdir(input_folder):
	#仅对.jpg、.jpeg、.png文件进行处理
	if(filename.lower().endswith((".jpg", ".jpeg", ".png"))):
		input_path = os.path.join(input_folder, filename)
		#输出都强制保存为PNG格式，可以保存为透明背景
		output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.png")

		try:
			inp = Image.open(input_path)
			out = remove(inp, session=session)  # 使用指定的会话进行抠图
			out.save(output_path)
			count += 1
			print(f"成功抠图：{filename}")
		except Exception as e:
			print(f"抠图失败{filename}: {e}")

print(f"\n全部完成!共成功抠出 {count} 张图片。保存在: {output_folder}")