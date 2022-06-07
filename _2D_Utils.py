import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib
import os
from tkinter import filedialog
from xml.etree import ElementTree as et
import numpy as np
from scipy.signal import find_peaks, medfilt

# Convert nm to cm-1 or vice versa
def nm_cm(to_convert):
	return 10000000 / to_convert

# Opens a filedialog to select the .xml file associated with desired data; returns filepaths of .xml and .txt file
def get_files():
	xml_file = filedialog.askopenfilename(title="Select desired .xml file", filetypes=[("XML", "*.xml")])
	data_file = os.path.splitext(xml_file)[0] + '.txt'
	return xml_file, data_file

# Reterns the XML ElementTree of the given .xml file xml_file
def get_tree(xml_file):
	return et.parse(xml_file)

# Saves an image of the given data with the given data_file path, replacing the extension with .jpg
def save_image(data, scan_start, scan_stop, fluor_min, fluor_max, data_file):
	ax = plt.imshow(data, extent=[scan_start, scan_stop, fluor_min, fluor_max], aspect='auto', cmap='viridis', interpolation='gaussian', vmax=abs(data.max()))
	plt.ylabel(r"Dispersed Fluorescence ($nm$)")
	plt.xlabel(r"LIF ($cm^{-1}$)")
	image_file = os.path.splitext(data_file)[0] + ".jpg"
	plt.savefig(image_file, dpi=1200)

# Displays a heatmap graph of the given data
def show_graph(data, scan_start, scan_stop, fluor_min, fluor_max):
	ax = plt.imshow(data, extent=[scan_start, scan_stop, fluor_min, fluor_max], aspect='auto', cmap='viridis', interpolation='gaussian', vmax=abs(data.max()))
	plt.ylabel(r"Dispersed Fluorescence ($nm$)")
	plt.xlabel(r"LIF ($cm^{-1}$)")
	plt.show()
	return ax

# Returns parameters of scan, assuming xml file was generated using the 2DLIF program; returns in order: scan_start, scan_stop, scan_step, nsteps, offset
def get_params(xml_root):
	return float(xml_root[2][2][1].text), float(xml_root[2][4][1].text), float(xml_root[2][3][1].text), int(xml_root[2][5][1].text), float(xml_root[3][2][1].text)
	
# Calculates the center of the y-axis based on the start position of the scan and the monochromator offset
def get_center(scan_start, offset):
	return nm_cm(scan_start - offset)

# Reads the data in the given file and calculates axes based on steps and fluor_steps; returns transposed data as ndarray
def read_data(data_file):
	data_transposed = np.genfromtxt(data_file).transpose()
	return data_transposed, medfilt(data_transposed)

# Return peaks of given data
def get_peaks(data, _prominence, _width=None):
	return find_peaks(data, prominence=_prominence, width=_width)

# Returns average of DF data within given range. If no range given, returns average of all data (useful for finding all peaks). Assumes data is transposed!
def LIF_slice(data, DF_pts, min=None, max=None):
	if (min != None) & (max != None):
		return data[np.where((DF_pts >= min) & (DF_pts <= max)), :].mean(axis=1).flatten()
	elif (min == None) & (max == None):
		return data[:, :].mean(axis=0).flatten()
	else:
		return None	
	
# Returns average of LIF data within given range. Assumes data is transposed!
def DF_slice(data, LIF_pts, min=None, max=None):
	if (min != None) & (max != None):
		return data[:, np.where((LIF_pts >= min) & (LIF_pts <= max))].mean(axis=2).flatten()
	elif (min == None) & (max == None):
		return data[:, :].mean(axis=1).flatten()
	else:
		return None

# Returns list of all dispersed fluorscence peaks and their corresponding LIF slices
def auto_slice(data, DF_pts, LIF_pts, DF_prominence=500, LIF_prominence=300):
	DF_peaks, DF_properties = get_peaks(DF_slice(data, LIF_pts), DF_prominence, 10)
	LIF_slices = []
	for i in range(0, DF_peaks.size):
		# Note in the line below, minimum is "+" width, maximum is "-" width; higher numbers are higher energy, i.e. smaller wavelength, and the DF_pts are organized small to large wavelength, i.e. high to low energy!
		DF_min = DF_pts[int(round(DF_peaks[i]+DF_properties["widths"][i]/2, 0))]
		DF_max = DF_pts[int(round(DF_peaks[i]-DF_properties["widths"][i]/2, 0))]
		_LIF_slice = LIF_slice(data, DF_pts, DF_min, DF_max)
		peaks = get_peaks(_LIF_slice, LIF_prominence)
		LIF_slices.append((DF_peaks[i], _LIF_slice, peaks, DF_properties["widths"][i]))
	return LIF_slices
