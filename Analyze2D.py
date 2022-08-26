import traceback
import pandas as pd
import numpy as np
import seaborn as sns
from tkinter import filedialog as fd
from matplotlib import pyplot as plt
from os.path import splitext
from xml.etree.ElementTree import ElementTree

if __name__ == '__main__':
	npixels = 1024
	pixel_nums = np.arange(1, 1025)

	params = {'scan_start': '', 'scan_stop': '', 'offset': '', 'nsteps': ''}

	try:
		tree = ElementTree()
		xml_file = fd.askopenfilename(title='Select .xml File')
		txt_file = splitext(xml_file)[0] + '.txt'
		print(txt_file)
		tree.parse(xml_file)
		root = tree.getroot()
		for elem in root.iter():
			if 'DBL' in elem.tag or 'I32' in elem.tag:
				if 'Scan.Start' in elem[0].text:
					params['scan_start'] = elem[1].text
					continue
				if 'Scan.Stop' in elem[0].text:
					params['scan_stop'] = elem[1].text
					continue
				if 'offset' in elem[0].text:
					params['offset'] = elem[1].text
					continue
				if 'NSteps' in elem[0].text:
					params['nsteps'] = elem[1].text
					continue
	except:
		traceback.print_exc()

	try:
		df = pd.read_csv(
			'C:/Users/Chris/OneDrive - Emory University/Graduate School/Heaven Lab/Data/SmO/8April2022/15340-15365_0.01_01.txt', delimiter='\t',
			names=pixel_nums
			)
		df = df.transpose()
		print(df.head())
		sns.set_theme()
		sns.heatmap(df)
		plt.show()
	except:
		traceback.print_exc()
