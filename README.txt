Chamber:
	Turn on backing pump.
	Switch on "Rough" and "Foreline" switches.
	Once foreline pressure reaches ~60mtorr, turn off "Rough" switch and turn on "Diff Pump" switches
	Open gates
	
	
Electronics:
	Ensure the SRS and Quantum Composer are turned on.
	If Quantum Composer was off, load applicable timings ("Function"->"Setup", "Next" to select recall, "Up" and "Down" to select configuration, "Function"->"Setup" to recall)
	Press run to start triggers.
		NOTE:
			Channel 1 is Pulse Valve (shouldn't be changed)
			Channel 2 is Ablation relative to Pulse Valve
			Channel 3 is Camera/Boxcar relative to Dye Laser
			Channel 4 is Dye Laser relative to Ablation
	Turn on Pulse Valve driver box
		Small toggle switch is used to control Pulse Valve
			Center: Off
			Up: Internal trigger
			Down: External trigger
	Turn on Boxcar main power
	Turn on Ion Guage
		Standard pressure without gas pulse is low E-5. With gas pulse can be mid E-5 to low E-4
		
		
Computer:
	All programs are on desktop.
	Run: 
		start_motor_controller - Shortcut
			"r" to run motor
			"q" to quite and return motor to home position
			
		YAG_Control.v6.vi - Shortcut
			Start program
			Wait for yellow light on BigSky power supply to stop blinking
			Switch to external
			Turn on Flaslamps
			Let warm up for ~15 mins
			Change power to 1100V (vmo1100)
			Open shutter
			Turn on QSwitch
			
		SpitlightGUI.exe - Shortcut
			Turn laser key
			"Login"->"Priveleged User"
			"File"->"Load User Parameter"
				Load "preferred.ini"
			Apply settings (bottom)
			Trigger tab
				Change to internal
				Apply
			Start laser
			Start pump source
			Change to external trigger
			Apply
			Open shutter when ready
				Make sure motor is running and pulse valve is running
			
	Also run applicable data collection program:
		2D-LIF_CDN.vi - Shortcut
		LIF V3.0 - Shortcut