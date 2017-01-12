from pymoku import Moku
from pymoku.instruments import *
import time, logging

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s::%(message)s')
logging.getLogger('pymoku').setLevel(logging.DEBUG)

# Use Moku.get_by_serial() or get_by_name() if you don't know the IP

# m = Moku.get_by_name('Oil Rigs')
m = Moku('192.168.69.53')

# i = m.discover_instrument()
# if i is None or i.type != 'netan':
# 	print("No or wrong instrument deployed")
i = NetAn()
m.attach_instrument(i)
# else:
	# print("Attached to existing Spectrum Analyser")

#################################
# BEGIN Instrument Configuration
# ------------------------------
# Set these parameters

i.set_defaults()

f_start = 1e6 # Hz
f_end = 1e8  # Hz
sweep_order = 9
sweep_length = 2**sweep_order
log_scale = False
single_sweep = False
amp_ch1 = 1.0 # Volts peak-to-peak (assuming 50 Ohm impedance)
amp_ch2 = 1.0 # Volts peak-to-peak (assuming 50 Ohm impedance)

averaging_time = 1e-5 # seconds
settling_time = 1e-6 # seconds

averaging_cycles = 500
settling_cycles = 1

i.set_dbscale(False),

i.set_sweep_parameters(f_start, f_end, sweep_length, log_scale, single_sweep, amp_ch1, amp_ch2, averaging_time, settling_time, averaging_cycles, settling_cycles) 

i.set_frontend(1, fiftyr=True, atten=False, ac=False)
i.set_frontend(2, fiftyr=True, atten=True, ac=False)


#################################
# END Instrument Configuration
#################################

i.commit()




# Set up basic plot configurations
line1, = plt.semilogx([])
line2, = plt.semilogx([])
plt.ion()
plt.show()

plt.grid(b=True)

try:
	# Get an initial frame to set any frame-specific plot parameters
	frame = i.get_frame()
	
	print "frame", frame

	# Format the x-axis as a frequency scale 
	ax = plt.gca()
	# ax.xaxis.set_major_formatter(FuncFormatter(frame.get_xaxis_fmt))
	# ax.yaxis.set_major_formatter(FuncFormatter(frame.get_yaxis_fmt))
	# ax.fmt_xdata = frame.get_xcoord_fmt
	# ax.fmt_ydata = frame.get_ycoord_fmt


	# Start drawing new frames
	while True:
		frame = i.get_frame()
		plt.pause(0.001)

		# Set the frame data for each channel plot
		line1.set_ydata(frame.ch1.magnitude)
		line2.set_ydata(frame.ch1.phase)

		print 'Magnitude: ', frame.ch1.magnitude
		print 'Input frame: ', frame.ch1.input
		
		# Frequency axis shouldn't change, but to be sure
		line1.set_xdata(frame.ch1_fs)
		line2.set_xdata(frame.ch2_fs)
		
		print "ch1_axis", frame.ch1_fs
		print "Sweep frequency delta: ", i.get_sweep_freq_delta()
		print "Minimum frequency: ", i.get_sweep_freq_min()
		print "Channel 1 Amplitude: ", i.sweep_amp_volts_ch1
		
		# Ensure the frequency axis is a tight fit
		ax.relim()
		ax.autoscale_view()

		# Redraw the lines
		plt.draw()

finally:
	m.close()