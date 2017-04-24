# Copyright (C) 2016, see AUTHORS.md
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from slave.driver import Driver, Command
from slave.types import Integer, String, Mapping, BitSequence
from protocol import VAT641Protocol

class VAT641Driver(object):

    VALVE_OPEN = 0
    VALVE_CLOSED = 1
    VALVE_INTERMEDIATE = 2
    VALVE_NOT_CONNECTED = 4

    def __init__(self, transport, protocol=None):

        if protocol is None:
            protocol = VAT641Protocol()

        self._transport = transport
        self._protocol = protocol
        #super(VAT590Driver, self)._init_(transport, protocol)

        self._mode = ('U:', String)

        self._close = ('C:', String)
        self._open = ('O:', String)
        self._hold = ('H:', String)
        self._zero_adjust = ('Z:', String)

        self._interlock = ('U:', String)
        self._speed = ('V:', String)

        self._software_version = Command('i:01', 'i:01', String)

        self._valve_position = Command('A:', 'R:', String)
        self._valve_is_open = ('i:05', String)

    def clear(self):
        self._protocol.clear(self._transport)

    def _query(self, cmd):
        if not isinstance(cmd, Command):
            raise TypeError("Can only query on Command")

        return cmd.query(self._transport, self._protocol)

    def _write(self, cmd, *datas):
        if not isinstance(cmd, Command):
            cmd = Command(write=cmd)

        cmd.write(self._transport, self._protocol, *datas)

    def switch_to_local_mode(self):
        self._write(self._mode, '02')

    def switch_to_remote_mode(self):
        self._write(self._mode, '01')

    def open(self):
        self._write(self._open, '')

    def close(self):
        self._write(self._close, '')

    def set_valve_position(self, position):
        if not isinstance(position, (int, long)):
            raise TypeError("position must be an integer")

        if position < 0 or position > 1000:
            raise ValueError('position must be in range [0, 1000]')

        self._write(self._valve_position, str(position).zfill(6))

    def get_valve_position(self):
        return int(self._query(self._valve_position))

    # returns the valve position in percentage: 100 ^= valve fully open, 0 ^= valve completely closed
    def get_open(self):
        return self.get_valve_position()/10.0

    def is_open(self):
        # format: i:05V1:aV2:b
        query = self._query(self._valve_is_open)
        a = query[7]
        b = query[11]
        if b == "-":
            return self.VALVE_NOT_CONNECTED
        elif a == "N":
            return self.VALVE_INTERMEDIATE
        elif a == "C":
            return self.VALVE_CLOSED
        elif a == "0" or a == "O":
            return self.VALVE_OPEN

    def zero_adjust(self):
        self._write(self._zero_adjust, '')

    def hold(self):
        self._write(self._hold, '')

    def interlock_keys(self):
        self._write(self._interlock, '03')

    def release_keys(self):
        self._write(self._interlock, '04')

    def set_speed(self, speed):
        if not isinstance(speed, (int, long)):
            raise TypeError("position must be an integer")

        if speed < 0 or speed > 1000:
            raise ValueError('position must be in range [0, 1000]')

        self._write(self._speed, str(speed).zfill(6))

    def get_software_version(self):
        return self._query(self._software_version)