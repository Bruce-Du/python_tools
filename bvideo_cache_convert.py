import os
import json
import sys

def convert(video_path, audio_path, convert_file_name):
	convert_command = 'ffmpeg.exe -i ' + video_path + ' -i ' + audio_path +' -c:v copy -c:a copy ' + convert_file_name
	print(convert_command)
	os.system(convert_command)

def get_dirname(json_path):
	file = open(json_path, 'r', encoding='utf-8')
	json_data = json.loads(file.read())
	return (json_data["title"], json_data["page_data"]["part"])

def convert_dir(root_path):
	for subdirname in os.listdir(root_path):
		subdir = os.path.join(root_path, subdirname)
		json_path = os.path.join(subdir, "entry.json")
		
		video_path = os.path.join(subdir, os.listdir(subdir)[0], "video.m4s")
		audio_path = os.path.join(subdir, os.listdir(subdir)[0], "audio.m4s")
		
		# 要移除空格，否则ffmpeg会报错
		convert_file_name = ""
		if(len(os.listdir(root_path)) < 2):
			convert_file_name = os.path.join(os.path.dirname(root_path), get_dirname(json_path)[0].replace(" ", "") + ".mp4")
		else:
			# 用os.path.join 比自己拼接好，避免了\转义带来的各种问题
			target_dir = os.path.join(os.path.dirname(root_path), get_dirname(json_path)[0].replace(" ", ""))
		
			if (not os.path.exists(target_dir)):
				os.mkdir(target_dir)
		
			convert_file_name = os.path.join(target_dir, get_dirname(json_path)[1].replace(" ", "") + ".mp4")
		convert(video_path, audio_path, convert_file_name)

def remove_dir(root_path):
	for root, dirs, files in os.walk(root_path, topdown=False):
		for name in files:
			os.remove(os.path.join(root, name))
		for name in dirs:
			os.rmdir(os.path.join(root, name))
	os.rmdir(root_path)

if __name__ == "__main__":
	# TODO 目录检查是否是合格的目录
	# 参数格式："D:\DownloadDir\BVideos\5028728"
	root_path = sys.argv[1]
	# TODO 把打印的结果输出为log日志
	convert_dir(root_path)
	# TODO 是否删除源目录应该可以配置
	remove_dir(root_path)
