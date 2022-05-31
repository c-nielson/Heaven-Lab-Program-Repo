import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib
import os
from tkinter import filedialog
import xml.etree.ElementTree

def get_files():
	xml_file = filedialog.askopenfilename()
	data_file = os.path.splitext(xml_file)[0] + '.txt'
	return xml_file, data_file

def get_tree(xml_file):
	return xml.etree.ElementTree.parse(xml_file)

def save_image(data, data_file):
	ax = sns.heatmap(data)
	plt.draw()
	image_file = os.path.splitext(data_file)[0] + ".jpg"
	plt.savefig(image_file, dpi=600)
	return image_file

def show_graph(data):
	matplotlib.use("TkAgg")	
	ax = sns.heatmap(data)
	plt.show()
