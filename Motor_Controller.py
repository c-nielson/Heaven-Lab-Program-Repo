# NOTE The program is currently set up for the Nema17 motor using a Phidget 1067_0B. Make adjustments accordingly!

# Nema17 information
# 200 steps per rotation
# 1.8 degrees per steps
# 1.2A/phase
# 3.4Ohm/phase
# Needed power: (1.2*2) * (3.4*2+0.5) + 0.5 = 18.02V, 2.4A minimum.
# Max current = 1.2A

import time
from Phidget22.Devices.Stepper import *
from Phidget22.Phidget import *

steps_per_rotation = 200  # Number of rotations per step for the Nema17

rots_per_second = 1 / 16 / steps_per_rotation  # The 1/16 facter is because the default Phidget scale factor is in 1/16 step per second
rots_per_minute = rots_per_second * 60  # Scalling factor for rotations per minute
steps_per_shot = 1 / (
		16 * 20)  # Scaling factor for steps per shot, i.e. how many (full) steps the motor will take for every shot, assuming the system is running at 20Hz

timeout = 0  # Wait for motor to connect; 0 is infinite limit on waiting
target_rpm_scale = 1000  # Limit on how for back the rod should go, scaled in rpm
target_sps_scale = target_rpm_scale / rots_per_minute * steps_per_shot  # Same as above, but scaled to steps per shot

target = target_sps_scale  # Set target
current = 0.8  # Limit current
velocity = 1 / 10  # Velocity to run motor at; with scale set to steps per shot, this would take 1 step every half second

pos_threshold = 0.05  # small factor to allow for motor going slightly past the home or limit position

RUN = True


# Pause motor motion
def pause(ch):
	if not ch.getIsMoving():  # Return if motor is already paused
		return
	ch.setVelocityLimit(0)
	print('Motor paused!\n')


# Resume motor motion
def run(ch):
	# if ch.getIsMoving(): # Return if motor is already moving
	# return
	RUN = True
	ch.setEngaged(True)
	print('Motor running!\n')


# PositionChangedHandler; controls reversal of motor once it has reached the set limits
def onPositionChange(self, position):
	# print(position)
	if abs(position - target) <= pos_threshold and RUN:
		self.setTargetPosition(0)
	if position <= pos_threshold and RUN:
		self.setTargetPosition(target)


# Stops movement and moves motor to zero position, disengaging afterward
def go_home(ch):
	print('Moving to home position; please wait...\n')
	RUN = False
	ch.setVelocityLimit(0)
	tmp = ch.getRescaleFactor()
	ch.setRescaleFactor(rots_per_minute)
	ch.setControlMode(StepperControlMode.CONTROL_MODE_STEP)
	ch.setTargetPosition(0)
	ch.setVelocityLimit(300)
	while ch.getIsMoving():
		time.sleep(0.050)
	ch.setEngaged(False)
	ch.setRescaleFactor(tmp)
	print('Motor parked in home position!\n')


def main():  # TODO: add code to randomize the starting position of the motor on startup; will minimize channeling in the rod
	# List options for commands
	print(
		'''\nThe following commands are available:\n
	\t"r" OR "run" OR "resume":\tBegin motor rotation.\n
	\t"p" OR "pause":\t\t\tPause motor rotation; keeps motor engaged.\n
	\t"q" OR "quit":\t\t\tPositions motor in home position and disengages, exiting the program.\n
	\tKeyboard Interrupt:\t\tSame as "quit".
	'''
	)

	try:
		# Create and attach to Stepper
		ch = Stepper()
		ch.openWaitForAttachment(timeout)

		# Set scale factor
		# ch.setRescaleFactor(rots_per_minute)
		ch.setRescaleFactor(steps_per_shot)

		# Set current limit
		ch.setCurrentLimit(current)

		# Set velocity limit
		ch.setVelocityLimit(velocity)

		# Set PositionChangedHandler
		ch.setOnPositionChangeHandler(onPositionChange)

		# CONTROL_MODE_RUN runs motor at constant velocity
		# ch.setControlMode(StepperControlMode.CONTROL_MODE_RUN)

		# Zero the current position; ideally this should never change, and should be near one extremum of the rod
		ch.addPositionOffset(-ch.getPosition())

		ch.setTargetPosition(target)

		# Listen for keystrokes
		while True:
			try:
				command = input('Command: ')
				if len(command) == 0:
					continue

				match command:
					case 'p' | 'pause':
						pause(ch)
					case 'r' | 'resume' | 'run':
						run(ch)
					case 'q' | 'quit':
						go_home(ch)
						print('Closing program...\n')
						break
					case _:
						print('That is not a command!\n')
						continue

			# NOTE The below code is for versions of Python < 3.10; 3.10 implemented the match case structure above. The following lines are
			# functionally the same
				# if (command == 'p') or (command == 'pause'):
					# pause(ch)  
				# elif (command == 'r') or (command == 'resume') or (command == 'run'):
					# run(ch)
				# elif (command == 'q') or (command == 'quit'):
					# go_home(ch)
					# print('\nClosing program...')
					# break
				# else:
					# print('That is not a command!')
					# continue

			# Interrupt will move the motor back to the zero position and close Phidget tools before exiting
			except KeyboardInterrupt:
				print('\nKeyboard interrupt detected!\n')
				go_home(ch)
				break

		ch.close()
		Phidget.finalize(0)
	except FileNotFoundError:
		print('\nPhidget drivers not found! Please download the appropriate drivers from the Phidget website and try again.\n')

	input('\nExiting...\n')
	sys.exit()


# Run program
main()
