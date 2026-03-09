import serial
import time

class CopleyDrive:
    def __init__(self, port='COM3', baudrate=9600):
        self.ser = serial.Serial(port, baudrate=baudrate, timeout=2)
        time.sleep(0.1)
        self.ser.send_break(duration=0.1)
        time.sleep(0.1)

    def send_command(self, command):
        self.ser.write(f'{command}\r'.encode())
        response = self.ser.readline().decode().strip()
        return response

    def get_parameter(self, param):
        return self.send_command(f'g r{param}')

    def set_parameter(self, param, value):
        return self.send_command(f's r{param} {value}')

    def home(self):
        # From ASCII Command Examples (16-127081rev00)
        drive.set_parameter('0xc8', '0')         # Absolute Move, Trapezoidal Profile
        drive.set_parameter('0x24', '21')        # (?) Drive set in Programmed Position Mode required for homing (?)
        # drive.set_parameter('0xc2', '0x204')   # (?) Homing Method, 0x204 = 516 = Hard Stop Positive BUT this doesn't seem to work with our rotation stage, it keeps turning indefnitely (?)
                                                 # (?) Tried also 514 = Home Switch Positive, but it also doesn't work (?)
        drive.set_parameter('0xc2', '544')       # (?) Homing Method: 544 = Next Index THIS does seem to work with our rotation stage (?)
        drive.set_parameter('0xc3', '0x320000')  # (?) Fast Velocity [0.1 counts/s] or [counts/s], as documented in the examples and Programmer's Guide respectively (?)
        drive.set_parameter('0xc4', '0xa0000')   # (?) Slow Velocity (?)
        drive.set_parameter('0xc5', '0xc0000')   # Acceleration / Deceleration [10 counts/s^2], those units are consistent
        drive.set_parameter('0xc6', '0')         # Home Offset [counts]
        drive.set_parameter('0xc7', '53')        # Current Limit [0.01A], e.g. 53 * 0.01 = 0.53A
        drive.set_parameter('0xbf', '250')       # Current Delay [ms]
        return drive.send_command('t 2')         # Home Command

    def abort_move(self):
        return self.send_command('t 0')

    def move_to_absolute(self, counts):
        drive.set_parameter('0x24', '21')        # (?) Drive operating mode: 21 = Servo mode, the position loop is driven by the trajectory generator, DIFFERENT than for homing? (?)
        drive.set_parameter('0xc8', '0')         # Absolute Move, Trapezoidal Profile
        drive.set_parameter('0xca', str(counts)) # Target Position [counts]
        drive.set_parameter('0xcb', '10000000')  # Maximum Velocity [0.1 counts/s]
        drive.set_parameter('0xcc', '500000')    # Maximum Acceleration [10 counts/s^2]
        drive.set_parameter('0xcd', '500000')    # Maximum Deceleration [10 counts/s^2]
        return drive.send_command('t 1')         # Trajectory Update

    def close(self):
        self.ser.close()

# Usage
drive = CopleyDrive('COM3')
# print(drive.home())
print(drive.move_to_absolute(200000))