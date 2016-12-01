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
from slave.types import String, Mapping, BitSequence
from protocol import VAT641Protocol

class VAT641Driver(object):

    def __init__(self, transport, protocol=None):

        if protocol is None:
            protocol = VAT641Protocol()

        self._transport = transport
        self._protocol = protocol
        #super(VAT590Driver, self)._init_(transport, protocol)

        self._remote = ('U:01', String)
        self._local = ('U:02', String)

        self._close = ('C:', String)
        self._open = ('O:', String)

        self._valve_position = Command('R:', 'A:', Integer)


        # write only commands
        self._hold = ('H:', String)
        self._reset = ('c:82', String)
        self._close = ('C:', String)
        self._open = ('O:', String)
        self._access_mode = ('c:01', String)

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
        self._write(self._local, '')

    def switch_to_remote_mode(self):
        self._write(self._remote, '')

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
        return self._query(self._valve_position)