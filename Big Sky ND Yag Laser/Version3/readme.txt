YAG_Control.v3 is latest version of BigSky control program structure.
Put active controls in a cluster, to allow updating all with single local variable write; modify those parts as needed in each event case.

Initial values wired as constants before start of event loop; reset on exit.

Have temperature read in the timeout event, and we can set the initial timeout interval shorter than after warmup, so we shouldn't need to read temp in the initialization prior to event loop, as it will happen often enough before timeout slows back down.


7 Jan 2015
back to testing with real YAG P/S.
Implement Cmd-Reply with no termination character checking on read. Reply is always 17 characters; read them all.  No need to do it twice.  Problem with "a" command being ignored first time: no characters to read, second time there are 34.  Need to increase wait from 100ms to 200 ms and this works ok.  Must be longer lag time for response to "a" command.  Even longer delay required for SAV1 command; use 1000 ms for arbitrary command send.  Worst case: repeat command and get double response next time.

Normal operation now: 
Run program
Enable lamps will start firing at default initial voltage and internal rep rate.  
Do this until temperature comes up to >36 C and Yellow Bkg color in Temperature indicator goes white.
To get laser output: open shutter, enable QSw, increase Voltage above threshold to desired power.
Voltage and Rep Rate adjustments will respond as soon as you type in new value or use up/down arrows on control.
Coerced limits set by DataOperations properties for rep rate (1-30 Hz) and lamp voltage (680-860 V).
Status of shutter and Q-Sw updated automatically when lamps are disabled or trigger mode is changed.  
Need to have green status for lamps, shutter, Q-Sw in order to get laser operation.

Red stop in main control cluster to stop laser, make automatic log entry, reset controls to default values.
Stopping program with abort button on execution bar will abort program, but not turn off laser.  
Recommend to use big red rectangular button to stop.  Lamp Standby or Q-Sw standby is fine to pause laser operation without changing any parameters.  Close shutter while running will automatically disable Q-Switch.

If using EXT lamp trigger mode, recommend setting lamps to standby when ext trigger is paused and no lasing is desired, to avoid keeping lamp capacitors charged, awaiting trigger.
