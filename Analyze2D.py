from Analyze2DHelper import *

if __name__ == '__main__':
	xml_file, txt_file = get_filenames()
	params = get_params(xml_file)
	df = get_df(txt_file, params)
	peaks, peak_params = get_2d_peaks(df)
	graph_2d(df, peaks=peaks)
	peak_df = get_peak_df(df, peaks, peak_params)
	peaks_1d = get_1d_peaks(peak_df)
	graph_peaks(peak_df, peaks=peaks_1d)
	dump_peak_info('df_dump.csv', 'peak_dump.csv', peak_df, peaks_1d)
	# TODO: Maybe the peak dump isn't needed? It's just indices..
	# print(peak_df.columns[peaks_1d[3][-2]])
