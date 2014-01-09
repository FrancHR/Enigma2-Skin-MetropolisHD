#######################################################################
#
#    Renderer for Enigma2
#    Coded by shamann (c)2011
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#######################################################################

from Renderer import Renderer
from enigma import eLabel
from enigma import eDVBVolumecontrol, eTimer
from Components.VariableText import VariableText

class MetVolume(VariableText, Renderer):

	def __init__(self):
		Renderer.__init__(self)
		VariableText.__init__(self)
		self.start = False                     		
		self.vTimer = eTimer()
		self.vTimer.callback.append(self.changed)
	GUI_WIDGET = eLabel

	def changed(self, what=""):
		if self.start:
			self.text = str(eDVBVolumecontrol.getInstance().getVolume()) + "%"

	def onShow(self):
		self.start = True
		self.vTimer.start(200)

	def onHide(self):
		self.start = False
		self.vTimer.stop()		
