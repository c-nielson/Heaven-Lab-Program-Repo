import traceback
from os.path import splitext
from tkinter import filedialog as fd
from xml.etree.ElementTree import ElementTree

import numpy as np
import pandas
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

npixels = 1024
nm_per_pixel = 0.125
pixel_nums = np.arange(1, 1025)


# Converts num given in nm or cm-1 to the other
def convert_nm_cm(num: float) -> float:
	return 10000000 / num


# Opens a file dialog and returns both the name of the selected .xml file as well as the accompanying .txt file
def get_filenames() -> (str, str):
	xml_file = fd.askopenfilename(title='Select .xml File', filetypes=[('XML', '*.xml')])
	txt_file = splitext(xml_file)[0] + '.txt'
	return xml_file, txt_file


# Returns data frame from .txt file matching filename (.xml). Creates 'nm_Offset' column and adjusts column names based on params.
def get_df(filename: str, params: dict) -> pd.DataFrame:
	try:
		df = pd.read_csv(
			filename, delimiter='\t', names=pixel_nums
		).transpose()

		# center_index is representative of resonant fluorescence; resonance is considered as 0 offset
		center_index = int(
			(npixels / 2) + (convert_nm_cm(params['scan_start']) - convert_nm_cm(params['scan_start'] - params['offset'])) / nm_per_pixel
			)
		high_energy_nm = -((center_index - 1) * nm_per_pixel)
		low_energy_nm = ((npixels - center_index) * nm_per_pixel)
		df.columns = np.linspace(params['scan_start'], params['scan_stop'], params['nsteps'])
		df['nm Offset'] = np.linspace(high_energy_nm, low_energy_nm, 1024)
		df = df.set_index('nm Offset')

		return df
	except:
		traceback.print_exc()


# Iterates through given .xml file and pulls out params of scan. Returns dict of params.
def get_params(filename: str) -> dict:
	params = {'scan_start': None, 'scan_stop': None, 'scan_step': None, 'offset': None, 'nsteps': None}

	try:
		tree = ElementTree()
		tree.parse(filename)
		root = tree.getroot()
		for elem in root.iter():
			if 'DBL' in elem.tag or 'I32' in elem.tag:
				if 'Scan.Start' in elem[0].text:
					params['scan_start'] = float(elem[1].text)
					continue
				if 'Scan.Stop' in elem[0].text:
					params['scan_stop'] = float(elem[1].text)
					continue
				if 'Scan.step' in elem[0].text:
					params['scan_step'] = float(elem[1].text)
					continue
				if 'offset' in elem[0].text:
					params['offset'] = float(elem[1].text)
					continue
				if 'NSteps' in elem[0].text:
					params['nsteps'] = int(elem[1].text)
					continue
	except:
		traceback.print_exc()

	return params


def graph_df(df: pandas.DataFrame):
	sns.set_theme()
	ax = plt.gca()
	sns.heatmap(df)
	plt.xlabel('$cm^{-1}$')
	plt.tight_layout()
	plt.show()
