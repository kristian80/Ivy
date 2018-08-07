##########################################################################################################
# PI_Ivy.py by Kristian Ambrosch
# 
# Our new Co-Pilot
#
# before installing pygame:
# sudo pip install -U pip setuptools
#
# then
# pip install pygame
##########################################################################################################
#
# ToDo:
# Bird Strike
# Hello Thunderstorm
# Wrong Barometric Pressure under 3000 Radar --> New Altitude DONE
# Landings on lights above 10000
# Taxi Lights
# Ice Buildup, all kinds of --> Test
# Flaps:
# Adjustment Window, Aircraft INI File
# Gear up and locked, Gear down and locked
# Transponder: I see, we have hot goods on board. You know, if I do not get my fifty percent share upon landing, you might get undesired visitors asking undesired questions.
# Disable until Plugin Enable
# 
# For Custom Jets:
# C300, MD80: V1,VR, V2
# B407, B412, J32, MD80: Heater, Air Conditioning
# 
# 
#
# Disable Errors on higher values DONE
# Disable Plugin until 20s after loading (=after hello) 
# Speak Numbers
# Add number of Errors
# Speak number of Errors after landing DONE
# Speak each class of Error after landing
# Number of Points? Logarithmic Value
# 
# Speak Barometric Pressure
#
# Say Flap Settings:/sim/cockpit1/controls/flap_ratio
# Deactivate on Load
# Aircraft ini File
# Brakes too often
#
##########################################################################################################
#from pygame import mixer



from XPLMDefs import *
from XPLMProcessing import *
from XPLMDisplay import *
from XPLMGraphics import *
from XPLMDataAccess import *
from XPLMUtilities import *
from XPLMPlugin import *
from math import *

import os.path
import random
import time
import ConfigParser
import pygame

class MyIvyAircraft(object):
		
		def __init__(self):
			self.vspeeds_enabled = False
			self.li_v1 = 0
			self.li_vr = 0
			self.li_v2 = 0
			self.name = "Standard"
			pass
		
		
		def UpdateData(self):
			pass
		
class MyIvyCL300(MyIvyAircraft):
		
		def __init__(self):
			self.vspeeds_enabled = True
			self.li_v1 = 0
			self.li_vr = 0
			self.li_v2 = 0
			self.name = "CL300"
			
			self.i_v1 = 				XPLMFindDataRef("cl300/refspds_v1")
			self.i_vr = 				XPLMFindDataRef("cl300/refspds_vr")
			self.i_v2 = 				XPLMFindDataRef("cl300/refspds_v2")
			
			pass
		
		
		def UpdateData(self):
			self.li_v1 = 				XPLMGetDatai(self.i_v1)
			self.li_vr = 				XPLMGetDatai(self.i_vr)
			self.li_v2 = 				XPLMGetDatai(self.i_v2)
			pass		


class MyIvyConfiguration(object):
		
		def __init__(self):
		
			self.mp3_path 					= XPLMGetSystemPath() + "\\Resources\\plugins\\PythonScripts\\IvyMP3s\\"
			self.number_path 				= self.mp3_path + "numbers\\"
			self.ini_path 					= XPLMGetSystemPath() + "\\Resources\\plugins\\PythonScripts\\Ivy.ini"
		
			self.data_rate 					= 0.1
			self.disable_after_loading 		= 20
			self.deact_after_queue 			= 2
		
			self.pos_rate_climb 			= 100
			self.ivy_ouch_g 				= 1.5
			self.brake_max_forward_g 		= 0.5
			self.alt_landing_lights_low 	= 1000
			self.alt_landing_lights_high 	= 10000
			self.night_world_light_precent 	= 0.5
			self.taxi_ground_speed_min 		= 5
			self.vis_is_fog 				= 5000
			self.cab_rate_low 				= -1500
			self.cab_rate_high 				= -2500
			self.cab_rate_reset_hysteresis 	= 500
			
			self.bank_reset_low 			= 15
			self.bank_low 					= 28
			self.bank_high 					= 35
			self.bank_xhigh 				= 45
			
			self.pitch_reset_low 			= -5
			self.pitch_low 					= -10
			self.pitch_high 				= -20
			
			self.max_g_down_low_reset 		= 1.5
			self.max_g_down_low 			= 2
			self.max_g_down_high 			= 3
			self.max_g_down_xhigh 			= 5
			
			
			self.trans_alt 					= 18000
			self.trans_hysteresis 			= 1000
			self.baro_tolerance 			= 3
			self.baro_alt_low 				= 3000
			
			self.ice_low 					= 0.05
			self.ice_high 					= 0.2
			
			self.cab_press_low 				= 13000
			self.cab_press_high 			= 20000
			
			
		pass
		
		def WriteConfig(self):
			pass
			config = ConfigParser.SafeConfigParser()
			
			config.add_section("IVY_SETTINGS")
			config.set("IVY_SETTINGS","pos_rate_climb",str(self.pos_rate_climb))
			config.set("IVY_SETTINGS","ivy_ouch_g",str(self.ivy_ouch_g))
			config.set("IVY_SETTINGS","brake_max_forward_g",str(self.brake_max_forward_g))
			config.set("IVY_SETTINGS","alt_landing_lights_low",str(self.alt_landing_lights_low))
			config.set("IVY_SETTINGS","alt_landing_lights_high",str(self.alt_landing_lights_high))
			config.set("IVY_SETTINGS","night_world_light_precent",str(self.night_world_light_precent))
			config.set("IVY_SETTINGS","taxi_ground_speed_min",str(self.taxi_ground_speed_min))
			config.set("IVY_SETTINGS","vis_is_fog",str(self.vis_is_fog))
			config.set("IVY_SETTINGS","cab_rate_low",str(self.cab_rate_low))
			config.set("IVY_SETTINGS","cab_rate_high",str(self.cab_rate_high))
			config.set("IVY_SETTINGS","cab_rate_reset_hysteresis",str(self.cab_rate_reset_hysteresis))
			config.set("IVY_SETTINGS","bank_reset_low",str(self.bank_reset_low))
			config.set("IVY_SETTINGS","bank_low",str(self.bank_low))
			config.set("IVY_SETTINGS","bank_high",str(self.bank_high))
			config.set("IVY_SETTINGS","bank_xhigh",str(self.bank_xhigh))
			config.set("IVY_SETTINGS","pitch_reset_low",str(self.pitch_reset_low))
			config.set("IVY_SETTINGS","pitch_low",str(self.pitch_low))
			config.set("IVY_SETTINGS","pitch_high",str(self.pitch_high))
			config.set("IVY_SETTINGS","max_g_down_low_reset",str(self.max_g_down_low_reset))
			config.set("IVY_SETTINGS","max_g_down_low",str(self.max_g_down_low))
			config.set("IVY_SETTINGS","max_g_down_high",str(self.max_g_down_high))
			config.set("IVY_SETTINGS","max_g_down_xhigh",str(self.max_g_down_xhigh))
			config.set("IVY_SETTINGS","trans_alt",str(self.trans_alt))
			config.set("IVY_SETTINGS","trans_hysteresis",str(self.trans_hysteresis))
			config.set("IVY_SETTINGS","baro_tolerance",str(self.baro_tolerance))
			config.set("IVY_SETTINGS","baro_alt_low",str(self.baro_alt_low))
			config.set("IVY_SETTINGS","ice_low",str(self.ice_low))
			config.set("IVY_SETTINGS","ice_high",str(self.ice_high))
			config.set("IVY_SETTINGS","cab_press_low",str(self.cab_press_low))
			config.set("IVY_SETTINGS","cab_press_high",str(self.cab_press_high))
			
			with open(self.ini_path , 'wb') as configfile: config.write(configfile)
				

		
		def ReadConfig(self):
			pass
			config = ConfigParser.SafeConfigParser()
			config.read(self.ini_path)
			
			try:	self.pos_rate_climb 			= config.getfloat("IVY_SETTINGS","pos_rate_climb")
			except:	pass
			try:	self.ivy_ouch_g 				= config.getfloat("IVY_SETTINGS","ivy_ouch_g")
			except:	pass
			try:	self.brake_max_forward_g 		= config.getfloat("IVY_SETTINGS","brake_max_forward_g")
			except:	pass
			try:	self.alt_landing_lights_low 	= config.getfloat("IVY_SETTINGS","alt_landing_lights_low")
			except:	pass
			try:	self.alt_landing_lights_high 	= config.getfloat("IVY_SETTINGS","alt_landing_lights_high")
			except:	pass
			try:	self.night_world_light_precent 	= config.getfloat("IVY_SETTINGS","night_world_light_precent")
			except:	pass
			try:	self.taxi_ground_speed_min 		= config.getfloat("IVY_SETTINGS","taxi_ground_speed_min")
			except:	pass
			try:	self.vis_is_fog 				= config.getfloat("IVY_SETTINGS","vis_is_fog")
			except:	pass
			try:	self.cab_rate_low 				= config.getfloat("IVY_SETTINGS","cab_rate_low")
			except:	pass
			try:	self.cab_rate_high 				= config.getfloat("IVY_SETTINGS","cab_rate_high")
			except:	pass
			try:	self.cab_rate_reset_hysteresis 	= config.getfloat("IVY_SETTINGS","cab_rate_reset_hysteresis")
			except:	pass
			
			try:	self.bank_reset_low 			= config.getfloat("IVY_SETTINGS","bank_reset_low")
			except:	pass
			try:	self.bank_low 					= config.getfloat("IVY_SETTINGS","bank_low")
			except:	pass
			try:	self.bank_high 					= config.getfloat("IVY_SETTINGS","bank_high")
			except:	pass
			try:	self.bank_xhigh 				= config.getfloat("IVY_SETTINGS","bank_xhigh")
			except:	pass
			
			try:	self.pitch_reset_low 			= config.getfloat("IVY_SETTINGS","pitch_reset_low")
			except:	pass
			try:	self.pitch_low 					= config.getfloat("IVY_SETTINGS","pitch_low")
			except:	pass
			try:	self.pitch_high 				= config.getfloat("IVY_SETTINGS","pitch_high")
			except:	pass
			
			try:	self.max_g_down_low_reset 		= config.getfloat("IVY_SETTINGS","max_g_down_low_reset")
			except:	pass
			try:	self.max_g_down_low 			= config.getfloat("IVY_SETTINGS","max_g_down_low")
			except:	pass
			try:	self.max_g_down_high 			= config.getfloat("IVY_SETTINGS","max_g_down_high")
			except:	pass
			try:	self.max_g_down_xhigh 			= config.getfloat("IVY_SETTINGS","max_g_down_xhigh")
			except:	pass
			
			
			try:	self.trans_alt 					= config.getfloat("IVY_SETTINGS","trans_alt")
			except:	pass
			try:	self.trans_hysteresis 			= config.getfloat("IVY_SETTINGS","trans_hysteresis")
			except:	pass
			try:	self.baro_tolerance 			= config.getfloat("IVY_SETTINGS","baro_tolerance")
			except:	pass
			try:	self.baro_alt_low 				= config.getfloat("IVY_SETTINGS","baro_alt_low")
			except:	pass
			
			try:	self.ice_low 					= config.getfloat("IVY_SETTINGS","ice_low")
			except:	pass
			try:	self.ice_high 					= config.getfloat("IVY_SETTINGS","ice_high")
			except:	pass
			
			try:	self.cab_press_low 				= config.getfloat("IVY_SETTINGS","cab_press_low")
			except:	pass
			try:	self.cab_press_high 			= config.getfloat("IVY_SETTINGS","cab_press_high")
			except:	pass
			
			
			
			
			
			
			

class MyIvyResponse(object):
	def __init__(self, event_name,mp3_path, active_on_load, minimum_occ,deactivate_time, is_error, ivy_object_list):
	
		self.queue_output = 0
		self.event_name = event_name
		self.is_error = is_error
		self.minimum_occ = minimum_occ
		self.deactivating = 0
		self.deactivate_time = deactivate_time
		self.time_activated = 0
		self.time_deactivated = 0
		self.time_deactivating = 0
		self.time_active = 0
		self.active = active_on_load
		self.played = active_on_load
		self.active_on_load = active_on_load
		self.mute = 0
		self.error_count = 0
		
		self.play_files = []
		
		ivy_object_list.append(self)
		
		#Append all file names that match our event
		for file_number in range(1,11):
			if (os.path.isfile(mp3_path + event_name + "_" + str(file_number) + ".mp3")):
				self.play_files.append(mp3_path + event_name + "_" + str(file_number) + ".mp3")
		pass

	def Activate(self, time):
		if (self.active == 0): 
			self.time_activated = time
		
		self.active = 1
		
		self.time_active = time - self.time_activated
		
		if ((self.time_active >= self.minimum_occ) and (self.played == 0)):
			self.Play()
		pass
		
	def SetAsPlayed(self, time):
		self.active = 1
		self.played = 1
		self.time_activated = time
		pass
		
	def Deactivate(self, time):
		if (self.active == 0): 
			return
		
		if (self.deactivating == 0):
			self.time_deactivated = time
		
		self.deactivating = 1
		self.time_deactivating = time - self.time_deactivated
		
		if (self.time_deactivating >= self.deactivate_time):
			self.deactivating = 0
			self.time_deactivated = 0
			self.active = 0
			self.time_activated = 0
			self.time_active = 0
			self.played = 0
		pass
		
		
	def Play(self):
		if (len(self.play_files) == 0):
			return 0

		if ((self.queue_output == 0) and (pygame.mixer.music.get_busy() == True)):
			return 0
		
		if (self.played == 1):
			return 0 
		
		if (self.is_error > 0): 
			self.error_count = self.error_count + 1
		
		if (len(self.play_files) > 1):	
			random_number = random.randint(0,len(self.play_files)-1)
		else:
			random_number = 0
		
		self.played = 1
		
		if (self.queue_output == 1):
			pygame.mixer.music.queue(self.play_files[random_number])
		else:
			pygame.mixer.music.load(self.play_files[random_number])
			pygame.mixer.music.play()
		return 1

class IvyLandingDetection(object):
	def __init__(self, time, sink_rate, g_normal, g_side, g_forward):
		self.time = time
		self.sink_rate = sink_rate
		self.g_normal = g_normal
		self.g_side = g_side
		self.g_forward = g_forward
		self.rating = 0
		self.RateLanding()
		pass
		
	def RateLanding(self):
		if ((self.sink_rate > -100) and (self.g_normal < 1.3)):	self.rating = 1
		elif (self.sink_rate > -250) and (self.g_normal < 1.5):	self.rating = 2
		elif (self.sink_rate > -500) and (self.g_normal < 2):		self.rating = 3
		else:														self.rating = 4
		pass
		
	def GetCurrentRate(self, last_landing_time, max_time):
		if ((last_landing_time - self.time) < max_time):
			return self.rating
		else:
			return 0
		
		
class PythonInterface:

	def ResetIvy(self):
		self.time = 0
		self.landing_detected = 0
		self.landing_rated = 0
		self.aircraft_crashed = 0
		self.pressure_said = 0
		self.play_mp3_queue = []
		
		
		
		
		
		for obj_number in range(0,len(self.ivy_object_list)):
			self.ivy_object_list[obj_number].error_count = 0
			self.ivy_object_list[obj_number].active = self.ivy_object_list[obj_number].active_on_load
			self.ivy_object_list[obj_number].played = self.ivy_object_list[obj_number].active_on_load
		
		lba_acf_descrip= []

		XPLMGetDatab(self.s_acf_descrip,lba_acf_descrip,0,240) 	
		self.ls_acf_descrip = str(lba_acf_descrip)
		
		if (self.ls_acf_descrip == "['Bombardier Challenger 300 XP11']"):
			self.ivyAircraft = MyIvyCL300()
		else:
			self.ivyAircraft = MyIvyAircraft()
		
		
		pass
		
		
	
	def XPluginStart(self):

		self.Name = "Ivy"
		self.Sig =  "ka.Python.Ivy"
		self.Desc = "My nuding Co-Pilot"
		
		

		self.play_mp3_queue = []
		self.ivy_object_list = []
		self.ivy_landing_list = []
		
		self.ivyAircraft = MyIvyAircraft()
		
		self.aircraft_loaded = 0
		self.plugin_enabled = 0
		self.deact_queue = 0
		
		self.ivyConfig = MyIvyConfiguration()
		self.ivyConfig.ReadConfig()
		
		
		
		#self.startup = 1
		
		self.s_acf_descrip = 			XPLMFindDataRef("sim/aircraft/view/acf_descrip") 
		self.ResetIvy()
		#self.Clicked = 0
		
		self.outputPath = XPLMGetSystemPath() + "\\Resources\\plugins\\PythonScripts\\IvyLog.txt"
		self.OutputFile = open(self.outputPath, 'w')
		
		# Init the pygame mixer
		pygame.mixer.init()
		random.seed()
		
		#self.END_MUSIC_EVENT = pygame.USEREVENT + 0    # ID for music Event
		#pygame.mixer.music.set_endevent(END_MUSIC_EVENT)
		
		#												#Name						PATH						DEACT_ON_LOAD		MINIMUM_OCC_TIME		DEACT_TIME				IS_ERROR			IVY_OBJECT_LIST
		self.ivyOuch = 					MyIvyResponse(	"ouch", 					self.ivyConfig.mp3_path,	0,				0, 						0, 						0,					self.ivy_object_list)
		self.ivyPosRateClimb = 			MyIvyResponse(	"pos_climb", 				self.ivyConfig.mp3_path,	0,				3, 						5, 						0,					self.ivy_object_list)
		self.ivyTyre = 					MyIvyResponse(	"tyre", 					self.ivyConfig.mp3_path,	0,				0, 						0, 						1,					self.ivy_object_list)
		self.ivyBrake = 				MyIvyResponse(	"brake", 					self.ivyConfig.mp3_path,	0,				3, 						10,						1,					self.ivy_object_list)
		self.ivyTransponder = 			MyIvyResponse(	"transponder", 				self.ivyConfig.mp3_path,	0,				120, 					0, 						1,					self.ivy_object_list)
		self.ivyCockpitLights = 		MyIvyResponse(	"cockpit_lights", 			self.ivyConfig.mp3_path,	0,				5, 						0, 						1,					self.ivy_object_list)
		self.ivyLandingLights = 		MyIvyResponse(	"landing_lights", 			self.ivyConfig.mp3_path,	0,				0, 						0, 						1,					self.ivy_object_list)
		
		self.ivyGearUp = 				MyIvyResponse(	"gear_up", 					self.ivyConfig.mp3_path,	1,				1, 						0, 						0,					self.ivy_object_list)
		self.ivyGearDown = 				MyIvyResponse(	"gear_down", 				self.ivyConfig.mp3_path,	1,				1, 						0, 						0,					self.ivy_object_list)
		
		self.ivyBeaconLights = 			MyIvyResponse(	"beacon", 					self.ivyConfig.mp3_path,	0,				20, 					0, 						1,					self.ivy_object_list)
		self.ivyNavLights = 			MyIvyResponse(	"nav_lights", 				self.ivyConfig.mp3_path,	0,				50, 					0, 						1,					self.ivy_object_list)
		self.ivyStrobes = 				MyIvyResponse(	"strobes", 					self.ivyConfig.mp3_path,	0,				200, 					0, 						1,					self.ivy_object_list)
		self.ivySkidTyres = 			MyIvyResponse(	"skid_tyres", 				self.ivyConfig.mp3_path,	0,				5, 						0, 						0,					self.ivy_object_list)
		self.ivyBatteryOut = 			MyIvyResponse(	"battery_out", 				self.ivyConfig.mp3_path,	0,				0, 						0, 						1,					self.ivy_object_list)
		self.ivyEngineFire = 			MyIvyResponse(	"engine_fire", 				self.ivyConfig.mp3_path,	0,				0, 						0, 						1,					self.ivy_object_list)
		self.ivyEngineFlameout = 		MyIvyResponse(	"engine_flameout", 			self.ivyConfig.mp3_path,	0,				0, 						0, 						1,					self.ivy_object_list)
		self.ivyEngineFailureGround = 	MyIvyResponse(	"engine_failure_ground", 	self.ivyConfig.mp3_path,	0,				0, 						0, 						1,					self.ivy_object_list)
		self.ivyEngineFailureAir = 		MyIvyResponse(	"engine_failure_air", 		self.ivyConfig.mp3_path,	0,				0, 						0, 						1,					self.ivy_object_list)
		self.ivyEngineHotStart = 		MyIvyResponse(	"engine_hot", 				self.ivyConfig.mp3_path,	0,				0, 						0, 						1,					self.ivy_object_list)
		
		self.ivyNoBatt = 				MyIvyResponse(	"no_batt", 					self.ivyConfig.mp3_path,	0,				180, 					0, 						0,					self.ivy_object_list)
		self.ivyHelloSun = 				MyIvyResponse(	"hello_sun", 				self.ivyConfig.mp3_path,	0,				15, 					0, 						0,					self.ivy_object_list)
		self.ivyHelloRain = 			MyIvyResponse(	"hello_rain", 				self.ivyConfig.mp3_path,	0,				15, 					0, 						0,					self.ivy_object_list)
		self.ivyHelloFog = 				MyIvyResponse(	"hello_fog", 				self.ivyConfig.mp3_path,	0,				15, 					0, 						0,					self.ivy_object_list)
		self.ivyHelloNormal = 			MyIvyResponse(	"hello_normal", 			self.ivyConfig.mp3_path,	0,				15, 					0, 						0,					self.ivy_object_list)
		self.ivyCabinDownNormal = 		MyIvyResponse(	"cabin_down_normal", 		self.ivyConfig.mp3_path,	0,				15, 					0, 						1,					self.ivy_object_list)
		self.ivyCabinDownFast = 		MyIvyResponse(	"cabin_down_fast", 			self.ivyConfig.mp3_path,	0,				5, 						0, 						1,					self.ivy_object_list)
		self.ivyBankNormal = 			MyIvyResponse(	"bank_normal", 				self.ivyConfig.mp3_path,	0,				0, 						0, 						0,					self.ivy_object_list)
		self.ivyBankHigh = 				MyIvyResponse(	"bank_high", 				self.ivyConfig.mp3_path,	0,				2, 						0, 						1,					self.ivy_object_list)
		self.ivyBankXHigh = 			MyIvyResponse(	"bank_xhigh", 				self.ivyConfig.mp3_path,	0,				2, 						0, 						1,					self.ivy_object_list)
		self.ivyPitchDownNormal = 		MyIvyResponse(	"pitch_down_normal", 		self.ivyConfig.mp3_path,	0,				0, 						0, 						0,					self.ivy_object_list)
		self.ivyPitchDownHigh = 		MyIvyResponse(	"pitch_down_high", 			self.ivyConfig.mp3_path,	0,				2, 						0, 						1,					self.ivy_object_list)
		self.ivyGNormalFlightNormal = 	MyIvyResponse(	"g_normal_flight_normal", 	self.ivyConfig.mp3_path,	0,				2, 						0, 						0,					self.ivy_object_list)
		self.ivyGNormalFlightHigh = 	MyIvyResponse(	"g_normal_flight_high", 	self.ivyConfig.mp3_path,	0,				2, 						0, 						1,					self.ivy_object_list)
		self.ivyGNormalFlightXHigh = 	MyIvyResponse(	"g_normal_flight_xhigh", 	self.ivyConfig.mp3_path,	0,				2, 						0, 						1,					self.ivy_object_list)
		self.ivyTurbulenceNormal = 		MyIvyResponse(	"turbulence_normal", 		self.ivyConfig.mp3_path,	0,				20, 					0, 						0,					self.ivy_object_list)
		self.ivyTurbolenceHigh = 		MyIvyResponse(	"turbulence_high", 			self.ivyConfig.mp3_path,	0,				20, 					0, 						0,					self.ivy_object_list)
		self.ivyLandingXGood = 			MyIvyResponse(	"landing_xgood", 			self.ivyConfig.mp3_path,	0,				5, 						0, 						0,					self.ivy_object_list)
		self.ivyLandingGood = 			MyIvyResponse(	"landing_good", 			self.ivyConfig.mp3_path,	0,				5, 						0, 						0,					self.ivy_object_list)
		self.ivyLandingNormal = 		MyIvyResponse(	"landing_normal", 			self.ivyConfig.mp3_path,	0,				5, 						0, 						0,					self.ivy_object_list) # TODO
		self.ivyLandingBad = 			MyIvyResponse(	"landing_bad", 				self.ivyConfig.mp3_path,	0,				5, 						1, 						0,					self.ivy_object_list)
		self.ivyLandingXBad = 			MyIvyResponse(	"landing_xbad", 			self.ivyConfig.mp3_path,	0,				5, 						1, 						0,					self.ivy_object_list)
		self.ivyBaroLow = 				MyIvyResponse(	"baro_low", 				self.ivyConfig.mp3_path,	0,				5, 						0, 						1,					self.ivy_object_list)
		self.ivyBaroGround = 			MyIvyResponse(	"baro_low", 				self.ivyConfig.mp3_path,	0,				5, 						0, 						1,					self.ivy_object_list)
		self.ivyBaroHigh = 				MyIvyResponse(	"baro_high", 				self.ivyConfig.mp3_path,	0,				5, 						0, 						1,					self.ivy_object_list)
		self.ivyLandingLightsHigh = 	MyIvyResponse(	"landing_lights_high", 		self.ivyConfig.mp3_path,	0,				5, 						0, 						1,					self.ivy_object_list)
		self.ivyRotate = 				MyIvyResponse(	"rotate", 					self.ivyConfig.mp3_path,	0,				0, 						0, 						0,					self.ivy_object_list)
		self.ivy60kt = 					MyIvyResponse(	"60kt", 					self.ivyConfig.mp3_path,	0,				0, 						0, 						0,					self.ivy_object_list)
		self.ivyV1 = 					MyIvyResponse(	"v1", 						self.ivyConfig.mp3_path,	0,				0, 						5, 						0,					self.ivy_object_list)
		self.ivyVR = 					MyIvyResponse(	"vr", 						self.ivyConfig.mp3_path,	0,				0, 						5, 						0,					self.ivy_object_list)
		self.ivyV2 = 					MyIvyResponse(	"v2", 						self.ivyConfig.mp3_path,	0,				0, 						5, 						0,					self.ivy_object_list)
		self.ivyCrash = 				MyIvyResponse(	"crash", 					self.ivyConfig.mp3_path,	0,				3, 						0, 						1,					self.ivy_object_list)
		# TODO
		
		self.ivyPressureLow = 			MyIvyResponse(	"pressure_low", 			self.ivyConfig.mp3_path,	0,				5, 						0, 						1,					self.ivy_object_list)
		self.ivyPressureXLow = 			MyIvyResponse(	"pressure_xlow", 			self.ivyConfig.mp3_path,	0,				1, 						0, 						1,					self.ivy_object_list)
		
		self.ivyIceWindowLow = 			MyIvyResponse(	"ice_window_low", 			self.ivyConfig.mp3_path,	0,				5, 						0, 						1,					self.ivy_object_list)
		self.ivyIceWindowHigh = 		MyIvyResponse(	"ice_window_high", 			self.ivyConfig.mp3_path,	0,				5, 						0, 						1,					self.ivy_object_list)
		self.ivyIcePropellerLow = 		MyIvyResponse(	"ice_propeller_low", 		self.ivyConfig.mp3_path,	0,				5, 						0, 						1,					self.ivy_object_list) # Inlet ice
		self.ivyIcePropellerHigh = 		MyIvyResponse(	"ice_propeller_high", 		self.ivyConfig.mp3_path,	0,				5, 						0, 						1,					self.ivy_object_list)
		self.ivyIcePitotLow = 			MyIvyResponse(	"ice_pitot_low", 			self.ivyConfig.mp3_path,	0,				5, 						0, 						1,					self.ivy_object_list) # Ice low bei 0.05
		self.ivyIcePitotHigh = 			MyIvyResponse(	"ice_pitot_high", 			self.ivyConfig.mp3_path,	0,				5, 						0, 						1,					self.ivy_object_list)
		self.ivyIceAirframeLow = 		MyIvyResponse(	"ice_airframe_low", 		self.ivyConfig.mp3_path,	0,				5, 						0, 						1,					self.ivy_object_list) # Ice high bei 0.15
		self.ivyIceAirframeHigh = 		MyIvyResponse(	"ice_airframe_high", 		self.ivyConfig.mp3_path,	0,				5, 						0, 						1,					self.ivy_object_list)
			
	
		#self.ivy = 		MyIvyResponse(	"landing_lights", 		self.ivyConfig.mp3_path,	0,			0, 						0, 						0,					self.ivy_object_list)


		self.f_g_normal_max = 1
		self.f_g_side_max = 0
		self.f_g_forward_max = 0
		
		self.f_g_normal_min = 1
		self.f_g_side_min = 0
		self.f_g_forward_min = 0
		
		self.f_g_normal_delta = 0
		self.f_g_side_delta = 0
		self.f_g_forward_delta = 0
		
		self.f_g_normal_old = 1
		self.f_g_side_old = 0
		self.f_g_forward_old = 0

		self.li_on_ground_old = 1
		#self.Clicked = 0
		
		self.show_output = 1
		
		
		
		
		##################################### DEBUG
		for obj_number in range(0,len(self.ivy_object_list)):
			buf = "IvyObject: " + self.ivy_object_list[obj_number].event_name + " Number of Soundfiles: " + str(len(self.ivy_object_list[obj_number].play_files)) + "\n\r"
			self.OutputFile.write(buf)
		self.OutputFile.flush()
		##################################### END DEBUG
		
		##########################################################################################
		# Register Flight Callback
		
		self.FlightLoopCB = self.FlightLoopCallback
		
		XPLMRegisterFlightLoopCallback(self, self.FlightLoopCB, self.ivyConfig.data_rate, 0)                #DEBUG
		
		##########################################################################################
		# Register Command Callbacks
		
		self.SayBaroCB 				= self.SayBaroCallback
		self.ResetIvyCB 			= self.ResetIvyCallback
		
		self.CmdSayBaro 			= XPLMCreateCommand ( "Ivy/say_baro" 	, "Ask Ivy to tell you the barometric pressure" )
		self.CmdResetIvy 			= XPLMCreateCommand ( "Ivy/reset_ivy" 	, "Reset Ivy" )
		
		XPLMRegisterCommandHandler 	( self , 	self.CmdSayBaro , 	self.SayBaroCB 	, 0 , 0 )            #DEBUG
		XPLMRegisterCommandHandler 	( self , 	self.CmdResetIvy , 	self.ResetIvyCB , 0 , 0 )            #DEBUG
		
		##########################################################################################
		#
		# Welcome
		# Engine started
		# 
		# 60 knots
		#
		# After 5: Battery on?
		# Night: Cockpit lights after 1min
		# Night and Taxi: No Taxi lights, beacon off
		# Flying and Night: Nav, Strobe
		# Flying, Night and below 1000ft, after >5000: Landing lights
		# Engines > 80, No Flaps: Not ready for departure (2nd 3rd time)
		# First Takeoff, Climb rate >500ft/min: Positive rate of climb
		#
		# Cabin pressure: 10.000ft, 20.000ft, 30.000ft
		# Cabin pressure change rate: 1000ft/min, 2000ft/min 5000ft/min (down)
		# Bank angle
		# Roll detection
		# Pitch angle
		# Looping detection
		# Gforce normal
		# Side forces
		# Frontal forces
		# Outside Temp + Heater
		# Outside Temp + Air cond
		#
		# Landing:
		# ft/min
		# g_forward
		# 60 
		#
		# Failures:
		# 
		# Tire blown
		# Ice Buildup
		# Engine fire
		# Engine flameout1
		# Engine hot started
		# Engine outside
		# Battery out
		# 
		#########################################################################################
		#
		#						DATAREF Find
		#
		#########################################################################################
		
		
		
		self.i_on_ground = 				XPLMFindDataRef("sim/flightmodel/failures/onground_any")
		self.f_climb_rate = 			XPLMFindDataRef("sim/flightmodel/position/vh_ind_fpm")
		self.f_gear_ratio = 			XPLMFindDataRef("sim/flightmodel/movingparts/gear1def")
		self.f_ground_speed = 			XPLMFindDataRef("sim/flightmodel/position/groundspeed")
		self.f_ias = 					XPLMFindDataRef("sim/flightmodel/position/indicated_airspeed")
		self.f_sun_pitch = 				XPLMFindDataRef("sim/graphics/scenery/sun_pitch_degrees")
		self.f_airport_light = 			XPLMFindDataRef("sim/graphics/scenery/airport_light_level") #0-1
		self.f_world_light_precent = 	XPLMFindDataRef("sim/graphics/scenery/percent_lights_on")
		self.i_has_skid = 				XPLMFindDataRef("sim/aircraft/gear/acf_gear_is_skid")
		self.i_transponder_mode = 		XPLMFindDataRef("sim/cockpit/radios/transponder_mode") # on = 3
		
		self.i_temp_sl = 				XPLMFindDataRef("sim/weather/temperature_sealevel_c") # Td ~ T - (100-RH)/5 where Td is the dew point, T is temperature, RH is relative humidity
		self.i_dew_sl = 				XPLMFindDataRef("sim/weather/dewpoi_sealevel_c")
		
		self.i_landing_lights = 		XPLMFindDataRef("sim/cockpit/electrical/landing_lights_on")
		self.i_beacon_lights = 			XPLMFindDataRef("sim/cockpit/electrical/beacon_lights_on")
		self.i_nav_lights = 			XPLMFindDataRef("sim/cockpit/electrical/nav_lights_on")
		self.i_strobe_lights = 			XPLMFindDataRef("sim/cockpit/electrical/strobe_lights_on")
		self.i_taxi_lights = 			XPLMFindDataRef("sim/cockpit/electrical/taxi_light_on")
		self.i_cockpit_lights = 		XPLMFindDataRef("sim/cockpit/electrical/cockpit_lights_on")
		self.f_radio_alt = 				XPLMFindDataRef("sim/cockpit2/gauges/indicators/radio_altimeter_height_ft_pilot")
		self.f8_batter_charge = 		XPLMFindDataRef("sim/cockpit/electrical/battery_charge_watt_hr")
		self.i_battery_on = 			XPLMFindDataRef("sim/cockpit/electrical/battery_on")
		self.i_gpu_on = 				XPLMFindDataRef("sim/cockpit/electrical/gpu_on")
		
		self.i_cloud_0 = 				XPLMFindDataRef("sim/weather/cloud_type[0]")
		self.i_cloud_1 = 				XPLMFindDataRef("sim/weather/cloud_type[0]")
		self.i_cloud_2 = 				XPLMFindDataRef("sim/weather/cloud_type[0]")
		self.f_visibility = 			XPLMFindDataRef("sim/weather/visibility_reported_m")
		self.i_rain = 					XPLMFindDataRef("sim/weather/rain_percent")
		self.i_thunder = 				XPLMFindDataRef("sim/weather/thunderstorm_percent")
		self.i_turbulence = 			XPLMFindDataRef("sim/weather/wind_turbulence_percent")
		
		self.i_batt1 = 					XPLMFindDataRef("sim/operation/failures/rel_bat0_lo")
		self.i_batt2 = 					XPLMFindDataRef("sim/operation/failures/rel_bat1_lo")
		
		self.i_tire1 = 					XPLMFindDataRef("sim/operation/failures/rel_tire1") #eight
		self.i_tire2 = 					XPLMFindDataRef("sim/operation/failures/rel_tire2")
		self.i_tire3 = 					XPLMFindDataRef("sim/operation/failures/rel_tire3")
		self.i_tire4 = 					XPLMFindDataRef("sim/operation/failures/rel_tire4")
		self.i_tire5 = 					XPLMFindDataRef("sim/operation/failures/rel_tire5")
		
		self.i_fire1 = 					XPLMFindDataRef("sim/operation/failures/rel_engfir0") #multiple
		self.i_fire2 = 					XPLMFindDataRef("sim/operation/failures/rel_engfir1")
		self.i_fire3 = 					XPLMFindDataRef("sim/operation/failures/rel_engfir2")
		self.i_fire4 = 					XPLMFindDataRef("sim/operation/failures/rel_engfir3")
		self.i_fire5 =					XPLMFindDataRef("sim/operation/failures/rel_engfir4")
		self.i_fire6 = 					XPLMFindDataRef("sim/operation/failures/rel_engfir5")
		self.i_fire7 = 					XPLMFindDataRef("sim/operation/failures/rel_engfir6")
		self.i_fire8 = 					XPLMFindDataRef("sim/operation/failures/rel_engfir7")
		
		self.i_flameout1 = 				XPLMFindDataRef("sim/operation/failures/rel_engfla0") #multiple
		self.i_flameout2 = 				XPLMFindDataRef("sim/operation/failures/rel_engfla1")
		self.i_flameout3 = 				XPLMFindDataRef("sim/operation/failures/rel_engfla2")
		self.i_flameout4 =				XPLMFindDataRef("sim/operation/failures/rel_engfla3")
		self.i_flameout5 = 				XPLMFindDataRef("sim/operation/failures/rel_engfla4")
		self.i_flameout6 = 				XPLMFindDataRef("sim/operation/failures/rel_engfla5")
		self.i_flameout7 = 				XPLMFindDataRef("sim/operation/failures/rel_engfla6")
		self.i_flameout8 = 				XPLMFindDataRef("sim/operation/failures/rel_engfla7")
		
		
		
		self.i_engine_failure1 = 		XPLMFindDataRef("sim/operation/failures/rel_engfai0") #multiple
		self.i_engine_failure2 = 		XPLMFindDataRef("sim/operation/failures/rel_engfai1")
		self.i_engine_failure3 = 		XPLMFindDataRef("sim/operation/failures/rel_engfai2")
		self.i_engine_failure4 = 		XPLMFindDataRef("sim/operation/failures/rel_engfai3")
		self.i_engine_failure5 = 		XPLMFindDataRef("sim/operation/failures/rel_engfai4")
		self.i_engine_failure6 = 		XPLMFindDataRef("sim/operation/failures/rel_engfai5")
		self.i_engine_failure7 = 		XPLMFindDataRef("sim/operation/failures/rel_engfai6")
		self.i_engine_failure8 = 		XPLMFindDataRef("sim/operation/failures/rel_engfai7")
		
		self.i_hot1 = 					XPLMFindDataRef("sim/operation/failures/rel_hotsta0") #multiple
		self.i_hot2 = 					XPLMFindDataRef("sim/operation/failures/rel_hotsta1")
		self.i_hot3 = 					XPLMFindDataRef("sim/operation/failures/rel_hotsta2")
		self.i_hot4 = 					XPLMFindDataRef("sim/operation/failures/rel_hotsta3")
		self.i_hot5 = 					XPLMFindDataRef("sim/operation/failures/rel_hotsta4")
		self.i_hot6 = 					XPLMFindDataRef("sim/operation/failures/rel_hotsta5")
		self.i_hot7 = 					XPLMFindDataRef("sim/operation/failures/rel_hotsta6")
		self.i_hot8 = 					XPLMFindDataRef("sim/operation/failures/rel_hotsta7")
		
		self.f_ice_frame = 				XPLMFindDataRef("sim/flightmodel/failures/frm_ice")
		self.f_ice_pitot = 				XPLMFindDataRef("sim/flightmodel/failures/pitot_ice")
		self.f_ice_propeller = 			XPLMFindDataRef("sim/flightmodel/failures/prop_ice")
		self.f_ice_window = 			XPLMFindDataRef("sim/flightmodel/failures/window_ice")
		  
		self.f_g_normal = 				XPLMFindDataRef("sim/flightmodel/forces/g_nrml") 
		self.f_g_forward = 				XPLMFindDataRef("sim/flightmodel/forces/g_axil")
		self.f_g_side = 				XPLMFindDataRef("sim/flightmodel/forces/g_side")
		
		
		self.f_pitch = 					XPLMFindDataRef("sim/flightmodel/position/theta")
		self.f_roll = 					XPLMFindDataRef("sim/flightmodel/position/phi")
		self.f_yaw = 					XPLMFindDataRef("sim/flightmodel/position/beta")
		
		#cab press
		self.f_cab_press = 				XPLMFindDataRef("sim/cockpit/pressure/cabin_altitude_actual_m_msl") # meter?
		#cab climb rate
		self.f_cab_rate = 				XPLMFindDataRef("sim/cockpit/pressure/cabin_vvi_actual_m_msec") # meter per second? 1000ft/min = 5m/s
		#cab humidity
		#cab temp
		
		self.f_outside_temp1 = 			XPLMFindDataRef("sim/weather/temperature_ambient_c")
		self.f_outside_temp2 = 			XPLMFindDataRef("sim/cockpit2/temperature/outside_air_temp_degc")
		self.f_outside_temp3 = 			XPLMFindDataRef("sim/cockpit2/temperature/outside_air_LE_temp_degc")
		
		self.f_baro_set =	 			XPLMFindDataRef("sim/cockpit/misc/barometer_setting")
		self.f_baro_sea_level =			XPLMFindDataRef("sim/weather/barometer_sealevel_inhg")
		self.f_baro_alt =				XPLMFindDataRef("sim/flightmodel/misc/h_ind")
		
		######################################################################################### End of DATAREF Find
		
		self.ReadData() # Read data for the first time to ensure window handler can process valid data from the start
	

		self.DrawWindowCB = self.DrawWindowCallback
		self.KeyCB = self.KeyCallback
		self.MouseClickCB = self.MouseClickCallback
		self.WindowId = XPLMCreateWindow(self, 10, 200, 500, 500, 1, self.DrawWindowCB, self.KeyCB, self.MouseClickCB, 0)
		return self.Name, self.Sig, self.Desc


	def XPluginStop(self):
		XPLMUnregisterFlightLoopCallback(self, self.FlightLoopCB, 0)
		XPLMUnregisterCommandHandler ( self , self.CmdSayBaro , self.SayBaroCB , 0 , 0 )
		XPLMUnregisterCommandHandler ( self , self.CmdResetIvy , self.ResetIvyCB , 0 , 0 )
		XPLMDestroyWindow(self, self.WindowId)
		self.OutputFile.close()
		self.ivyConfig.WriteConfig()
		pass
		
		

	def SayBaroCallback( self , cmd , phase , refcon ) :
		if ( phase == 0 ) :	
			self.SayBaro()
		return 0
		
	def ResetIvyCallback( self , cmd , phase , refcon ) :
		#if ( phase == 0 ) :	
		#	self.ResetIvy()
		return 0
		
	def SayBaro(self):

		self.play_mp3_queue.append(self.ivyConfig.mp3_path + "baro_press_1.mp3")	
		self.SpellOutDigits(self.li_baro_sea_level)
		pass
		
		
	def SpellOutDigits(self, spell_number):
		# 1000	
		digit = int((spell_number % 10000) / 1000 )
		self.OutputFile.write(str(digit))
		self.play_mp3_queue.append(self.ivyConfig.number_path + str(digit) + ".mp3")

		# 100
		digit = int((spell_number % 1000) / 100 )
		self.OutputFile.write(str(digit))
		self.play_mp3_queue.append(self.ivyConfig.number_path + str(digit) + ".mp3")
		
		# 10
		digit = int((spell_number % 100) / 10 )
		self.OutputFile.write(str(digit))
		self.play_mp3_queue.append(self.ivyConfig.number_path + str(digit) + ".mp3")
		
		# 1
		digit = int(spell_number % 10)
		self.OutputFile.write(str(digit))
		self.play_mp3_queue.append(self.ivyConfig.number_path + str(digit) + ".mp3")
		
		self.OutputFile.write("Digits \n\r")
		self.OutputFile.flush()
		self.OutputFile.flush()		
		pass
		
	def SpellOutNumber(self, spell_number):
		self.OutputFile.write("SpellOutNumber: ")
		# 1000
		digit = int((spell_number % 10000) / 1000 )
		self.OutputFile.write(str(digit) + " ")
		if (digit > 0):
			self.play_mp3_queue.append(self.ivyConfig.number_path + str(digit*1000) + ".mp3")
			self.play_mp3_queue.append(self.ivyConfig.number_path + "1000")
		# 100
		digit = int((spell_number % 1000) / 100)
		self.OutputFile.write(str(digit) + " ")
		if (digit > 0):
			self.play_mp3_queue.append(self.ivyConfig.number_path + str(digit*100) + ".mp3")
			self.play_mp3_queue.append(self.ivyConfig.number_path + "100")
			
		# 10
		digit = int((spell_number % 100) / 10)
		self.OutputFile.write(str(digit) + " ")
		if (digit > 1):
			self.play_mp3_queue.append(self.ivyConfig.number_path + str(digit*10) + ".mp3")
			digit = int(spell_number % 10)
		else:
			digit = int(spell_number % 100)
		
		# Single digit or <20
		self.OutputFile.write(str(digit) + " ")
		if (digit > 0): 
			self.play_mp3_queue.append(self.ivyConfig.number_path + str(digit) + ".mp3")
		
		self.OutputFile.write("Number End \n\r")
		self.OutputFile.flush()
		self.OutputFile.flush()
		pass

	def XPluginEnable(self):
		self.plugin_enabled = 1
		return 1


	def XPluginDisable(self):
		self.plugin_enabled = 0
		pass



	def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
	
		if (inFromWho == XPLM_PLUGIN_XPLANE):
			if (inMessage == XPLM_MSG_PLANE_LOADED):
				self.aircraft_loaded = 1
				self.ResetIvy()
			if (inMessage == XPLM_MSG_AIRPORT_LOADED):
				self.aircraft_loaded = 1
				self.ResetIvy()
			if (inMessage == XPLM_MSG_PLANE_CRASHED):
				self.aircraft_crashed = 1
		pass



	def DrawWindowCallback(self, inWindowID, inRefcon):
		
		lLeft = [];	lTop = []; lRight = [];	lBottom = []
		XPLMGetWindowGeometry(inWindowID, lLeft, lTop, lRight, lBottom)
		left = int(lLeft[0]); top = int(lTop[0]); right = int(lRight[0]); bottom = int(lBottom[0])

		color = 1.0, 1.0, 1.0
		
		XPLMDrawTranslucentDarkBox(left, top, right, bottom)
		XPLMDrawString(color, left + 5, top - 10, "Data 1: " + str(self.ls_acf_descrip), 0, xplmFont_Basic)
		XPLMDrawString(color, left + 5, top - 20, "Data 2: " + str(self.ivyAircraft.li_v1), 0, xplmFont_Basic)
		XPLMDrawString(color, left + 5, top - 30, "Data 3: " + str(len(self.play_mp3_queue)), 0, xplmFont_Basic)
		XPLMDrawString(color, left + 5, top - 40, "Data 4: " + str(pygame.mixer.music.get_busy()), 0, xplmFont_Basic)
		XPLMDrawString(color, left + 5, top - 50, "Data 5: " + str(self.ivy60kt.active), 0, xplmFont_Basic)
		XPLMDrawString(color, left + 5, top - 60, "Data 6: " + str(self.lf_ias), 0, xplmFont_Basic)

		
		if ((self.li_on_ground == 1) and (self.ivyAircraft.vspeeds_enabled == True) and 
			    (self.lf_ias >= self.ivyAircraft.li_v1) and (self.lf_ground_speed > self.ivyConfig.taxi_ground_speed_min)):
			XPLMDrawString(color, left + 5, top - 70, "Statement TRUE", 0, xplmFont_Basic)
		else: 
			XPLMDrawString(color, left + 5, top - 70, "Statement FALSE", 0, xplmFont_Basic)
		
		
		return 0


	def KeyCallback(self, inWindowID, inKey, inFlags, inVirtualKey, inRefcon, losingFocus):
		return 0


	def MouseClickCallback(self, inWindowID, x, y, inMouse, inRefcon):
		return 0
		
	def DetectLanding(self):	
		if (self.li_on_ground == 0):
			self.landing_detected = 0
			self.landing_rated = 0
		elif ((self.li_on_ground_old == 0) and (self.li_on_ground == 1)):
			self.landing_detected = 1
			
			buf = "Landing detected: " + str(self.time) + " Sinkrate: " + str(self.lf_climb_rate) + " G-Force: " + str(self.lf_g_normal) + "\n\r"
			self.OutputFile.write(buf)
			self.OutputFile.flush()
			
			#(self, time, sink_rate, g_normal, g_side, g_forward)
			landing_object = IvyLandingDetection(self.time, self.lf_climb_rate, self.lf_g_normal, self.lf_g_side, self.lf_g_forward)
			self.ivy_landing_list.append(landing_object)
			
			self.landing_rated = 0
			for obj_number in range(0,len(self.ivy_landing_list)):
				act_rating = self.ivy_landing_list[obj_number].GetCurrentRate(self.time, 10)
				if (act_rating > self.landing_rated) : self.landing_rated = act_rating
				buf = "Landing: " + str(self.ivy_landing_list[obj_number].time) + " Rating: " + str(act_rating) + " | "  
				self.OutputFile.write(buf)
			self.OutputFile.write("\n\r")
			self.OutputFile.flush()
			
		self.li_on_ground_old = self.li_on_ground
		pass
		
	def EndOfFlightEvaluation(self):
		error_rate = 0
		self.landing_detected = 0
		for obj_number in range(0,len(self.ivy_object_list)):
			if (self.ivy_object_list[obj_number].is_error != 0):
				error_rate = error_rate + self.ivy_object_list[obj_number].error_count
			
		if (error_rate == 0): 
			self.play_mp3_queue.append(self.ivyConfig.mp3_path + "error_zero" + ".mp3")
		elif (error_rate < 5):
			self.play_mp3_queue.append(self.ivyConfig.mp3_path + "error_good" + ".mp3")
		elif (error_rate < 10):
			self.play_mp3_queue.append(self.ivyConfig.mp3_path + "error_bad" + ".mp3")
		else:
			self.play_mp3_queue.append(self.ivyConfig.mp3_path + "error_xbad" + ".mp3")
	
	
		self.SpellOutNumber(error_rate)
	
		if (error_rate == 1):
			self.play_mp3_queue.append(self.ivyConfig.mp3_path + "error_a" + ".mp3")
		elif (error_rate > 1):
			self.play_mp3_queue.append(self.ivyConfig.mp3_path + "error_b" + ".mp3")
		pass
		
	def FlightLoopCallback(self, elapsedMe, elapsedSim, counter, refcon):
	
		self.time = self.time + self.ivyConfig.data_rate
		
		# We reset the aircraft loaded situation after 60 seconds
		if (self.time > (60 + self.ivyConfig.disable_after_loading)): 
			self.aircraft_loaded = 0
		
		# Get all the fresh data
		self.ReadData()
		
		# If started to play queue file, we deactivate for X cycles
		if (self.deact_queue > 0):
			self.deact_queue = self.deact_queue - 1
		# If we still have to say something, do not play sounds
		elif (len(self.play_mp3_queue) > 0):
			if (pygame.mixer.music.get_busy() == False):
				pygame.mixer.music.load(self.play_mp3_queue[0])
				pygame.mixer.music.play()
				del self.play_mp3_queue[0]
				self.deact_queue = self.ivyConfig.deact_after_queue
		
		##########################################################################################################################################################################################################
		# NOT after Load and NOT after Crash

		elif ((self.time > self.ivyConfig.disable_after_loading) and (self.aircraft_crashed == 0)):
	
			if (self.lf_g_normal > self.f_g_normal_max): self.f_g_normal_max = self.lf_g_normal
			if (self.lf_g_side > self.f_g_side_max): self.f_g_side_max = self.lf_g_side
			if (self.lf_g_forward > self.f_g_forward_max): self.f_g_forward_max = self.lf_g_forward
			
			if (self.lf_g_normal < self.f_g_normal_min): self.f_g_normal_min = self.lf_g_normal
			if (self.lf_g_side < self.f_g_side_min): self.f_g_side_min = self.lf_g_side
			if (self.lf_g_forward < self.f_g_forward_min): self.f_g_forward_min = self.lf_g_forward
			

			
			self.f_g_normal_delta = (self.lf_g_normal - self.f_g_normal_old) / self.ivyConfig.data_rate
			self.f_g_side_delta = (self.lf_g_side - self.f_g_side_old) / self.ivyConfig.data_rate
			self.f_g_front_delta = (self.lf_g_forward - self.f_g_forward_old) / self.ivyConfig.data_rate
		
			self.f_g_normal_old = self.lf_g_normal
			self.f_g_side_old = self.lf_g_side
			self.f_g_forward_old = self.lf_g_forward
			
			self.DetectLanding()
			
			
			
			if ((self.li_on_ground == 1) and ((self.lf_g_normal) > self.ivyConfig.ivy_ouch_g)): #play ouch
				pygame.mixer.music.load(self.ivyConfig.mp3_path + "ouch_1.mp3")
				pygame.mixer.music.play()
			
			if ((self.li_on_ground == 0) and (self.lf_climb_rate > self.ivyConfig.pos_rate_climb)):														self.ivyPosRateClimb.Activate(self.time)
			elif (self.li_on_ground == 1):																												self.ivyPosRateClimb.Deactivate(self.time)
			

			
			if (self.lf_gear_ratio > 0.999):																											self.ivyGearDown.Activate(self.time)
			else:																																		self.ivyGearDown.Deactivate(self.time)
			
			if (self.lf_gear_ratio < 0.001):																											self.ivyGearUp.Activate(self.time)
			else:																																		self.ivyGearUp.Deactivate(self.time)
			
			if ((self.li_tire1 + self.li_tire2 + self.li_tire3 + self.li_tire4 + self.li_tire5) > 0):													self.ivyTyre.Activate(self.time)
			else:																																		self.ivyTyre.Deactivate(self.time)
			
			if ((self.li_on_ground == 1) and (self.lf_g_forward > self.ivyConfig.brake_max_forward_g)): 												self.ivyBrake.Activate(self.time)
			else:																																		self.ivyBrake.Deactivate(self.time)		
			
			if ((self.li_on_ground == 0) and (self.li_transponder_mode < 2)):																			self.ivyTransponder.Activate(self.time) # Dataref: Mode2=ON, B407 4=ON
			elif (self.li_on_ground == 1):																												self.ivyTransponder.Deactivate(self.time)
			
			if ((self.li_on_ground == 0) and (self.lf_radio_alt < self.ivyConfig.alt_landing_lights_low) and 
			    (self.lf_world_light_precent > self.ivyConfig.night_world_light_precent) and (self.li_landing_lights == 0)):							self.ivyLandingLights.Activate(self.time)
			else:																																		self.ivyLandingLights.Deactivate(self.time)
			
			if ((self.li_on_ground == 1) and (self.lf_ground_speed > self.ivyConfig.taxi_ground_speed_min) and (self.li_beacon_lights == 0)):			self.ivyBeaconLights.Activate(self.time) 
			elif (self.li_beacon_lights != 0):																											self.ivyBeaconLights.Deactivate(self.time)
					
			if ((self.li_on_ground == 0) and (self.li_nav_lights == 0)):																				self.ivyNavLights.Activate(self.time) 
			else:																																		self.ivyNavLights.Deactivate(self.time) 
			
			if ((self.li_on_ground == 0) and (self.li_strobe_lights == 0)):																				self.ivyStrobes.Activate(self.time) 				
			else:																																		self.ivyStrobes.Deactivate(self.time)
			
			if (((self.li_tire1 + self.li_tire2 + self.li_tire3 + self.li_tire4 + self.li_tire5) > 0) and (self.li_has_skid == 1)):						self.ivySkidTyres.Activate(self.time) 			
			else:																																		self.ivySkidTyres.Deactivate(self.time)
			
			if ((self.li_batt1 + self.li_batt2) > 0):																									self.ivyBatteryOut.Activate(self.time) 			
			else:																																		self.ivyBatteryOut.Deactivate(self.time) 
			
			if ((self.li_fire1 + self.li_fire2 + self.li_fire3 + self.li_fire4 + self.li_fire5 + self.li_fire6 + self.li_fire7 + self.li_fire8) > 0):	self.ivyEngineFire.Activate(self.time) 			
			else:																																		self.ivyEngineFire.Deactivate(self.time)
			
			if ((self.li_flameout1 + self.li_flameout2 + self.li_flameout3 + self.li_flameout4 + 
				 self.li_flameout5 + self.li_flameout6 + self.li_flameout7 + self.li_flameout8) > 0):													self.ivyEngineFlameout.Activate(self.time) 	
			else:																																		self.ivyEngineFlameout.Deactivate(self.time)
			
			if ((self.li_on_ground == 1) and 
			   ((self.li_engine_failure1 + self.li_engine_failure2 + self.li_engine_failure3 + self.li_engine_failure4 + 
				 self.li_engine_failure5 + self.li_engine_failure6 + self.li_engine_failure7 + self.li_engine_failure8) > 0)):							self.ivyEngineFailureGround.Activate(self.time) 	
			else:																																		self.ivyEngineFailureGround.Deactivate(self.time)
			
			if ((self.li_on_ground == 0) and 
			   ((self.li_engine_failure1 + self.li_engine_failure2 + self.li_engine_failure3 + self.li_engine_failure4 + 
				 self.li_engine_failure5 + self.li_engine_failure6 + self.li_engine_failure7 + self.li_engine_failure8) > 0)):							self.ivyEngineFailureAir.Activate(self.time) 		
			else:																																		self.ivyEngineFailureAir.Deactivate(self.time)
			
			if ((self.li_hot1 + self.li_hot2 + self.li_hot3 + self.li_hot4 + self.li_hot5 + self.li_hot6 + self.li_hot7 + self.li_hot8) > 0):			self.ivyEngineHotStart.Activate(self.time) 		
			else:																																		self.ivyEngineHotStart.Deactivate(self.time)
			
			if ((self.li_battery_on == 0) and (self.li_gpu_on == 0)):																					self.ivyNoBatt.Activate(self.time) 				
			else:																																		self.ivyNoBatt.Deactivate(self.time)
			
				
			
			
			
			if ((self.aircraft_loaded == 1) and 
				(self.li_cloud_0 < 2) and (self.li_cloud_1 < 2) and (self.li_cloud_2 < 2) and 
				(self.lf_visibility > self.ivyConfig.vis_is_fog) and (self.li_rain == 0) and (self.li_thunder == 0)):														self.ivyHelloSun.Activate(self.time) 				
			else:																																		self.ivyHelloSun.Deactivate(self.time)
			
			if ((self.aircraft_loaded == 1) and 
				(self.lf_visibility > self.ivyConfig.vis_is_fog) and (self.li_rain > 0) and (self.li_thunder == 0)):															self.ivyHelloRain.Activate(self.time) 			
			else:																																		self.ivyHelloRain.Deactivate(self.time)
			
			#ToDo:
			#if ((self.aircraft_loaded == 1) and 
			#	(self.lf_visibility > self.ivyConfig.vis_is_fog) and (self.li_thunder > 0)):															self.ivyHelloThunder.Activate(self.time) 			
			#else:																																		self.ivyHelloThunder.Deactivate(self.time)
			
			if ((self.aircraft_loaded == 1) and 
				(self.lf_visibility <= self.ivyConfig.vis_is_fog)):																						self.ivyHelloFog.Activate(self.time) 				
			else:																																		self.ivyHelloFog.Deactivate(self.time)
			
			if ((self.aircraft_loaded == 1) and 
				((self.li_cloud_0 >= 2) or (self.li_cloud_1 >= 2) or (self.li_cloud_2 >= 2)) and 
				(self.lf_visibility > self.ivyConfig.vis_is_fog) and (self.li_rain == 0) and (self.li_thunder == 0)):									self.ivyHelloNormal.Activate(self.time) 			
			else:																																		self.ivyHelloNormal.Deactivate(self.time)
			
			if ((self.li_on_ground == 0) and (self.lf_cab_rate < self.ivyConfig.cab_rate_low)):															self.ivyCabinDownNormal.Activate(self.time) 		
			elif (self.lf_cab_rate > (self.ivyConfig.cab_rate_low + self.ivyConfig.cab_rate_reset_hysteresis)):											self.ivyCabinDownNormal.Deactivate(self.time)
			
			if ((self.li_on_ground == 0) and (self.lf_cab_rate < self.ivyConfig.cab_rate_high)):																				
																																						self.ivyCabinDownFast.Activate(self.time) 		
																																						self.ivyCabinDownNormal.SetAsPlayed(self.time)
			elif (self.lf_cab_rate > (self.ivyConfig.cab_rate_high + self.ivyConfig.cab_rate_reset_hysteresis)):										self.ivyCabinDownFast.Deactivate(self.time)
			
			if ((self.li_on_ground == 0) and (abs(self.lf_roll) > self.ivyConfig.bank_low)):															self.ivyBankNormal.Activate(self.time) 			
			elif (abs(self.lf_roll) < self.ivyConfig.bank_reset_low):																					self.ivyBankNormal.Deactivate(self.time)
			
			if ((self.li_on_ground == 0) and (abs(self.lf_roll) > self.ivyConfig.bank_high)):		
																																						self.ivyBankHigh.Activate(self.time) 
																																						self.ivyBankNormal.SetAsPlayed(self.time)
			elif (abs(self.lf_roll) < self.ivyConfig.bank_low):																							self.ivyBankHigh.Deactivate(self.time)
			
			if ((self.li_on_ground == 0) and (abs(self.lf_roll) > self.ivyConfig.bank_xhigh)):															
																																						self.ivyBankXHigh.Activate(self.time) 
																																						self.ivyBankHigh.SetAsPlayed(self.time)
																																						self.ivyBankNormal.SetAsPlayed(self.time)		
			elif (abs(self.lf_roll) < self.ivyConfig.bank_high):																						self.ivyBankXHigh.Deactivate(self.time)
			
			if ((self.li_on_ground == 0) and (self.lf_pitch < self.ivyConfig.pitch_low)):																self.ivyPitchDownNormal.Activate(self.time) 		
			elif (self.lf_pitch > self.ivyConfig.pitch_reset_low):																						self.ivyPitchDownNormal.Deactivate(self.time)
			
			if ((self.li_on_ground == 0) and (self.lf_pitch <= self.ivyConfig.pitch_high)):																					
																																						self.ivyPitchDownHigh.Activate(self.time) 
																																						self.ivyPitchDownNormal.SetAsPlayed(self.time)
			elif (self.lf_pitch > self.ivyConfig.pitch_low):																							self.ivyPitchDownHigh.Deactivate(self.time)
			
			
			
			

			
			
			
			
			
			
			
			
			
			
			if ((self.li_on_ground == 0) and (self.lf_g_normal >= self.ivyConfig.max_g_down_low)):														self.ivyGNormalFlightNormal.Activate(self.time) 	
			elif (self.lf_g_normal <= self.ivyConfig.max_g_down_low_reset):																				self.ivyGNormalFlightNormal.Deactivate(self.time)
			
			if ((self.li_on_ground == 0) and (self.lf_g_normal >= self.ivyConfig.max_g_down_high)):														
																																						self.ivyGNormalFlightHigh.Activate(self.time) 
																																						self.ivyGNormalFlightNormal.SetAsPlayed(self.time)
			elif (self.lf_g_normal <= self.ivyConfig.max_g_down_low_reset):																				self.ivyGNormalFlightHigh.Deactivate(self.time)
			
			if ((self.li_on_ground == 0) and (self.lf_g_normal >= self.ivyConfig.max_g_down_xhigh)):																					
																																						self.ivyGNormalFlightXHigh.Activate(self.time)
																																						self.ivyGNormalFlightHigh.SetAsPlayed(self.time)
																																						self.ivyGNormalFlightNormal.SetAsPlayed(self.time)
			elif (self.lf_g_normal <= self.ivyConfig.max_g_down_low_reset):																				self.ivyGNormalFlightXHigh.Deactivate(self.time)
			
			#self.li_turbulence = XPLMGetDatai(self.i_turbulence)
			#if ((self.li_on_ground == 0) and (self.li_turbulence > 10)):																				self.ivyTurbulenceNormal.Activate(self.time) 		
			#elif (self.li_turbulence < 2):																												self.ivyTurbulenceNormal.Deactivate(self.time)
			
			#if ((self.li_on_ground == 0) and (self.li_turbulence > 30)):																				self.ivyTurbolenceHigh.Activate(self.time) 		
			#elif (self.li_turbulence < 5):																												self.ivyTurbolenceHigh.Deactivate(self.time)
			
			if ((self.lf_radio_alt < self.ivyConfig.baro_alt_low) and 
			    (abs(self.li_baro_set - self.li_baro_sea_level) > self.ivyConfig.baro_tolerance) and (self.time > 60)):																
																																						self.ivyBaroGround.Activate(self.time)
																																						if ((self.ivyBaroGround.played == 1) and (self.pressure_said == 0)): 
																																							self.pressure_said = 1
																																							self.SayBaro()
			elif ((abs(self.li_baro_set - self.li_baro_sea_level) <= self.ivyConfig.baro_tolerance) or (self.lf_baro_alt > self.ivyConfig.trans_alt)) :
																																						self.ivyBaroGround.Deactivate(self.time)
																																						self.pressure_said = 0
			
			if ((self.lf_baro_alt > (self.ivyConfig.trans_alt + self.ivyConfig.trans_hysteresis)) and 
			    (abs(2992 - self.li_baro_sea_level) > self.ivyConfig.baro_tolerance)):																	self.ivyBaroHigh.Activate(self.time)
			else:																																		self.ivyBaroHigh.Deactivate(self.time)
			
			if ((self.li_on_ground == 1) and (self.lf_ias > 58) and (self.lf_ias < 70)):																self.ivy60kt.Activate(self.time) 
			else:																																		self.ivy60kt.Deactivate(self.time)
			
			if ((self.li_on_ground == 1) and (self.lf_ias > 160) and (self.landing_detected == 0)):														self.ivyRotate.Activate(self.time) 
			else:																																		self.ivyRotate.Deactivate(self.time)
			
			if (self.lf_ice_frame > self.ivyConfig.ice_low):																							self.ivyIceAirframeLow.Activate(self.time)
			else:																																		self.ivyIceAirframeLow.Deactivate(self.time)
			
			if (self.lf_ice_frame > self.ivyConfig.ice_high):																												
																																						self.ivyIceAirframeHigh.Activate(self.time)
																																						self.ivyIceAirframeLow.SetAsPlayed(self.time)
			else:																																		self.ivyIceAirframeHigh.Deactivate(self.time)
			
			if (self.lf_ice_pitot > self.ivyConfig.ice_low):																							self.ivyIcePitotLow.Activate(self.time)
			else:																																		self.ivyIcePitotLow.Deactivate(self.time)
			
			if (self.lf_ice_pitot > self.ivyConfig.ice_high):																												
																																						self.ivyIcePitotHigh.Activate(self.time)
																																						self.ivyIcePitotLow.SetAsPlayed(self.time)
			else:																																		self.ivyIcePitotHigh.Deactivate(self.time)
			
			if (self.lf_ice_propeller > self.ivyConfig.ice_low):																						self.ivyIcePropellerLow.Activate(self.time)
			else:																																		self.ivyIcePropellerLow.Deactivate(self.time)
			
			if (self.lf_ice_propeller > self.ivyConfig.ice_high):																												
																																						self.ivyIcePropellerHigh.Activate(self.time)
																																						self.ivyIcePropellerLow.SetAsPlayed(self.time)
			else:																																		self.ivyIcePropellerHigh.Deactivate(self.time)
			
			if (self.lf_ice_window > self.ivyConfig.ice_low):																							self.ivyIceWindowLow.Activate(self.time)
			else:																																		self.ivyIceWindowLow.Deactivate(self.time)
			
			if (self.lf_ice_window > self.ivyConfig.ice_high):																												
																																						self.ivyIceWindowHigh.Activate(self.time)
																																						self.ivyIceWindowLow.SetAsPlayed(self.time)
			else:																																		self.ivyIceWindowHigh.Deactivate(self.time)
			
			if (self.lf_cab_press > self.ivyConfig.cab_press_low):																						self.ivyPressureLow.Activate(self.time) 
			else:																																		self.ivyPressureLow.Deactivate(self.time)
			
			if (self.lf_cab_press > self.ivyConfig.cab_press_high):																												
																																						self.ivyPressureXLow.Activate(self.time) 
																																						self.ivyPressureLow.SetAsPlayed(self.time)
			else:																																		self.ivyPressureXLow.Deactivate(self.time)
			
			
		
			
			
			if ((self.li_on_ground == 1) and (self.ivyAircraft.vspeeds_enabled == True) and 
			    (self.lf_ias >= self.ivyAircraft.li_v1) and (self.lf_ground_speed > self.ivyConfig.taxi_ground_speed_min)):								self.ivyV1.Activate(self.time)
			elif ((self.li_on_ground == 1) and (self.lf_ias < 10)):																						self.ivyV1.Deactivate(self.time)
			
			if ((self.li_on_ground == 1) and (self.ivyAircraft.vspeeds_enabled == True) and 
			    (self.lf_ias >= self.ivyAircraft.li_vr) and (self.lf_ground_speed > self.ivyConfig.taxi_ground_speed_min)):								self.ivyVR.Activate(self.time)
			elif ((self.li_on_ground == 1) and (self.lf_ias < 10)):																						self.ivyVR.Deactivate(self.time)
			
			
			##########################################################################################################################################################################################################
			# After Landing
			
			
			
			if ((self.landing_detected == 1) and (self.landing_rated == 1)):																			
																																						self.ivyLandingXGood.Activate(self.time) 	
																																						if (self.ivyLandingXGood.played == 1):	self.EndOfFlightEvaluation()
			else:																																		self.ivyLandingXGood.Deactivate(self.time)
			
			if ((self.landing_detected == 1) and (self.landing_rated == 2)):																			
																																						self.ivyLandingGood.Activate(self.time) 	
																																						if (self.ivyLandingGood.played == 1):	self.EndOfFlightEvaluation()
			else:																																		self.ivyLandingGood.Deactivate(self.time)
			
			if ((self.landing_detected == 1) and (self.landing_rated == 3)):																			
																																						self.ivyLandingBad.Activate(self.time) 	
																																						if (self.ivyLandingBad.played == 1):	self.EndOfFlightEvaluation()
			else:																																		self.ivyLandingBad.Deactivate(self.time)
			
			if ((self.landing_detected == 1) and (self.landing_rated == 4)):																			
																																						self.ivyLandingXBad.Activate(self.time) 
																																						if (self.ivyLandingXBad.played == 1):	self.EndOfFlightEvaluation()
			else:																																		self.ivyLandingXBad.Deactivate(self.time)
		
		##########################################################################################################################################################################################################
		# After Load or after Crash

		if ((self.aircraft_crashed == 1) and (self.time > self.ivyConfig.disable_after_loading)):														self.ivyCrash.Activate(self.time) 			
		else:																																			self.ivyCrash.Deactivate(self.time)
			
		#if ((self.lf_world_light_precent > 0.5) and (self.lf_climb_rate > 100)):  pass
		
		#buf = "Normal: " + "{:.2f}".format(self.f_g_normal_delta) + "Side: " + "{:.2f}".format(self.f_g_side_delta) + "Normal: " + "{:.2f}".format(self.f_g_forward_delta) + "\r\n"
		#self.OutputFile.write(buf)
		
		return self.ivyConfig.data_rate


	def ReadData(self):
		#########################################################################################
		#
		#						DATAREF Local Variables
		#
		#########################################################################################
				
		
		
		lba_acf_descrip= []

		XPLMGetDatab(self.s_acf_descrip,lba_acf_descrip,0,240) 	
		self.ls_acf_descrip = str(lba_acf_descrip)
		self.li_on_ground= 				XPLMGetDatai(self.i_on_ground) 			
		self.lf_climb_rate= 			XPLMGetDataf(self.f_climb_rate) 
		self.lf_gear_ratio=				XPLMGetDataf(self.f_gear_ratio) 
		self.lf_ground_speed= 			XPLMGetDataf(self.f_ground_speed) 	* 3600/1852	# is m/s and we want nm/h
		self.lf_ias= 					XPLMGetDataf(self.f_ias)
		self.lf_sun_pitch= 				XPLMGetDataf(self.f_sun_pitch) 			
		self.lf_airport_light= 			XPLMGetDataf(self.f_airport_light) 		
		self.lf_world_light_precent= 	XPLMGetDataf(self.f_world_light_precent) 	
		self.li_has_skid= 				XPLMGetDatai(self.i_has_skid) 			
		self.li_transponder_mode= 		XPLMGetDatai(self.i_transponder_mode) 	
		
		self.li_temp_sl= 				XPLMGetDatai(self.i_temp_sl) 				
		self.li_dew_sl= 				XPLMGetDatai(self.i_dew_sl) 				
		
		self.li_landing_lights= 		XPLMGetDatai(self.i_landing_lights) 		
		self.li_beacon_lights= 			XPLMGetDatai(self.i_beacon_lights) 		
		self.li_nav_lights= 			XPLMGetDatai(self.i_nav_lights) 			
		self.li_strobe_lights= 			XPLMGetDatai(self.i_strobe_lights) 		
		self.li_taxi_lights= 			XPLMGetDatai(self.i_taxi_lights) 			
		self.li_cockpit_lights= 		XPLMGetDatai(self.i_cockpit_lights) 	
		self.lf_radio_alt= 				XPLMGetDataf(self.f_radio_alt)
		self.lf8_batter_charge= 		XPLMGetDataf(self.f8_batter_charge) 

		self.li_battery_on = 			XPLMGetDatai(self.i_battery_on)	
		self.li_gpu_on = 				XPLMGetDatai(self.i_gpu_on)	

		self.li_cloud_0 = 				XPLMGetDatai(self.i_cloud_0) 				
		self.li_cloud_1 = 				XPLMGetDatai(self.i_cloud_1) 				
		self.li_cloud_2 = 				XPLMGetDatai(self.i_cloud_2) 				
		self.lf_visibility = 			XPLMGetDataf(self.f_visibility) 			
		self.li_rain = 					XPLMGetDatai(self.i_rain) 					
		self.li_thunder = 				XPLMGetDatai(self.i_thunder) 				
		self.li_turbulence = 			XPLMGetDatai(self.i_turbulence) 			
		
		
		self.li_batt1= 					XPLMGetDatai(self.i_batt1)			
		self.li_batt2= 					XPLMGetDatai(self.i_batt2)			
		
		self.li_tire1= 					XPLMGetDatai(self.i_tire1) 				
		self.li_tire2= 					XPLMGetDatai(self.i_tire2) 				
		self.li_tire3= 					XPLMGetDatai(self.i_tire3) 				
		self.li_tire4= 					XPLMGetDatai(self.i_tire4) 				
		self.li_tire5= 					XPLMGetDatai(self.i_tire5) 								
		
		self.li_fire1= 					XPLMGetDatai(self.i_fire1) 				
		self.li_fire2= 					XPLMGetDatai(self.i_fire2) 				
		self.li_fire3= 					XPLMGetDatai(self.i_fire3) 				
		self.li_fire4= 					XPLMGetDatai(self.i_fire4) 				
		self.li_fire5= 					XPLMGetDatai(self.i_fire5) 				
		self.li_fire6= 					XPLMGetDatai(self.i_fire6) 				
		self.li_fire7= 					XPLMGetDatai(self.i_fire7) 				
		self.li_fire8= 					XPLMGetDatai(self.i_fire8) 				
		
		self.li_flameout1= 				XPLMGetDatai(self.i_flameout1) 			
		self.li_flameout2= 				XPLMGetDatai(self.i_flameout2) 			
		self.li_flameout3=				XPLMGetDatai(self.i_flameout3) 			
		self.li_flameout4= 				XPLMGetDatai(self.i_flameout4) 			
		self.li_flameout5= 				XPLMGetDatai(self.i_flameout5) 			
		self.li_flameout6= 				XPLMGetDatai(self.i_flameout6) 			
		self.li_flameout7= 				XPLMGetDatai(self.i_flameout7) 			
		self.li_flameout8= 				XPLMGetDatai(self.i_flameout8) 			
		
		
		
		self.li_engine_failure1= 		XPLMGetDatai(self.i_engine_failure1) 		
		self.li_engine_failure2= 		XPLMGetDatai(self.i_engine_failure2) 		
		self.li_engine_failure3= 		XPLMGetDatai(self.i_engine_failure3) 		
		self.li_engine_failure4= 		XPLMGetDatai(self.i_engine_failure4) 		
		self.li_engine_failure5= 		XPLMGetDatai(self.i_engine_failure5) 		
		self.li_engine_failure6= 		XPLMGetDatai(self.i_engine_failure6) 		
		self.li_engine_failure7= 		XPLMGetDatai(self.i_engine_failure7) 		
		self.li_engine_failure8= 		XPLMGetDatai(self.i_engine_failure8) 		
		
		self.li_hot1= 					XPLMGetDatai(self.i_hot1) 					
		self.li_hot2= 					XPLMGetDatai(self.i_hot2) 					
		self.li_hot3= 					XPLMGetDatai(self.i_hot3) 					
		self.li_hot4= 					XPLMGetDatai(self.i_hot4) 					
		self.li_hot5= 					XPLMGetDatai(self.i_hot5) 					
		self.li_hot6= 					XPLMGetDatai(self.i_hot6) 					
		self.li_hot7= 					XPLMGetDatai(self.i_hot7) 					
		self.li_hot8= 					XPLMGetDatai(self.i_hot8) 	

		self.lf_ice_frame = 			XPLMGetDataf(self.f_ice_frame)	
		self.lf_ice_pitot = 			XPLMGetDataf(self.f_ice_pitot)	
		self.lf_ice_propeller = 		XPLMGetDataf(self.f_ice_propeller)
		self.lf_ice_window = 			XPLMGetDataf(self.f_ice_window)	



		
		  
		self.lf_g_normal= 				XPLMGetDataf(self.f_g_normal) 			
		self.lf_g_forward= 				XPLMGetDataf(self.f_g_forward) 			
		self.lf_g_side= 				XPLMGetDataf(self.f_g_side) 				
		
		
		self.lf_pitch= 					XPLMGetDataf(self.f_pitch) 				
		self.lf_roll= 					XPLMGetDataf(self.f_roll) 				
		self.lf_yaw= 					XPLMGetDataf(self.f_yaw) 					
		
		#cab press
		self.lf_cab_press= 				XPLMGetDataf(self.f_cab_press) 			
		#cab climb rate
		self.lf_cab_rate= 				XPLMGetDataf(self.f_cab_rate) 			
		#cab humidity
		#cab temp
		
		self.lf_outside_temp1= 			XPLMGetDataf(self.f_outside_temp1) 		
		self.lf_outside_temp2= 			XPLMGetDataf(self.f_outside_temp2) 		
		self.lf_outside_temp3= 			XPLMGetDataf(self.f_outside_temp3) 	

		self.lf_baro_set = 				XPLMGetDataf(self.f_baro_set)
		self.li_baro_set = 				int(self.lf_baro_set * 100)
		self.lf_baro_sea_level = 		XPLMGetDataf(self.f_baro_sea_level)
		self.li_baro_sea_level = 		int(self.lf_baro_sea_level * 100)
		self.lf_baro_alt = 				XPLMGetDataf(self.f_baro_alt)
		
		self.ivyAircraft.UpdateData()
		
		######################################################################################### End of DATAREF Local Variables
		pass
		