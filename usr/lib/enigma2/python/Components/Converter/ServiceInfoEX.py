#2boom (c) 2013
# v.0.4 03.04.13
from Poll import Poll
from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService
from Components.Element import cached

class ServiceInfoEX(Poll, Converter, object):
	apid = 0
	vpid = 1
	sid = 2
	onid = 3
	tsid = 4
	prcpid = 5
	caids = 6
	pmtpid = 7
	txtpid = 8
	xres = 9
	yres = 10
	atype = 11
	vtype = 12
	avtype = 13
	fps = 14
	tbps = 15
	format = 16
	
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		if type == "apid":
			self.type = self.apid
		elif type == "vpid":
			self.type = self.vpid
		elif type == "sid":
			self.type = self.sid
		elif type == "onid":
			self.type = self.onid
		elif type == "tsid":
			self.type = self.tsid
		elif type == "prcpid":
			self.type = self.prcpid
		elif type == "caids":
			self.type = self.caids
		elif type == "pmtpid":
			self.type = self.pmtpid
		elif type == "txtpid":
			self.type = self.txtpid
		elif type == "tsid":
			self.type = self.tsid
		elif type == "xres":
			self.type = self.xres
		elif type == "yres":
			self.type = self.yres
		elif  type == "atype":
			self.type = self.atype
		elif  type == "vtype":
			self.type = self.vtype
		elif  type == "avtype":
			self.type = self.avtype
		elif  type == "fps":
			self.type = self.fps
		elif  type == "tbps":
			self.type = self.tbps
		else: 
			self.type = self.format
			self.sfmt = type[:]
		self.poll_interval = 1000
		self.poll_enabled = True
		
	def getServiceInfoString(self, info, what, convert = lambda x: "%d" % x):
		v = info.getInfo(what)
		if v == -1:
			return "N/A"
		if v == -2:
			return info.getInfoString(what)
		if v == -3:
			t_objs = info.getInfoObject(what)
			if t_objs and (len(t_objs) > 0):
				ret_val=""
				for t_obj in t_objs:
					ret_val += "%.4X " % t_obj
				return ret_val[:-1]
			else:
				return ""
		return convert(v)
		
	@cached
	def getText(self):
		self.stream = { 'apid':"N/A", 'vpid':"N/A", 'sid':"N/A", 'onid':"N/A", 'tsid':"N/A", 'prcpid':"N/A", 'caids':"FTA", 'pmtpid':"N/A", 'txtpid':"N/A", 'xres':"", 'yres':"", 'atype':"", 'vtype':"", 'avtype':"", 'fps':"", 'tbps':"",}
		streaminfo = ""
		service = self.source.service
		info = service and service.info()
		if not info:
			return ""
		if self.getServiceInfoString(info, iServiceInformation.sAudioPID) != "N/A":
			self.stream['apid'] = "%0.4X" % int(self.getServiceInfoString(info, iServiceInformation.sAudioPID))
		if self.getServiceInfoString(info, iServiceInformation.sVideoPID) != "N/A":
			self.stream['vpid'] = "%0.4X" % int(self.getServiceInfoString(info, iServiceInformation.sVideoPID))
		if self.getServiceInfoString(info, iServiceInformation.sSID) != "N/A":
			self.stream['sid'] = "%0.4X" % int(self.getServiceInfoString(info, iServiceInformation.sSID))
		if self.getServiceInfoString(info, iServiceInformation.sONID) != "N/A":
			self.stream['onid'] = "%0.4X" % int(self.getServiceInfoString(info, iServiceInformation.sONID))
		if self.getServiceInfoString(info, iServiceInformation.sTSID) != "N/A":
			self.stream['tsid'] = "%0.4X" % int(self.getServiceInfoString(info, iServiceInformation.sTSID))
		if self.getServiceInfoString(info, iServiceInformation.sPCRPID) != "N/A":
			self.stream['prcpid'] = "%0.4X" % int(self.getServiceInfoString(info, iServiceInformation.sPCRPID))
		if self.getServiceInfoString(info, iServiceInformation.sPMTPID) != "N/A":
			self.stream['pmtpid'] = "%0.4X" % int(self.getServiceInfoString(info, iServiceInformation.sPMTPID))
		if self.getServiceInfoString(info, iServiceInformation.sTXTPID) != "N/A":
			self.stream['txtpid'] = "%0.4X" % int(self.getServiceInfoString(info, iServiceInformation.sTXTPID))
		self.stream['caids'] = self.getServiceInfoString(info, iServiceInformation.sCAIDs)
		if self.getServiceInfoString(info, iServiceInformation.sVideoHeight) != "N/A":
			self.stream['yres'] = self.getServiceInfoString(info, iServiceInformation.sVideoHeight) + ("i", "p", "")[info.getInfo(iServiceInformation.sProgressive)]
		if self.getServiceInfoString(info, iServiceInformation.sVideoWidth) != "N/A":
			self.stream['xres'] = self.getServiceInfoString(info, iServiceInformation.sVideoWidth)
		audio = service.audioTracks()
		if audio:
			if audio.getCurrentTrack() > -1:
				self.stream['atype'] = str(audio.getTrackInfo(audio.getCurrentTrack()).getDescription())
		self.stream['vtype'] = ("MPEG2", "MPEG4", "MPEG1", "MPEG4-II", "VC1", "VC1-SM", "")[info.getInfo(iServiceInformation.sVideoType)]
		self.stream['avtype'] = ("MPEG2/", "MPEG4/", "MPEG1/", "MPEG4-II/", "VC1/", "VC1-SM/", "")[info.getInfo(iServiceInformation.sVideoType)] + self.stream['atype']
		if self.getServiceInfoString(info, iServiceInformation.sFrameRate, lambda x: "%d" % ((x+500)/1000)) != "N/A":
			self.stream['fps'] = self.getServiceInfoString(info, iServiceInformation.sFrameRate, lambda x: "%d" % ((x+500)/1000))
		if self.getServiceInfoString(info, iServiceInformation.sTransferBPS, lambda x: "%d kB/s" % (x/1024)) != "N/A":
			self.stream['tbps'] = self.getServiceInfoString(info, iServiceInformation.sTransferBPS, lambda x: "%d kB/s" % (x/1024))
		
		if self.type == self.apid:
			streaminfo = self.stream['apid']
		elif self.type == self.vpid:
			streaminfo = self.stream['vpid']
		elif self.type == self.sid:
			streaminfo = self.stream['sid']
		elif self.type == self.onid:
			streaminfo = self.stream['onid']
		elif self.type == self.tsid:
			streaminfo = self.stream['tsid']
		elif self.type == self.prcpid:
			streaminfo = self.stream['prcpid']
		elif self.type == self.caids:
			streaminfo = self.stream['caids']
		elif self.type == self.pmtpid:
			streaminfo = self.stream['pmtpid']
		elif self.type == self.txtpid:
			streaminfo = self.stream['txtpid']
		elif self.type == self.tsid:
			streaminfo = self.stream['tsid']
		elif self.type == self.xres:
			streaminfo = self.stream['xres']
		elif self.type == self.yres:
			streaminfo = self.stream['yres']
		elif self.type == self.atype:
			streaminfo = self.stream['atype']
		elif self.type == self.vtype:
			streaminfo = self.stream['vtype']
		elif self.type == self.avtype:
			streaminfo = self.stream['avtype']
		elif self.type == self.fps:
			streaminfo = self.stream['fps']
		elif self.type == self.tbps:
			streaminfo = self.stream['tbps']
		elif self.type == self.format:
			tmp = self.sfmt[:]
			for param in tmp.split():
				if param != '':
					if param[0] != '%':
						streaminfo += param 
					else:
						streaminfo += ' ' + self.stream[param.strip('%')] + '  '
		return streaminfo
		
	text = property(getText)

	def changed(self, what):
		if what[0] == self.CHANGED_SPECIFIC:
			if what[1] == iPlayableService.evStart or what[1] == iPlayableService.evVideoSizeChanged or what[1] == iPlayableService.evUpdatedInfo:
				Converter.changed(self, what)
		elif what[0] != self.CHANGED_SPECIFIC or what[1] in self.interesting_events:
			Converter.changed(self, what)
		elif what[0] == self.CHANGED_POLL:
			self.downstream_elements.changed(what)

