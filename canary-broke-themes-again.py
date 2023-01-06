import re
import glob

keep_old = True
csv_path = "Discord Class List - Classes.csv" # get put the csv and the script on the same folder
themes_path = "C:/Users/david/powercord/src/Powercord/themes" # themes folder location (ex: "/home/username/powercord/src/Powercord/themes")

with open(csv_path,"r") as f:
	raw_csv = f.read()

classes = re.findall("(?:^|\n)\.?(.+),\.?(.+)",raw_csv)

path_list = glob.glob(f"{themes_path}/**/*.*css",recursive=True)

def replace_classes(filePath):
	with open(filePath,"r") as f:
		css = f.read()
		
	if keep_old:
		with open(filePath+".old","w") as f:
			f.write(css)
	
	for class_pair in classes:
		css = css.replace(class_pair[0],class_pair[1])
	
	with open(filePath,"w") as f:
		f.write(css)


for css_path in  path_list:
	replace_classes(css_path)


