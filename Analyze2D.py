from Analyze2DHelper import *

if __name__ == '__main__':
	xml_file, txt_file = get_filenames()
	params = get_params(xml_file)
	df = get_df(txt_file, params)
	peaks, peak_params = get_peaks(df)
	graph_2d(df, peaks=peaks)
	peak_df = get_peak_df(df, peaks, peak_params)
	graph_peaks(peak_df)
