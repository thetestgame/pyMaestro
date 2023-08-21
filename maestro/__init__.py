"""
Copyright (c) Jordan Maxwell. All rights reserved.
See LICENSE file in the project root for full license information.
"""

import serial

# ----------------------------------------------------------------------------------------------- #

class Controller(object):
    """
    """

    def __init__(self, channels: int = 24) -> None:
        """
        """

        self._channel_count = channels # Number of channels pins available to the controller

    @property
    def channel_count(self) -> int:
        """
        Returns the number of channels available to the controller
        """

        return self._channel_count

    def close(self) -> None:
        """
        Closes the serial connection
        """

        raise NotImplementedError()

    def send_command(self, command: str) -> None:
        """
        Sends a command to the controller
        """

        raise NotImplementedError()

    def set_channel_range(self, channel: int, min: int, max: int) -> None:
        """
        Sets the minimum and maximum channel values
        """

        raise NotImplementedError()

    def get_channel_range(self, channel: int) -> tuple:
        """
        Returns the minimum and maximum channel values
        """

        raise NotImplementedError()
    
    def set_target(self, channel: int, position: int) -> None:
        """
        Sets the target position of a channel
        """

        raise NotImplementedError()
    
    def set_speed(self, channel: int, speed: int) -> None:
        """
        """

        raise NotImplementedError()

    def set_acceleration(self, channel: int, acceleration: int) -> None:
        """
        """

        raise NotImplementedError()

    def go_home(self) -> None:
        """
        """

        raise NotImplementedError()
    
    def stop_script(self) -> None:
        """
        """

        raise NotImplementedError()
    
    def restart_script(self) -> None:
        """
        """

        raise NotImplementedError()
    
    def restart_script_with_parameters(self, param: object) -> None:
        """
        """

        raise NotImplementedError()

    def get_position(self, channel: int) -> int:
        """
        Retrieves the position of a channel
        """

        raise NotImplementedError()

    def is_moving(self, channel: int) -> bool:
        """
        """

        raise NotImplementedError()
    
    def get_moving_state(self) -> bool:
        """
        """

        raise NotImplementedError()
        
    def get_errors(self) -> int:
        """
        """

        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------- #

class MaestroController(Controller):
    """
    """

    def __init__(self, com: str = "/dev/ttyACM0", device: int = 0x0c, channels: int = 24) -> None:
        """
        """

        super().__init__(channels)

        self._serial = serial.Serial(com)          # Open the serial port with the Masetro controller
        self._device_cmd = chr(0xaa) + chr(device) # Command lead-in and device number are sent for each serial command

        self._channel_targets = [0] * channels     # Initialize the cahnnel position array

        self._channel_min = [0] * channels         # Minimum channel value
        self._channel_max = [0] * channels         # Maximum channel value

    def close(self) -> None:
        """
        Closes the serial connection
        """

        self._serial.close()

    def send_command(self, command: str) -> None:
        """
        Sends a command to the Maestro
        """

        command_str = self._device_cmd + command
        self._serial.write(bytes(command_str, "latin-1"))

    def set_channel_range(self, channel: int, min: int, max: int) -> None:
        """
        Sets the minimum and maximum channel values
        """

        if channel >= self.channel_count or channel < 0:
            raise ValueError("Channel number out of range")

        self._channel_min[channel] = min
        self._channel_max[channel] = max

    def get_channel_range(self, channel: int) -> tuple:
        """
        Returns the minimum and maximum channel values
        """

        if channel >= self.channel_count or channel < 0:
            raise ValueError("Channel number out of range")

        return (self._channel_min[channel], self._channel_max[channel])
    
    def set_target(self, channel: int, position: int) -> None:
        """
        Sets the target position of a channel
        """

        if channel >= self.channel_count or channel < 0:
            raise ValueError("Channel number out of range")

        if self._channel_max[channel] > 0 and position > self._channel_max[channel]:
            position = self._channel_max[channel]

        if self._channel_min[channel] > 0 and position < self._channel_min[channel]:
            position = self._channel_min[channel]

        lsb = position & 0x7f         # 7 bits for least significant byte
        msb = (position >> 7) & 0x7f  # shift 7 and take next 7 bits for msb
        cmd = chr(0x04) + chr(channel) + chr(lsb) + chr(msb)
        self.send_command(cmd)
        
        # Store our target channel position
        self._channel_targets[channel] = position
    
    def set_speed(self, channel: int, speed: int) -> None:
        """
        """

        if channel >= self.channel_count or channel < 0:
            raise ValueError("Channel number out of range")

        lsb = speed & 0x7f          # 7 bits for least significant byte
        msb = (speed >> 7) & 0x7f   # shift 7 and take next 7 bits for msb
        cmd = chr(0x07) + chr(channel) + chr(lsb) + chr(msb)
        self.send_command(cmd)

    def set_acceleration(self, channel: int, acceleration: int) -> None:
        """
        """

        if channel >= self.channel_count or channel < 0:
            raise ValueError("Channel number out of range")

        lsb = acceleration & 0x7f          # 7 bits for least significant byte
        msb = (acceleration >> 7) & 0x7f   # shift 7 and take next 7 bits for msb
        cmd = chr(0x09) + chr(channel) + chr(lsb) + chr(msb)
        self.send_command(cmd)
    
    def go_home(self) -> None:
        """
        """

        raise NotImplementedError()
    
    def stop_script(self) -> None:
        """
        """

        cmd = chr(0x24)
        self.send_command(cmd)
    
    def restart_script(self) -> None:
        """
        """

        raise NotImplementedError()
    
    def restart_script_with_parameters(self, param: object) -> None:
        """
        """

        raise NotImplementedError()

    def get_position(self, channel: int) -> int:
        """
        Retrieves the position of a channel
        """

        if channel >= self.channel_count or channel < 0:
            raise ValueError("Channel number out of range")

        cmd = chr(0x10) + chr(channel)
        self.send_command(cmd)

        lsb = ord(self._serial.read())
        msb = ord(self._serial.read())
        return (msb << 8) + lsb
    
    def is_moving(self, channel: int) -> bool:
        """
        """

        if channel >= self.channel_count or channel < 0:
            raise ValueError("Channel number out of range")

        if self._channel_targets[channel] > 0:
            if self.get_position(channel) != self._channel_targets[channel]:
                return True
            
        return False
    
    def get_moving_state(self) -> bool:
        """
        """

        cmd = chr(0x13)
        self.send_command(cmd)

        if self.usb.read() == chr(0):
            return False
        else:
            return True
        
    def get_errors(self) -> int:
        """
        """

        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------- #

class MicroMaestroController(MaestroController):
    """
    """

    def __init__(self, comStr: str = "/dev/ttyACM0", device: int = 0x0c) -> None:
        super().__init__(comStr, device, 6)

# ----------------------------------------------------------------------------------------------- #

class MiniMaestroController(MaestroController):
    """
    """

    def __init__(self, comStr: str = "/dev/ttyACM0", device: int = 0x0c, channels: int = 12) -> None:
        assert channels <= 24 and channels >= 12, "Number of channels must be between 12 and 24"
        super().__init__(comStr, device, channels)

    def set_pwm(self) -> None:
        """
        """

        raise NotImplementedError()
    
    def set_multi_target(self) -> None:
        """
        """

        raise NotImplementedError()
    
# ----------------------------------------------------------------------------------------------- #