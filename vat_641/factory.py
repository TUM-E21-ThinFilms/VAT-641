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

from e21_util.transport import Serial
from e21_util.log import get_sputter_logger
from e21_util.ports import Ports
from protocol import VAT641Protocol
from driver import VAT641Driver

class VAT641Factory:
    def get_logger(self):
        return get_sputter_logger('VAT 64.1 Series', 'vat641.log')

    def create_valve(self, device=None, logger=None):
        if logger is None:
            logger = self.get_logger()

        if device is None:
            device = Ports().get_port(Ports.DEVICE_TURBO_VALVE)

        protocol = VAT641Protocol(logger=logger)
        return VAT641Driver(Serial(device, 4800, 7, 'E', 1, 0.2), protocol)