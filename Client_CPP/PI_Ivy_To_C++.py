 
 
 
 
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
// IvyLandingDetection;
//;
// Small class to store our landing data, rate the landing && check if the touchdown was within the given time frame;
 
class IvyLandingDetection(object){
	def __init__(self, time, sink_rate, g_normal, g_side, g_forward){
		m_time = time;
		m_sink_rate = sink_rate;
		m_g_normal = g_normal;
		m_g_side = g_side;
		m_g_forward = g_forward;
		m_rating = 0;
		m_RateLanding();
		pass;
 
	def RateLanding(self){
		if ((m_sink_rate > -100) && (m_g_normal < 1.5)){		m_rating = 1;
		else if (m_sink_rate > -250) && (m_g_normal < 2){		m_rating = 2;
		else if (m_sink_rate > -400) && (m_g_normal < 3){		m_rating = 3;
		else if (m_sink_rate > -500) && (m_g_normal < 4){		m_rating = 4;
		else{														m_rating = 5;
		pass;
 
	def GetCurrentRate(self, last_landing_time, max_time){
		if ((last_landing_time - m_time) < max_time){
			return m_rating;
		else{
			return 0;
 
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
// IvyPassengers;
//;
// Small class to make our passenger noise;
 
class IvyPassengers(object){
	def __init__(self, ivyConfig, channel){
		m_ivyConfig = ivyConfig;
		m_is_screaming = false;
		//m_fading = false;
 
		m_passengerChannel 	= pygame.mixer.Channel(channel);
		m_passengerChannel.stop();
		m_screamSound = pygame.mixer.Sound(m_ivyConfig.mp3_path + "passenger_screams.wav");
 
		pass;
 
	def MakeScream(self, screaming, volume){
		volume = min(1 , volume);
		volume = max(0.3 , volume);
 
		m_passengerChannel.set_volume(volume);
 
		if ((screaming == true) && (m_is_screaming == false)){
			//m_fading = false;
			m_is_screaming = true;
			m_passengerChannel.play(m_screamSound, -1, 0, 1000);
 
		else if ((screaming == false) && (m_is_screaming == true)){
		//else if (screaming == false){
			m_is_screaming = false;
			m_passengerChannel.fadeout(500);
		pass;
 
 
 
 
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
// PythonInterface;
//;
// Main class where we do our stuff;
 
class PythonInterface{
 
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
	// ResetIvy;
	//;
	// Resets all datasets && reloads the IvyAircraft depending upon the aircraft name given in the acf file;
 
	def ResetIvy(self){
		m_time = 0;
		m_landing_detected = 0;
		m_landing_rated = 0;
		m_landing_bounces = 0;
		m_landing_g_normal = 0;
		m_landing_sink_rate = 0;
		m_aircraft_crashed = 0;
		m_pressure_said = 0;
		m_non_smoking_old = 0;
		m_non_smoking_event = -100 // Needed for Startup with Non-Smoking enabled.;
 
		m_airport_departure = "NONE";
		m_airport_departure_temp = "NONE";
		m_airport_arrival   = "NONE";
		m_time_departure = 0;
 
 
		m_play_mp3_queue = [];
		m_ivy_landing_list = [];
 
 
 
		for obj_number in range(0,len(m_ivy_object_list)){
			m_ivy_object_list[obj_number].error_count = 0;
			m_ivy_object_list[obj_number].active = m_ivy_object_list[obj_number].active_on_load;
			m_ivy_object_list[obj_number].played = m_ivy_object_list[obj_number].active_on_load;
 
		lba_acf_descrip= [];
		lba_acf_tailnumber = [];
 
		XPLMGetDatab(m_s_acf_descrip,lba_acf_descrip,0,240);
		XPLMGetDatab(m_s_acf_tailnumber,lba_acf_tailnumber,0,40);
 
		m_ls_acf_descrip = str(lba_acf_descrip) + str(lba_acf_tailnumber);
 
		m_ivyAircraft = m_ivy_aircraft_list[0];
 
		for index in range(0,len(m_ivy_aircraft_list)){
			if (m_ivy_aircraft_list[index].name in m_ls_acf_descrip){
				m_ivyAircraft = m_ivy_aircraft_list[index];
 
 
 
		pass;
 
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
	// XPluginStart;
	//;
	// Startup function for loading error responses && loading datarefs;
 
	def XPluginStart(self){
 
		m_Name = "Ivy";
		m_Sig =  "ka.Python.Ivy";
		m_Desc = "The nagging Co-Pilot";
 
		m_play_mp3_queue = [];
		m_ivy_object_list = [];
		m_ivy_landing_list = [];
		m_ivy_aircraft_list = [];
 
		//m_ivyAircraft = MyIvyAircraft();
 
		m_aircraft_loaded = 0;
		m_plugin_enabled = 0;
		m_deact_queue = 0;
 
 
 
		m_no_aircraft = true;
		m_draw_window = 0;
		m_MenuVSpeedsShow = 0;
		m_logbook_index = 0;
 
 
 
		m_ivyConfig = MyIvyConfiguration();
		m_ivyConfig.ReadConfig();
 
 
 
		m_ivy_aircraft_list.append(MyIvyConfigAircraft(""));
		m_ivyAircraft = m_ivy_aircraft_list[0];
 
		for index in range(1,100){
			aircraft_ini_path = m_ivyConfig.config_path + "IvyAircraft_" + str(index) + ".ini";
			if (os.path.isfile(aircraft_ini_path)){
				m_ivy_aircraft_list.append(MyIvyConfigAircraft(aircraft_ini_path));
 
 
 
 
		//m_startup = 1;
 
		m_s_acf_descrip = 			XPLMFindDataRef("sim/aircraft/view/acf_descrip");
		m_s_acf_tailnumber = 		XPLMFindDataRef("sim/aircraft/view/acf_tailnum");
		m_ResetIvy();
		//m_Clicked = 0;
 
		m_outputPath = m_ivyConfig.config_path + "IvyLog.txt";
		m_OutputFile = open(m_outputPath, 'w');
 
		// Init the pygame mixer;
		pygame.mixer.init();
		m_ivyChannel 		= pygame.mixer.Channel(0);
 
		m_ivyPassengers = IvyPassengers(m_ivyConfig, 1);
 
 
		random.seed();
 
 
 
		//m_END_MUSIC_EVENT = pygame.USEREVENT + 0    // ID for music Event;
		//pygame.mixer.music.set_endevent(END_MUSIC_EVENT);
 
		//												//Name						PATH						DEACT_ON_LOAD		MINIMUM_OCC_TIME		DEACT_TIME				IS_ERRor			IVY_OBJECT_LIST		CHANNEL;
		m_ivyOuch = 					MyIvyResponse(	"ouch", 					m_ivyConfig.mp3_path,	0,				0, 						0, 						0,					m_ivy_object_list, 	0);
		m_ivyPosRateClimb = 			MyIvyResponse(	"pos_climb", 				m_ivyConfig.mp3_path,	0,				1, 						20, 					0,					m_ivy_object_list, 	0);
		m_ivyTyre = 					MyIvyResponse(	"tyre", 					m_ivyConfig.mp3_path,	0,				0, 						0, 						1,					m_ivy_object_list, 	0);
		m_ivyBrake = 				MyIvyResponse(	"brake", 					m_ivyConfig.mp3_path,	0,				2, 						10,						1,					m_ivy_object_list, 	0);
		m_ivyTransponder = 			MyIvyResponse(	"transponder", 				m_ivyConfig.mp3_path,	0,				120, 					0, 						1,					m_ivy_object_list, 	0);
		m_ivyCockpitLights = 		MyIvyResponse(	"cockpit_lights", 			m_ivyConfig.mp3_path,	0,				5, 						0, 						1,					m_ivy_object_list, 	0) // TBD;
		m_ivyLandingLights = 		MyIvyResponse(	"landing_lights", 			m_ivyConfig.mp3_path,	0,				0, 						0, 						1,					m_ivy_object_list, 	0);
 
		m_ivyGearUp = 				MyIvyResponse(	"gear_up", 					m_ivyConfig.mp3_path,	1,				1, 						0, 						0,					m_ivy_object_list, 	0);
		m_ivyGearDown = 				MyIvyResponse(	"gear_down", 				m_ivyConfig.mp3_path,	1,				1, 						0, 						0,					m_ivy_object_list, 	0);
 
		m_ivyBeaconLights = 			MyIvyResponse(	"beacon", 					m_ivyConfig.mp3_path,	0,				20, 					0, 						1,					m_ivy_object_list, 	0);
		m_ivyNavLights = 			MyIvyResponse(	"nav_lights", 				m_ivyConfig.mp3_path,	0,				50, 					0, 						1,					m_ivy_object_list, 	0);
		m_ivyStrobes = 				MyIvyResponse(	"strobes", 					m_ivyConfig.mp3_path,	0,				200, 					0, 						1,					m_ivy_object_list, 	0);
		m_ivySkidTyres = 			MyIvyResponse(	"skid_tyres", 				m_ivyConfig.mp3_path,	0,				5, 						0, 						0,					m_ivy_object_list, 	0);
		m_ivyBatteryOut = 			MyIvyResponse(	"battery_out", 				m_ivyConfig.mp3_path,	0,				0, 						0, 						1,					m_ivy_object_list, 	0);
		m_ivyEngineFire = 			MyIvyResponse(	"engine_fire", 				m_ivyConfig.mp3_path,	0,				0, 						0, 						1,					m_ivy_object_list, 	0);
		m_ivyEngineFlameout = 		MyIvyResponse(	"engine_flameout", 			m_ivyConfig.mp3_path,	0,				0, 						0, 						1,					m_ivy_object_list, 	0);
		m_ivyEngineFailureGround = 	MyIvyResponse(	"engine_failure_ground", 	m_ivyConfig.mp3_path,	1,				0, 						0, 						1,					m_ivy_object_list, 	0);
		m_ivyEngineFailureAir = 		MyIvyResponse(	"engine_failure_air", 		m_ivyConfig.mp3_path,	0,				0, 						0, 						1,					m_ivy_object_list, 	0);
		m_ivyEngineHotStart = 		MyIvyResponse(	"engine_hot", 				m_ivyConfig.mp3_path,	0,				0, 						0, 						1,					m_ivy_object_list, 	0);
		m_ivyBirdStrike = 			MyIvyResponse(	"bird", 					m_ivyConfig.mp3_path,	0,				0, 						0, 						1,					m_ivy_object_list, 	0);
 
		m_ivyOverspeedFlaps = 		MyIvyResponse(	"overspeed_flaps", 			m_ivyConfig.mp3_path,	1,				0, 						1, 						1,					m_ivy_object_list, 	0);
		m_ivyOverspeedGear = 		MyIvyResponse(	"overspeed_gear", 			m_ivyConfig.mp3_path,	1,				0, 						1, 						1,					m_ivy_object_list, 	0);
		m_ivyOverspeedAircraft = 	MyIvyResponse(	"overspeed_aircraft", 		m_ivyConfig.mp3_path,	1,				1, 						1, 						1,					m_ivy_object_list, 	0);
		m_ivyStall = 				MyIvyResponse(	"stall", 					m_ivyConfig.mp3_path,	1,				0, 						5, 						1,					m_ivy_object_list, 	0);
 
		m_ivyNoBatt = 				MyIvyResponse(	"no_batt", 					m_ivyConfig.mp3_path,	0,				180, 					0, 						0,					m_ivy_object_list, 	0);
		m_ivyHelloSun = 				MyIvyResponse(	"hello_sun", 				m_ivyConfig.mp3_path,	0,				15, 					0, 						0,					m_ivy_object_list, 	0);
		m_ivyHellorain = 			MyIvyResponse(	"hello_rain", 				m_ivyConfig.mp3_path,	0,				15, 					0, 						0,					m_ivy_object_list, 	0);
		m_ivyHelloFog = 				MyIvyResponse(	"hello_fog", 				m_ivyConfig.mp3_path,	0,				15, 					0, 						0,					m_ivy_object_list, 	0);
		m_ivyHelloNormal = 			MyIvyResponse(	"hello_normal", 			m_ivyConfig.mp3_path,	0,				15, 					0, 						0,					m_ivy_object_list, 	0);
		m_ivyCabinDownNormal = 		MyIvyResponse(	"cabin_down_normal", 		m_ivyConfig.mp3_path,	0,				2, 						0, 						1,					m_ivy_object_list, 	0);
		m_ivyCabinDownFast = 		MyIvyResponse(	"cabin_down_fast", 			m_ivyConfig.mp3_path,	0,				2, 						0, 						1,					m_ivy_object_list, 	0);
		m_ivyBankNormal = 			MyIvyResponse(	"bank_normal", 				m_ivyConfig.mp3_path,	0,				0, 						0, 						0,					m_ivy_object_list, 	0);
		m_ivyBankHigh = 				MyIvyResponse(	"bank_high", 				m_ivyConfig.mp3_path,	0,				2, 						0, 						1,					m_ivy_object_list, 	0);
		m_ivyBankXHigh = 			MyIvyResponse(	"bank_xhigh", 				m_ivyConfig.mp3_path,	0,				2, 						0, 						1,					m_ivy_object_list, 	0);
		m_ivyPitchDownNormal = 		MyIvyResponse(	"pitch_down_normal", 		m_ivyConfig.mp3_path,	0,				0, 						0, 						0,					m_ivy_object_list, 	0);
		m_ivyPitchDownHigh = 		MyIvyResponse(	"pitch_down_high", 			m_ivyConfig.mp3_path,	0,				2, 						0, 						1,					m_ivy_object_list, 	0);
		m_ivyGNormalFlightNormal = 	MyIvyResponse(	"g_normal_flight_normal", 	m_ivyConfig.mp3_path,	0,				2, 						0, 						0,					m_ivy_object_list, 	0);
		m_ivyGNormalFlightHigh = 	MyIvyResponse(	"g_normal_flight_high", 	m_ivyConfig.mp3_path,	0,				2, 						0, 						1,					m_ivy_object_list, 	0);
		m_ivyGNormalFlightXHigh = 	MyIvyResponse(	"g_normal_flight_xhigh", 	m_ivyConfig.mp3_path,	0,				2, 						0, 						1,					m_ivy_object_list, 	0);
		m_ivyGNormalNegativeLow = 	MyIvyResponse(	"g_normal_negative_low", 	m_ivyConfig.mp3_path,	0,				0.5, 					0, 						1,					m_ivy_object_list, 	0);
		m_ivyGNormalNegativeHigh = 	MyIvyResponse(	"g_normal_negative_high", 	m_ivyConfig.mp3_path,	0,				0.5, 					0, 						1,					m_ivy_object_list, 	0);
		m_ivyTurbulenceNormal = 		MyIvyResponse(	"turbulence_normal", 		m_ivyConfig.mp3_path,	0,				20, 					0, 						0,					m_ivy_object_list, 	0);
		m_ivyTurbolenceHigh = 		MyIvyResponse(	"turbulence_high", 			m_ivyConfig.mp3_path,	0,				20, 					0, 						0,					m_ivy_object_list, 	0);
 
		m_ivyLandingXGood = 			MyIvyResponse(	"landing_xgood", 			m_ivyConfig.mp3_path,	0,				5, 						0, 						0,					m_ivy_object_list, 	0);
		m_ivyLandingGood = 			MyIvyResponse(	"landing_good", 			m_ivyConfig.mp3_path,	0,				5, 						0, 						0,					m_ivy_object_list, 	0);
		m_ivyLandingNormal = 		MyIvyResponse(	"landing_normal", 			m_ivyConfig.mp3_path,	0,				5, 						0, 						0,					m_ivy_object_list, 	0);
		m_ivyLandingBad = 			MyIvyResponse(	"landing_bad", 				m_ivyConfig.mp3_path,	0,				5, 						0, 						0,					m_ivy_object_list, 	0);
		m_ivyLandingXBad = 			MyIvyResponse(	"landing_xbad", 			m_ivyConfig.mp3_path,	0,				5, 						0, 						1,					m_ivy_object_list, 	0);
 
		m_ivyBaroLow = 				MyIvyResponse(	"baro_low", 				m_ivyConfig.mp3_path,	0,				5, 						0, 						1,					m_ivy_object_list, 	0);
		m_ivyBaroGround = 			MyIvyResponse(	"baro_low", 				m_ivyConfig.mp3_path,	0,				60,						0, 						0,					m_ivy_object_list, 	0);
		m_ivyBaroHigh = 				MyIvyResponse(	"baro_high", 				m_ivyConfig.mp3_path,	0,				120,					0, 						1,					m_ivy_object_list, 	0);
		m_ivyLandingLightsHigh = 	MyIvyResponse(	"landing_lights_high", 		m_ivyConfig.mp3_path,	0,				30, 					0, 						1,					m_ivy_object_list, 	0);
		m_ivyRotate = 				MyIvyResponse(	"rotate", 					m_ivyConfig.mp3_path,	0,				0, 						0, 						0,					m_ivy_object_list, 	0);
		m_ivy60kt = 					MyIvyResponse(	"60kt", 					m_ivyConfig.mp3_path,	0,				0, 						5, 						0,					m_ivy_object_list, 	0);
		m_ivy80kt = 					MyIvyResponse(	"80kt", 					m_ivyConfig.mp3_path,	0,				0, 						5, 						0,					m_ivy_object_list, 	0);
		m_ivy100kt = 				MyIvyResponse(	"100kt", 					m_ivyConfig.mp3_path,	0,				0, 						5, 						0,					m_ivy_object_list, 	0);
		m_ivyV1 = 					MyIvyResponse(	"v1", 						m_ivyConfig.mp3_path,	0,				0, 						5, 						0,					m_ivy_object_list, 	0);
		m_ivyVR = 					MyIvyResponse(	"vr", 						m_ivyConfig.mp3_path,	0,				0, 						5, 						0,					m_ivy_object_list, 	0);
		m_ivyBelowV2 = 				MyIvyResponse(	"below_v2", 				m_ivyConfig.mp3_path,	0,				5, 						5, 						1,					m_ivy_object_list, 	0);
		m_ivyAboveV2 = 				MyIvyResponse(	"above_v2", 				m_ivyConfig.mp3_path,	0,				0, 						5, 						0,					m_ivy_object_list, 	0);
		m_ivyFlapsRetracted = 		MyIvyResponse(	"flaps_retracted", 			m_ivyConfig.mp3_path,	1,				0, 						0, 						0,					m_ivy_object_list, 	0);
		m_ivySlatsRetracted = 		MyIvyResponse(	"slats_retracted", 			m_ivyConfig.mp3_path,	1,				0, 						0, 						0,					m_ivy_object_list, 	0);
		m_ivyFlapsPosition = 		MyIvyResponse(	"flaps", 					m_ivyConfig.mp3_path,	1,				0, 						0, 						0,					m_ivy_object_list, 	0);
		m_ivySlatsPosition = 		MyIvyResponse(	"slats", 					m_ivyConfig.mp3_path,	1,				0, 						0, 						0,					m_ivy_object_list, 	0);
 
		m_ivyCrash = 				MyIvyResponse(	"crash", 					m_ivyConfig.mp3_path,	0,				3, 						0, 						1,					m_ivy_object_list, 	0);
		// TODO;
 
		m_ivyPressureLow = 			MyIvyResponse(	"pressure_low", 			m_ivyConfig.mp3_path,	0,				5, 						0, 						1,					m_ivy_object_list, 	0);
		m_ivyPressureXLow = 			MyIvyResponse(	"pressure_xlow", 			m_ivyConfig.mp3_path,	0,				1, 						0, 						1,					m_ivy_object_list, 	0);
 
		m_ivyIceWindowLow = 			MyIvyResponse(	"ice_window_low", 			m_ivyConfig.mp3_path,	0,				20, 					0, 						1,					m_ivy_object_list, 	0);
		m_ivyIceWindowHigh = 		MyIvyResponse(	"ice_window_high", 			m_ivyConfig.mp3_path,	0,				20, 					0, 						1,					m_ivy_object_list, 	0);
		m_ivyIcePropellerLow = 		MyIvyResponse(	"ice_propeller_low", 		m_ivyConfig.mp3_path,	0,				40, 					0, 						1,					m_ivy_object_list, 	0) // Inlet ice;
		m_ivyIcePropellerHigh = 		MyIvyResponse(	"ice_propeller_high", 		m_ivyConfig.mp3_path,	0,				40, 					0, 						1,					m_ivy_object_list, 	0);
		m_ivyIcePitotLow = 			MyIvyResponse(	"ice_pitot_low", 			m_ivyConfig.mp3_path,	0,				60, 					0, 						1,					m_ivy_object_list, 	0) // Ice low bei 0.05;
		m_ivyIcePitotHigh = 			MyIvyResponse(	"ice_pitot_high", 			m_ivyConfig.mp3_path,	0,				60, 					0, 						1,					m_ivy_object_list, 	0);
		m_ivyIceAirframeLow = 		MyIvyResponse(	"ice_airframe_low", 		m_ivyConfig.mp3_path,	0,				100, 					0, 						1,					m_ivy_object_list, 	0) // Ice high bei 0.15;
		m_ivyIceAirframeHigh = 		MyIvyResponse(	"ice_airframe_high", 		m_ivyConfig.mp3_path,	0,				100, 					0, 						1,					m_ivy_object_list, 	0);
 
		m_ivyAnnounceTakeOff = 		MyIvyResponse(	"takeoff", 					m_ivyConfig.mp3_path,	0,				0, 						0, 						0,					m_ivy_object_list, 	0);
		m_ivyAnnounceLanding = 		MyIvyResponse(	"landing", 					m_ivyConfig.mp3_path,	0,				0, 						0, 						0,					m_ivy_object_list, 	0);
 
		m_ivySeatBelts = 			MyIvyResponse(	"seatbelts", 				m_ivyConfig.mp3_path,	0,				1, 						0, 						0,					m_ivy_object_list, 	0);
 
		m_ivyMinimums = 				MyIvyResponse(	"minimums", 				m_ivyConfig.mp3_path,	0,				0, 						10, 					0,					m_ivy_object_list, 	0);
		m_ivyApplause = 				MyIvyResponse(	"passenger_applause", 		m_ivyConfig.mp3_path,	1,				5, 						30, 					0,					m_ivy_object_list, 	1);
 
		// No Callout Events;
		m_ivyArmLanding = 			MyIvyResponse(	"arm_landing", 				m_ivyConfig.mp3_path,	0,				1, 						0, 						0,					m_ivy_object_list, 	0);
		m_ivyArmMinimums = 			MyIvyResponse(	"arm_descent", 				m_ivyConfig.mp3_path,	0,				1, 						10, 					0,					m_ivy_object_list, 	0);
 
 
		//m_ivy = 		MyIvyResponse(	"landing_lights", 		m_ivyConfig.mp3_path,	0,			0, 						0, 						0,					m_ivy_object_list);
 
 
		m_f_g_normal_max = 1;
		m_f_g_side_max = 0;
		m_f_g_forward_max = 0;
 
		m_f_g_normal_min = 1;
		m_f_g_side_min = 0;
		m_f_g_forward_min = 0;
 
		m_f_g_normal_delta = 0;
		m_f_g_side_delta = 0;
		m_f_g_forward_delta = 0;
 
		m_f_g_normal_old = 1;
		m_f_g_side_old = 0;
		m_f_g_forward_old = 0;
 
		m_li_on_ground_old = 1;
		//m_Clicked = 0;
 
		m_cab_press_rate = 0.0;
		m_cab_press_old = 0.0;
 
		m_show_output = 1;
 
 
 
 
		////////////////////////////////////////////////////////////////////////// DEBUG;
		for obj_number in range(0,len(m_ivy_object_list)){
			buf = "IvyObject{ " + m_ivy_object_list[obj_number].event_name + " Number of Soundfiles{ " + str(len(m_ivy_object_list[obj_number].play_files)) + "\n\r";
			m_OutputFile.write(buf);
		m_OutputFile.flush();
		////////////////////////////////////////////////////////////////////////// END DEBUG;
 
		////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
		// Register Flight Callback;
 
		m_FlightLoopCB = m_FlightLoopCallback;
 
		XPLMRegisterFlightLoopCallback(self, m_FlightLoopCB, m_ivyConfig.data_rate, 0);
 
		////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
		// Register Command Callbacks;
 
		m_SayBaroCB 				= m_SayBaroCallback;
		m_ResetIvyCB 			= m_ResetIvyCallback;
		m_SayWindCB				= m_SayWindCallback;
		m_ToogleWindowCB			= m_ToogleWindowCallback;
		m_AnnouncementCB			= m_AnnouncementCallback;
 
		m_CmdSayBaro 			= XPLMCreateCommand ( "Ivy/say_baro" 	, "Ask Ivy to tell you the barometric pressure" );
		m_CmdSayWind 			= XPLMCreateCommand ( "Ivy/say_wind" 	, "Ivy holds out a finger && tells you the current wind direction plus speed" );
		m_CmdToogleWindow		= XPLMCreateCommand ( "Ivy/show_output" , "Shows the loaded aircraft name, IvyAircraft name, && slats/flaps datarefs from the IvyAircraft ini for custom aircraft config" );
		m_CmdResetIvy 			= XPLMCreateCommand ( "Ivy/reset_ivy" 	, "Reset Ivy" );
		m_CmdAnnouncement		= XPLMCreateCommand ( "Ivy/cabin_announcement" 	, "Tell Ivy to make a cabin announcement" );
 
		XPLMRegisterCommandHandler 	( self , 	m_CmdSayBaro , 		m_SayBaroCB 		, 0 , 0 );
		XPLMRegisterCommandHandler 	( self , 	m_CmdResetIvy , 		m_ResetIvyCB 	, 0 , 0 );
		XPLMRegisterCommandHandler 	( self , 	m_CmdSayWind , 		m_SayWindCB 		, 0 , 0 );
		XPLMRegisterCommandHandler 	( self , 	m_CmdToogleWindow , 	m_ToogleWindowCB , 0 , 0 );
		XPLMRegisterCommandHandler 	( self , 	m_CmdAnnouncement , 	m_AnnouncementCB , 0 , 0 );
 
		// Menu;
		m_IvyMenu = XPLMAppendMenuItem(XPLMFindPluginsMenu(), "Ivy", 0, 1);
		m_ShowLogMenuHandlerCB = m_IvyMenuHandler;
		m_MenuId = XPLMCreateMenu(self, "Ivy", XPLMFindPluginsMenu(), m_IvyMenu, m_ShowLogMenuHandlerCB, 0);
		XPLMAppendMenuItem(m_MenuId, "Show Logbook", 1, 1);
		XPLMAppendMenuItem(m_MenuId, "Set V-Speeds", 2, 1);
		XPLMAppendMenuItem(m_MenuId, "Make Announcement", 3, 1);
		XPLMAppendMenuItem(m_MenuId, "Barometric Pressure", 4, 1);
		XPLMAppendMenuItem(m_MenuId, "Wind Situtation", 5, 1);
		XPLMAppendMenuItem(m_MenuId, "Show Output", 6, 1);
		XPLMAppendMenuItem(m_MenuId, "Reset Ivy", 7, 1);
 
		// Flag to tell us if theLogbook is shown;
		m_MenuLogbookShow = 0;
 
 
		//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
		//;
		//						DATAREF Find;
		//;
		//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
 
 
 
		m_i_on_ground = 				XPLMFindDataRef("sim/flightmodel/failures/onground_any");
		m_f_climb_rate = 			XPLMFindDataRef("sim/flightmodel/position/vh_ind_fpm");
 
		m_f_gear1_ratio = 			XPLMFindDataRef("sim/flightmodel/movingparts/gear1def");
		m_f_gear2_ratio = 			XPLMFindDataRef("sim/flightmodel/movingparts/gear2def");
		m_f_gear3_ratio = 			XPLMFindDataRef("sim/flightmodel/movingparts/gear3def");
		m_f_gear4_ratio = 			XPLMFindDataRef("sim/flightmodel/movingparts/gear4def");
		m_f_gear5_ratio = 			XPLMFindDataRef("sim/flightmodel/movingparts/gear5def");
 
		m_f_ground_speed = 			XPLMFindDataRef("sim/flightmodel/position/groundspeed");
		m_f_ias = 					XPLMFindDataRef("sim/flightmodel/position/indicated_airspeed");
		m_f_sun_pitch = 				XPLMFindDataRef("sim/graphics/scenery/sun_pitch_degrees");
		m_f_airport_light = 			XPLMFindDataRef("sim/graphics/scenery/airport_light_level") //0-1;
		m_f_world_light_precent = 	XPLMFindDataRef("sim/graphics/scenery/percent_lights_on");
		m_i_has_skid = 				XPLMFindDataRef("sim/aircraft/gear/acf_gear_is_skid");
		m_i_transponder_mode = 		XPLMFindDataRef("sim/cockpit/radios/transponder_mode") // on = 3;
		m_i_sim_ground_speed = 		XPLMFindDataRef("sim/time/ground_speed");
 
		m_i_temp_sl = 				XPLMFindDataRef("sim/weather/temperature_sealevel_c") // Td ~ T - (100-RH)/5 where Td is the dew point, T is temperature, RH is relative humidity;
		m_i_dew_sl = 				XPLMFindDataRef("sim/weather/dewpoi_sealevel_c");
 
		m_i_landing_lights = 		XPLMFindDataRef("sim/cockpit/electrical/landing_lights_on");
		m_i_beacon_lights = 			XPLMFindDataRef("sim/cockpit/electrical/beacon_lights_on");
		m_i_nav_lights = 			XPLMFindDataRef("sim/cockpit/electrical/nav_lights_on");
		m_i_strobe_lights = 			XPLMFindDataRef("sim/cockpit/electrical/strobe_lights_on");
		m_i_taxi_lights = 			XPLMFindDataRef("sim/cockpit/electrical/taxi_light_on");
		m_i_cockpit_lights = 		XPLMFindDataRef("sim/cockpit/electrical/cockpit_lights_on");
		m_f_radio_alt = 				XPLMFindDataRef("sim/cockpit2/gauges/indicators/radio_altimeter_height_ft_pilot");
		m_f_decision_height = 		XPLMFindDataRef("sim/cockpit/misc/radio_altimeter_minimum");
		m_f8_batter_charge = 		XPLMFindDataRef("sim/cockpit/electrical/battery_charge_watt_hr");
		m_i_battery_on = 			XPLMFindDataRef("sim/cockpit/electrical/battery_on");
		m_i_gpu_on = 				XPLMFindDataRef("sim/cockpit/electrical/gpu_on");
 
		m_i_flaps_overspeed = 		XPLMFindDataRef("sim/flightmodel/failures/over_vfe");
		m_i_gear_overspeed = 		XPLMFindDataRef("sim/flightmodel/failures/over_vle");
		m_f_aircraft_vne 		= 	XPLMFindDataRef("sim/aircraft/view/acf_Vne");
		m_i_aircraft_overspeed = 	XPLMFindDataRef("sim/flightmodel/failures/over_vne");
		m_i_stall = 					XPLMFindDataRef("sim/flightmodel/failures/stallwarning");
 
		m_i_cloud_0 = 				XPLMFindDataRef("sim/weather/cloud_type[0]");
		m_i_cloud_1 = 				XPLMFindDataRef("sim/weather/cloud_type[0]");
		m_i_cloud_2 = 				XPLMFindDataRef("sim/weather/cloud_type[0]");
		m_f_visibility = 			XPLMFindDataRef("sim/weather/visibility_reported_m");
		m_i_rain = 					XPLMFindDataRef("sim/weather/rain_percent");
		m_i_thunder = 				XPLMFindDataRef("sim/weather/thunderstorm_percent");
		m_i_turbulence = 			XPLMFindDataRef("sim/weather/wind_turbulence_percent");
 
		m_i_batt1 = 					XPLMFindDataRef("sim/operation/failures/rel_bat0_lo");
		m_i_batt2 = 					XPLMFindDataRef("sim/operation/failures/rel_bat1_lo");
 
		m_i_tire1 = 					XPLMFindDataRef("sim/operation/failures/rel_tire1") //eight;
		m_i_tire2 = 					XPLMFindDataRef("sim/operation/failures/rel_tire2");
		m_i_tire3 = 					XPLMFindDataRef("sim/operation/failures/rel_tire3");
		m_i_tire4 = 					XPLMFindDataRef("sim/operation/failures/rel_tire4");
		m_i_tire5 = 					XPLMFindDataRef("sim/operation/failures/rel_tire5");
 
		m_i_fire1 = 					XPLMFindDataRef("sim/operation/failures/rel_engfir0") //multiple;
		m_i_fire2 = 					XPLMFindDataRef("sim/operation/failures/rel_engfir1");
		m_i_fire3 = 					XPLMFindDataRef("sim/operation/failures/rel_engfir2");
		m_i_fire4 = 					XPLMFindDataRef("sim/operation/failures/rel_engfir3");
		m_i_fire5 =					XPLMFindDataRef("sim/operation/failures/rel_engfir4");
		m_i_fire6 = 					XPLMFindDataRef("sim/operation/failures/rel_engfir5");
		m_i_fire7 = 					XPLMFindDataRef("sim/operation/failures/rel_engfir6");
		m_i_fire8 = 					XPLMFindDataRef("sim/operation/failures/rel_engfir7");
 
		m_i_flameout1 = 				XPLMFindDataRef("sim/operation/failures/rel_engfla0") //multiple;
		m_i_flameout2 = 				XPLMFindDataRef("sim/operation/failures/rel_engfla1");
		m_i_flameout3 = 				XPLMFindDataRef("sim/operation/failures/rel_engfla2");
		m_i_flameout4 =				XPLMFindDataRef("sim/operation/failures/rel_engfla3");
		m_i_flameout5 = 				XPLMFindDataRef("sim/operation/failures/rel_engfla4");
		m_i_flameout6 = 				XPLMFindDataRef("sim/operation/failures/rel_engfla5");
		m_i_flameout7 = 				XPLMFindDataRef("sim/operation/failures/rel_engfla6");
		m_i_flameout8 = 				XPLMFindDataRef("sim/operation/failures/rel_engfla7");
 
 
 
		m_i_engine_failure1 = 		XPLMFindDataRef("sim/operation/failures/rel_engfai0") //multiple;
		m_i_engine_failure2 = 		XPLMFindDataRef("sim/operation/failures/rel_engfai1");
		m_i_engine_failure3 = 		XPLMFindDataRef("sim/operation/failures/rel_engfai2");
		m_i_engine_failure4 = 		XPLMFindDataRef("sim/operation/failures/rel_engfai3");
		m_i_engine_failure5 = 		XPLMFindDataRef("sim/operation/failures/rel_engfai4");
		m_i_engine_failure6 = 		XPLMFindDataRef("sim/operation/failures/rel_engfai5");
		m_i_engine_failure7 = 		XPLMFindDataRef("sim/operation/failures/rel_engfai6");
		m_i_engine_failure8 = 		XPLMFindDataRef("sim/operation/failures/rel_engfai7");
 
		m_i_hot1 = 					XPLMFindDataRef("sim/operation/failures/rel_hotsta0") //multiple;
		m_i_hot2 = 					XPLMFindDataRef("sim/operation/failures/rel_hotsta1");
		m_i_hot3 = 					XPLMFindDataRef("sim/operation/failures/rel_hotsta2");
		m_i_hot4 = 					XPLMFindDataRef("sim/operation/failures/rel_hotsta3");
		m_i_hot5 = 					XPLMFindDataRef("sim/operation/failures/rel_hotsta4");
		m_i_hot6 = 					XPLMFindDataRef("sim/operation/failures/rel_hotsta5");
		m_i_hot7 = 					XPLMFindDataRef("sim/operation/failures/rel_hotsta6");
		m_i_hot8 = 					XPLMFindDataRef("sim/operation/failures/rel_hotsta7");
 
		m_f_ice_frame = 				XPLMFindDataRef("sim/flightmodel/failures/frm_ice");
		m_f_ice_pitot = 				XPLMFindDataRef("sim/flightmodel/failures/pitot_ice");
		m_f_ice_propeller = 			XPLMFindDataRef("sim/flightmodel/failures/prop_ice");
		m_f_ice_window = 			XPLMFindDataRef("sim/flightmodel/failures/window_ice");
 
		m_f_g_normal = 				XPLMFindDataRef("sim/flightmodel/forces/g_nrml");
		m_f_g_forward = 				XPLMFindDataRef("sim/flightmodel/forces/g_axil");
		m_f_g_side = 				XPLMFindDataRef("sim/flightmodel/forces/g_side");
 
		m_i_bird = 					XPLMFindDataRef("sim/operation/failures/rel_bird_strike");
 
 
		m_f_pitch = 					XPLMFindDataRef("sim/flightmodel/position/theta");
		m_f_roll = 					XPLMFindDataRef("sim/flightmodel/position/phi");
		m_f_yaw = 					XPLMFindDataRef("sim/flightmodel/position/beta");
 
		//cab press;
		m_f_cab_press = 				XPLMFindDataRef("sim/cockpit/pressure/cabin_altitude_actual_m_msl") // meter?;
		//cab climb rate;
		m_f_cab_rate = 				XPLMFindDataRef("sim/cockpit/pressure/cabin_vvi_actual_m_msec") // meter per second? 1000ft/min = 5m/s;
		//cab humidity;
		//cab temp;
 
		m_f_outside_temp1 = 			XPLMFindDataRef("sim/weather/temperature_ambient_c");
		m_f_outside_temp2 = 			XPLMFindDataRef("sim/cockpit2/temperature/outside_air_temp_degc");
		m_f_outside_temp3 = 			XPLMFindDataRef("sim/cockpit2/temperature/outside_air_LE_temp_degc");
 
		m_f_baro_set =	 			XPLMFindDataRef("sim/cockpit/misc/barometer_setting");
		m_f_baro_sea_level =			XPLMFindDataRef("sim/weather/barometer_sealevel_inhg");
		m_f_baro_alt =				XPLMFindDataRef("sim/flightmodel/misc/h_ind");
 
		m_f_wind_direction = 		XPLMFindDataRef("sim/weather/wind_direction_degt");
		m_f_wind_speed_kt = 			XPLMFindDataRef("sim/weather/wind_speed_kt");
 
		m_f_slats_1 =		    	XPLMFindDataRef("sim/flightmodel2/controls/slat1_deploy_ratio");
		m_f_flaps_1 =		    	XPLMFindDataRef("sim/flightmodel2/controls/flap1_deploy_ratio");
 
		m_d_latitude	=				XPLMFindDataRef("sim/flightmodel/position/latitude");
		m_d_longitude =				XPLMFindDataRef("sim/flightmodel/position/longitude");
 
		m_i_nonsmoking = 			XPLMFindDataRef("sim/cockpit/switches/no_smoking");
		m_i_fastenseatbelt = 		XPLMFindDataRef("sim/cockpit/switches/fasten_seat_belts");
 
		m_i_replay = 				XPLMFindDataRef("sim/operation/prefs/replay_mode");
 
		////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// End of DATAREF Find;
 
		//m_ReadData() // Read data for the first time to ensure window handler can process valid data from the start;
 
		m_data_read_valid = false;
 
		m_DrawWindowCB = m_DrawWindowCallback;
		m_KeyCB = m_KeyCallback;
		m_MouseClickCB = m_MouseClickCallback;
		m_WindowId = XPLMCreateWindow(self, 10, 200, 500, 500, 1, m_DrawWindowCB, m_KeyCB, m_MouseClickCB, 0);
 
		// Make sure file exists;
		logbook_file 	= open(m_ivyConfig.logbook_path, 'a+');
		logbook_file.close();
 
 
		return m_Name, m_Sig, m_Desc;
 
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
	// VSpeeds Functions following;
	def CreateVSpeedsWidget(self){
		x=300;
		y=300;
		x2=x+200;
		y2=y-200;
 
		m_VSpeedsWidget = XPCreateWidget(x, y, x2, y2, 1, "Ivy VSpeeds", 1,	0, xpWidgetClass_MainWindow);
 
 
		// Add Close Box decorations to the Main Widget;
		XPSetWidgetProperty(m_VSpeedsWidget, xpProperty_MainWindowHasCloseBoxes, 1);
 
		m_v1_label = XPCreateWidget(x+10, y-25, x+50, y-40, 1,	"V1{",  0, m_VSpeedsWidget, xpWidgetClass_Caption);
		m_vr_label = XPCreateWidget(x+10, y-45, x+50, y-60, 1,	"VR{",  0, m_VSpeedsWidget, xpWidgetClass_Caption);
		m_v2_label = XPCreateWidget(x+10, y-65, x+50, y-80, 1,	"V2{",  0, m_VSpeedsWidget, xpWidgetClass_Caption);
		m_dh_label = XPCreateWidget(x+10, y-85, x+50, y-100, 1,	"DH{",  0, m_VSpeedsWidget, xpWidgetClass_Caption);
 
		m_kt60_label  = XPCreateWidget(x+10, y-105, x+50, y-120, 1,	"60kt{",  0, m_VSpeedsWidget, xpWidgetClass_Caption);
		m_kt80_label  = XPCreateWidget(x+10, y-125, x+50, y-140, 1,	"80kt{",  0, m_VSpeedsWidget, xpWidgetClass_Caption);
		m_kt100_label = XPCreateWidget(x+10, y-145, x+50, y-160, 1,	"100kt{",  0, m_VSpeedsWidget, xpWidgetClass_Caption);
 
		m_v1_label_val = XPCreateWidget(x+50, y-25, x+80, y-40, 1,	str(m_ivyAircraft.li_v1),  		0, m_VSpeedsWidget, xpWidgetClass_Caption);
		m_vr_label_val = XPCreateWidget(x+50, y-45, x+80, y-60, 1,	str(m_ivyAircraft.li_vr),  		0, m_VSpeedsWidget, xpWidgetClass_Caption);
		m_v2_label_val = XPCreateWidget(x+50, y-65, x+80, y-80, 1,	str(m_ivyAircraft.li_v2),  		0, m_VSpeedsWidget, xpWidgetClass_Caption);
		m_dh_label_val = XPCreateWidget(x+50, y-85, x+80, y-100, 1,	str(int(m_lf_decision_height)),  0, m_VSpeedsWidget, xpWidgetClass_Caption);
 
		m_v1_textbox = XPCreateWidget(x+80, y-30, x+120, y-40, 1,	str(m_ivyAircraft.li_v1),  		0, m_VSpeedsWidget, xpWidgetClass_TextField);
		m_vr_textbox = XPCreateWidget(x+80, y-50, x+120, y-60, 1,	str(m_ivyAircraft.li_vr),  		0, m_VSpeedsWidget, xpWidgetClass_TextField);
		m_v2_textbox = XPCreateWidget(x+80, y-70, x+120, y-80, 1,	str(m_ivyAircraft.li_v2),  		0, m_VSpeedsWidget, xpWidgetClass_TextField);
		m_dh_textbox = XPCreateWidget(x+80, y-90, x+120, y-100, 1,	str(int(m_lf_decision_height)), 	0, m_VSpeedsWidget, xpWidgetClass_TextField);
 
		XPSetWidgetProperty(m_v1_textbox, xpProperty_TextFieldType, xpTextEntryField);
		XPSetWidgetProperty(m_vr_textbox, xpProperty_TextFieldType, xpTextEntryField);
		XPSetWidgetProperty(m_v2_textbox, xpProperty_TextFieldType, xpTextEntryField);
		XPSetWidgetProperty(m_dh_textbox, xpProperty_TextFieldType, xpTextEntryField);
 
		XPSetWidgetProperty (m_v1_textbox, xpProperty_Enabled , 1 );
		XPSetWidgetProperty (m_vr_textbox, xpProperty_Enabled , 1 );
		XPSetWidgetProperty (m_v2_textbox, xpProperty_Enabled , 1 );
		XPSetWidgetProperty (m_dh_textbox, xpProperty_Enabled , 1 );
 
		m_v1_button = XPCreateWidget(x+140, y-30, x+180, y-40, 1,	"Set",  0, m_VSpeedsWidget, xpWidgetClass_Button);
		m_vr_button = XPCreateWidget(x+140, y-50, x+180, y-60, 1,	"Set",  0, m_VSpeedsWidget, xpWidgetClass_Button);
		m_v2_button = XPCreateWidget(x+140, y-70, x+180, y-80, 1,	"Set",  0, m_VSpeedsWidget, xpWidgetClass_Button);
		m_dh_button = XPCreateWidget(x+140, y-90, x+180, y-100, 1,	"Set",  0, m_VSpeedsWidget, xpWidgetClass_Button);
 
		m_kt60_button = XPCreateWidget(x+55, y-110, x+65, y-120, 1,	"",  0, m_VSpeedsWidget, xpWidgetClass_Button);
		XPSetWidgetProperty(m_kt60_button, xpProperty_ButtonType, xpRadioButton);
		XPSetWidgetProperty(m_kt60_button, xpProperty_ButtonBehavior, xpButtonBehaviorCheckBox);
		if (m_ivyConfig.kt60_enabled == true){ 	XPSetWidgetProperty(m_kt60_button, xpProperty_ButtonState, 1);
		else{										XPSetWidgetProperty(m_kt60_button, xpProperty_ButtonState, 0);
 
		m_kt80_button = XPCreateWidget(x+55, y-130, x+65, y-140, 1,	"",  0, m_VSpeedsWidget, xpWidgetClass_Button);
		XPSetWidgetProperty(m_kt80_button, xpProperty_ButtonType, xpRadioButton);
		XPSetWidgetProperty(m_kt80_button, xpProperty_ButtonBehavior, xpButtonBehaviorCheckBox);
		if (m_ivyConfig.kt80_enabled == true){ 	XPSetWidgetProperty(m_kt80_button, xpProperty_ButtonState, 1);
		else{										XPSetWidgetProperty(m_kt80_button, xpProperty_ButtonState, 0);
 
		m_kt100_button = XPCreateWidget(x+55, y-150, x+65, y-160, 1,	"",  0, m_VSpeedsWidget, xpWidgetClass_Button);
		XPSetWidgetProperty(m_kt100_button, xpProperty_ButtonType, xpRadioButton);
		XPSetWidgetProperty(m_kt100_button, xpProperty_ButtonBehavior, xpButtonBehaviorCheckBox);
		if (m_ivyConfig.kt100_enabled == true){ 	XPSetWidgetProperty(m_kt100_button, xpProperty_ButtonState, 1);
		else{										XPSetWidgetProperty(m_kt100_button, xpProperty_ButtonState, 0);
 
 
 
		m_IvyVSpeedHandlerCB = m_IvyVSpeedHandler;
		XPAddWidgetCallback(self, m_VSpeedsWidget, m_IvyVSpeedHandlerCB);
 
		pass;
 
 
 
 
	def IvyVSpeedHandler(self, inMessage, inWidget,	inParam1, inParam2){
		if (inMessage == xpMessage_CloseButtonPushed){
			if (m_MenuVSpeedsShow == 1){
				XPDestroyWidget(self, m_VSpeedsWidget, 1);
				m_MenuVSpeedsShow = 0;
			return 1;
 
		if (inMessage == xpMsg_PushButtonPressed){
			if (inParam1 == m_v1_button){
				buffer = [];
				XPGetWidgetDescriptor(m_v1_textbox, buffer, 256);
				text = buffer[0];
				if (text.isdigit() == true){ m_ivyAircraft.li_v1 = int(text);
				XPSetWidgetDescriptor(m_v1_textbox,   str(m_ivyAircraft.li_v1));
				XPSetWidgetDescriptor(m_v1_label_val, str(m_ivyAircraft.li_v1));
 
			if (inParam1 == m_vr_button){
				buffer = [];
				XPGetWidgetDescriptor(m_vr_textbox, buffer, 256);
				text = buffer[0];
				if (text.isdigit() == true){ m_ivyAircraft.li_vr = int(text);
				XPSetWidgetDescriptor(m_vr_textbox,   str(m_ivyAircraft.li_vr));
				XPSetWidgetDescriptor(m_vr_label_val, str(m_ivyAircraft.li_vr));
 
			if (inParam1 == m_v2_button){
				buffer = [];
				XPGetWidgetDescriptor(m_v2_textbox, buffer, 256);
				text = buffer[0];
				if (text.isdigit() == true){ m_ivyAircraft.li_v2 = int(text);
				XPSetWidgetDescriptor(m_v2_textbox,   str(m_ivyAircraft.li_v2));
				XPSetWidgetDescriptor(m_v2_label_val, str(m_ivyAircraft.li_v2));
 
			if (inParam1 == m_dh_button){
				buffer = [];
				XPGetWidgetDescriptor(m_dh_textbox, buffer, 256);
				text = buffer[0];
				if (text.isdigit() == true){
					dh_new = float(int(text));
					XPLMSetDataf(m_f_decision_height, dh_new);
					m_lf_decision_height = XPLMGetDataf(m_f_decision_height);
				XPSetWidgetDescriptor(m_dh_textbox,   str(int(m_lf_decision_height)));
				XPSetWidgetDescriptor(m_dh_label_val, str(int(m_lf_decision_height)));
 
		if (inMessage == xpMsg_ButtonStateChanged){
			if (inParam1 == m_kt60_button){
				if (XPGetWidgetProperty(m_kt60_button, xpProperty_ButtonState, None) == 1){			m_ivyConfig.kt60_enabled = true;
				else{																					m_ivyConfig.kt60_enabled = false;
 
			if (inParam1 == m_kt80_button){
				if (XPGetWidgetProperty(m_kt80_button, xpProperty_ButtonState, None) == 1){			m_ivyConfig.kt80_enabled = true;
				else{																					m_ivyConfig.kt80_enabled = false;
 
			if (inParam1 == m_kt100_button){
				if (XPGetWidgetProperty(m_kt100_button, xpProperty_ButtonState, None) == 1){			m_ivyConfig.kt100_enabled = true;
				else{																					m_ivyConfig.kt100_enabled = false;
 
 
		return 0;
		pass;
 
 
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
	// Logbook Widget Functions following;
 
	def CreateLogbookWidget(self, x, y, w, h){
		x2 = x + w;
		y2 = y - h;
 
		// Create the Main Widget window;
		m_LogbookWidget = XPCreateWidget(x, y, x2, y2, 1, "Ivy Loogbook", 1,	0, xpWidgetClass_MainWindow);
		m_IvyLogbookHandlerCB = m_IvyLogbookHandler;
		XPAddWidgetCallback(self, m_LogbookWidget, m_IvyLogbookHandlerCB);
 
		// Add Close Box decorations to the Main Widget;
		XPSetWidgetProperty(m_LogbookWidget, xpProperty_MainWindowHasCloseBoxes, 1);
		logbookstring = "test1; test2\n\r test3";
 
		m_logbook_lines = int(m_ivyConfig.log_window_entries);
		m_logbook_index = 0;
		m_text_field_array = [];
		m_logbook_entries = [];
 
		logbook_file = open(m_ivyConfig.logbook_path, 'a+');
		m_logbook_entries = logbook_file.readlines();
		logbook_file.close();
 
		m_LogbookScrollBar = XPCreateWidget(x2-10, y-20, x2-5, y2, 1,	"",	0, m_LogbookWidget, xpWidgetClass_ScrollBar);
		XPSetWidgetProperty(m_LogbookScrollBar, xpProperty_ScrollBarMin, 0);
		XPSetWidgetProperty(m_LogbookScrollBar, xpProperty_ScrollBarMax, max(len(m_logbook_entries)+2, 0));
		XPSetWidgetProperty(m_LogbookScrollBar, xpProperty_ScrollBarPageAmount, m_logbook_lines);
		XPSetWidgetProperty(m_LogbookScrollBar, xpProperty_ScrollBarSliderPosition, min(m_logbook_lines,len(m_logbook_entries))) // Set page to show last flight max(len(m_logbook_entries), m_logbook_lines);
 
		m_IvyScrollbarHandlerCB = m_IvyLogbookScrollHandler;
		XPAddWidgetCallback(self, m_LogbookScrollBar, m_IvyScrollbarHandlerCB);
 
		for index in range (0,m_logbook_lines){
			m_text_field_array.append(XPCreateWidget(x+5, y-(30 + (index*20)), x2-15, y-(40 + (index*20)), 1,	"test" + str(index),  0, m_LogbookWidget, xpWidgetClass_TextField));
			//subwindow =                  XPCreateWidget(x+5, y-(50 + (index*20)), x2-15, y-(60 + (index*20)),1, "",	0, m_LogbookWidget, xpWidgetClass_SubWindow);
			//XPSetWidgetProperty(subwindow, xpProperty_SubWindowType, xpSubWindowStyle_SubWindow);
 
 
 
		// Text Draw;
		m_IvyFillLogbook();
 
 
		pass;
 
	def IvyLogbookHandler(self, inMessage, inWidget,	inParam1, inParam2){
		if (inMessage == xpMessage_CloseButtonPushed){
			if (m_MenuLogbookShow == 1){
				XPDestroyWidget(self, m_LogbookWidget, 1);
				m_MenuLogbookShow = 0;
			return 1;
 
		return 0;
		pass;
 
	def IvyLogbookScrollHandler(self, inMessage, inWidget,	inParam1, inParam2){
		if (inMessage == xpMsg_ScrollBarSliderPositionChanged){
			m_IvyFillLogbook();
			return 1;
		return 0;
		pass;
 
 
 
	def IvyFillLogbook(self){
		m_logbook_index = max(len(m_logbook_entries) - XPGetWidgetProperty(m_LogbookScrollBar, xpProperty_ScrollBarSliderPosition, None),0);
		for index in range(0,len(m_text_field_array)){
			text_index = index + m_logbook_index;
			if (text_index < len(m_logbook_entries)){
				XPSetWidgetDescriptor(m_text_field_array[index], m_logbook_entries[text_index]);
			else{
				XPSetWidgetDescriptor(m_text_field_array[index], "");
 
		pass;
 
 
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
	// Utility Functions following;
 
	def XPluginStop(self){
		XPLMUnregisterFlightLoopCallback	(self, 		m_FlightLoopCB, 		0);
		XPLMUnregisterCommandHandler 		( self , 	m_CmdSayBaro , 		m_SayBaroCB , 		0 , 0 );
		XPLMUnregisterCommandHandler 		( self , 	m_CmdResetIvy , 		m_ResetIvyCB , 		0 , 0 );
		XPLMUnregisterCommandHandler 		( self , 	m_CmdSayWind , 		m_SayWindCB 		, 	0 , 0 );
		XPLMUnregisterCommandHandler 		( self , 	m_CmdToogleWindow , 	m_ToogleWindowCB , 	0 , 0 );
		XPLMUnregisterCommandHandler 		( self , 	m_CmdAnnouncement , 	m_AnnouncementCB , 	0 , 0 );
		XPLMDestroyWindow(self, m_WindowId);
		XPLMDestroyMenu(self, m_MenuId);
		//XPLMDestroyMenu(self, m_IvyMenu);
 
		if (m_MenuLogbookShow == 1){ XPDestroyWidget(self, m_LogbookWidget, 1);
		if (m_MenuVSpeedsShow == 1){ XPDestroyWidget(self, m_VSpeedsWidget, 1);
		m_OutputFile.close();
		m_ivyConfig.WriteConfig();
		pass;
 
	def XPluginEnable(self){
		m_plugin_enabled = 1;
		return 1;
 
 
	def XPluginDisable(self){
		m_plugin_enabled = 0;
		pass;
 
 
	def XPluginReceiveMessage(self, inFromWho, inMessage, inParam){
 
		if (inFromWho == XPLM_PLUGIN_XPLANE){
			if (inMessage == XPLM_MSG_PLANE_LOADED){
				m_aircraft_loaded = 1;
				m_no_aircraft = false;
				m_ResetIvy();
			if (inMessage == XPLM_MSG_AIRPorT_LOADED){
				m_aircraft_loaded = 1;
				m_no_aircraft = false;
				m_ResetIvy();
			if (inMessage == XPLM_MSG_PLANE_CRASHED){
				m_aircraft_crashed = 1;
		pass;
 
 
 
	def DrawWindowCallback(self, inWindowID, inRefcon){
 
		lLeft = [];	lTop = []; lRight = [];	lBottom = [];
		XPLMGetWindowGeometry(inWindowID, lLeft, lTop, lRight, lBottom);
		left = int(lLeft[0]); top = int(lTop[0]); right = int(lRight[0]); bottom = int(lBottom[0]);
 
		color = 1.0, 1.0, 1.0;
 
		if (m_data_read_valid == true) && (m_draw_window == 1){
 
			XPLMDrawTranslucentDarkBox(left, top, right, bottom);
			XPLMDrawString(color, left + 5, top - 10, "Aircraft Name{    " + str(m_ls_acf_descrip), 0, xplmFont_Basic);
			XPLMDrawString(color, left + 5, top - 20, "IvyAircraft Name{ " + str(m_ivyAircraft.name), 0, xplmFont_Basic);
			XPLMDrawString(color, left + 5, top - 30, "Slats position{ 	 " + str(m_ivyAircraft.lf_slats), 0, xplmFont_Basic);
			XPLMDrawString(color, left + 5, top - 40, "Flaps position{   " + str(m_ivyAircraft.lf_flaps), 0, xplmFont_Basic);
			XPLMDrawString(color, left + 5, top - 50, "V1{               " + str(m_ivyAircraft.li_v1), 0, xplmFont_Basic);
			XPLMDrawString(color, left + 5, top - 60, "VR{               " + str(m_ivyAircraft.li_vr), 0, xplmFont_Basic);
			XPLMDrawString(color, left + 5, top - 70, "V2{               " + str(m_ivyAircraft.li_v2), 0, xplmFont_Basic);
			XPLMDrawString(color, left + 5, top - 80, "Decision Height{  " + str(int(m_lf_decision_height)), 0, xplmFont_Basic);
			//XPLMDrawString(color, left + 5, top - 90, "Debug1{           " + str(m_lf_cab_rate), 0, xplmFont_Basic);
			//XPLMDrawString(color, left + 5, top -100, "Debug2{           " + str(m_lf_cab_press), 0, xplmFont_Basic);
			//XPLMDrawString(color, left + 5, top -110, "Debug3{           " + str(m_lf_climb_rate), 0, xplmFont_Basic);
 
// For Debug;
//		if ((m_li_on_ground == 0) && (m_lf_radio_alt > (m_lf_decision_height + m_ivyConfig.decition_height_arm))){
//			XPLMDrawString(color, left + 5, top - 100, "Statement true", 0, xplmFont_Basic);
//		else{
//			XPLMDrawString(color, left + 5, top - 100, "Statement false", 0, xplmFont_Basic);
 
 
		return 0;
 
 
	def KeyCallback(self, inWindowID, inKey, inFlags, inVirtualKey, inRefcon, losingFocus){
		return 0;
 
 
	def MouseClickCallback(self, inWindowID, x, y, inMouse, inRefcon){
		return 0;
 
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
	// Callback Functions;
 
	def IvyMenuHandler(self, inMenuRef, inItemRef){
		// If menu selected show our logbook;
		if (inItemRef == 1){
			if (m_MenuLogbookShow == 0){
				m_CreateLogbookWidget(int(m_ivyConfig.log_window_pos_x), int(m_ivyConfig.log_window_pos_y), int(m_ivyConfig.log_window_width), int(m_ivyConfig.log_window_height));
				m_MenuLogbookShow = 1;
			else{
				m_MenuLogbookShow = 0;
				XPDestroyWidget(self, m_LogbookWidget, 1);
		else if (inItemRef == 2){
			if (m_MenuLogbookShow == 0){
				m_CreateVSpeedsWidget();
				m_MenuVSpeedsShow = 1;
			else{
				m_MenuVSpeedsShow = 0;
				XPDestroyWidget(self, m_VSpeedsWidget, 1);
		else if (inItemRef == 3){
			m_AnnouncementCallback(0,0,0);
		else if (inItemRef == 4){
			m_SayBaroCallback(0,0,0);
		else if (inItemRef == 5){
			m_SayWindCallback(0,0,0);
		else if (inItemRef == 6){
			m_ToogleWindowCallback(0,0,0);
		else if (inItemRef == 7){
			m_ResetIvyCallback(0,0,0);
		pass;
 
	def SayBaroCallback( self , cmd , phase , refcon ) {
		if ( phase == 0 ) {
			m_SayBaro();
		return 0;
 
	def SayWindCallback( self , cmd , phase , refcon ) {
		if ( phase == 0 ) {
			m_SayWind();
		return 0;
 
	def AnnouncementCallback( self , cmd , phase , refcon ) {
		if ( phase == 0 ) {
			if (m_li_on_ground == 1){
				m_ivyAnnounceTakeOff.Activate(m_time);
			else{
				m_ivyAnnounceLanding.Activate(m_time);
		return 0;
 
	def ResetIvyCallback( self , cmd , phase , refcon ) {
		if ( phase == 0 ) {
			m_ResetIvy();
		return 0;
 
	def ToogleWindowCallback( self , cmd , phase , refcon ) {
		if ( phase == 0 ) {
			m_draw_window = 1 - m_draw_window;
		return 0;
 
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
	// SayBaro;
	//;
	// Ivy tells you the current barometric pressure;
 
	def SayBaro(self){
 
		m_play_mp3_queue.append(m_ivyConfig.mp3_path + "baro_press_1.wav");
		m_SpellOutDigits(m_li_baro_sea_level);
		pass;
 
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
	// SayWind;
	//;
	// Ivy tells you the current wind direction && speed;
 
	def SayWind(self){
		m_play_mp3_queue.append(m_ivyConfig.mp3_path + "wind1.wav");
		m_SpellOutNumber(int(m_lf_wind_direction));
		m_play_mp3_queue.append(m_ivyConfig.mp3_path + "wind2.wav");
		m_SpellOutNumber(int(m_lf_wind_speed_kt));
		m_play_mp3_queue.append(m_ivyConfig.mp3_path + "knots.wav");
 
 
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
	// SpellOutDigits;
	//;
	// Ivy spells the single digits of the number given;
 
	def SpellOutDigits(self, spell_number){
		// 1000;
		digit = int((spell_number % 10000) / 1000 );
		m_OutputFile.write(str(digit));
		m_play_mp3_queue.append(m_ivyConfig.number_path + str(digit) + ".wav");
 
		// 100;
		digit = int((spell_number % 1000) / 100 );
		m_OutputFile.write(str(digit));
		m_play_mp3_queue.append(m_ivyConfig.number_path + str(digit) + ".wav");
 
		// 10;
		digit = int((spell_number % 100) / 10 );
		m_OutputFile.write(str(digit));
		m_play_mp3_queue.append(m_ivyConfig.number_path + str(digit) + ".wav");
 
		// 1;
		digit = int(spell_number % 10);
		m_OutputFile.write(str(digit));
		m_play_mp3_queue.append(m_ivyConfig.number_path + str(digit) + ".wav");
 
		m_OutputFile.write("Digits \n\r");
		m_OutputFile.flush();
		m_OutputFile.flush();
		pass;
 
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
	// SpellOutNumber;
	//;
	// Ivy says the number given;
 
	def SpellOutNumber(self, spell_number){
		m_OutputFile.write("SpellOutNumber{ ");
		// 1000;
		digit = int((spell_number % 10000) / 1000 );
		m_OutputFile.write(str(digit) + " ");
		if (digit > 0){
			m_play_mp3_queue.append(m_ivyConfig.number_path + str(digit) + ".wav");
			m_play_mp3_queue.append(m_ivyConfig.number_path + "1000" + ".wav");
		// 100;
		digit = int((spell_number % 1000) / 100);
		m_OutputFile.write(str(digit) + " ");
		if (digit > 0){
			m_play_mp3_queue.append(m_ivyConfig.number_path + str(digit) + ".wav");
			m_play_mp3_queue.append(m_ivyConfig.number_path + "100" + ".wav");
 
		// 10;
		digit = int((spell_number % 100) / 10);
		m_OutputFile.write(str(digit) + " ");
		if (digit > 1){
			m_play_mp3_queue.append(m_ivyConfig.number_path + str(digit*10) + ".wav");
			digit = int(spell_number % 10);
		else{
			digit = int(spell_number % 100);
 
		// Single digit || <20;
		m_OutputFile.write(str(digit) + " ");
		if (digit > 0){
			m_play_mp3_queue.append(m_ivyConfig.number_path + str(digit) + ".wav");
		// if total value is zero, say zero;
		else if (int(spell_number) == 0){
			m_play_mp3_queue.append(m_ivyConfig.number_path + "0" + ".wav");
 
 
 
		m_OutputFile.write("Number End \n\r");
		m_OutputFile.flush();
		m_OutputFile.flush();
		pass;
 
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
	// CheckAnnouncement;
	//;
	// Checks toogling of non smoking sign to make announcement;
 
	def CheckAnnouncement(self){
		if (m_non_smoking_old != m_li_nonsmoking){
			if ((m_time - m_non_smoking_event) < m_ivyConfig.non_smoking_annoucetime){
				if (m_li_on_ground == 1){
					m_ivyAnnounceTakeOff.Activate(m_time);
				else{
					m_ivyAnnounceLanding.Activate(m_time);
 
			m_non_smoking_event = m_time;
 
		m_non_smoking_old = m_li_nonsmoking;
		pass;
 
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
	// DetectLanding;
	//;
	// Detect each single touchdown, create a IvyLandingDetection object with the corresponding values && store it in the ivy_landing_list;
 
	def DetectLanding(self){
		// Detect potential depature airport first{
		// Need to store temporarily, because helicopters on bouncing might trigger this;
		if ((m_li_on_ground == 1) && (m_lf_ground_speed < m_ivyConfig.taxi_ground_speed_min)){
			m_airport_departure_ref = XPLMFindNavAid(None, None, m_ld_latitude, m_ld_longitude, None, xplm_Nav_Airport);
			m_airport_name = [];
			XPLMGetNavAidInfo(m_airport_departure_ref, None, None, None, None, None, None, m_airport_name, None, None);
			m_airport_departure_temp = m_airport_name[0];
 
 
 
		if (m_li_on_ground == 0){
			m_landing_detected = 0;
			m_landing_rated = 0;
 
			// Store the potential departure airport within a 10s window after positive climb callout;
			// Pos climb has a 20s cooldown, which means that we only take the new departure after 20s on ground;
			flight_time = m_time - m_ivyPosRateClimb.time_activated;
			if ((flight_time > 0) && (flight_time < 10)){	m_airport_departure = m_airport_departure_temp;
 
 
		else if ((m_li_on_ground_old == 0) && (m_li_on_ground == 1)){
			m_landing_detected = 1;
 
			buf = "Landing detected{ " + str(m_time) + " Sinkrate{ " + str(m_lf_climb_rate) + " G-Force{ " + str(m_lf_g_normal) + "\n\r";
			m_OutputFile.write(buf);
			m_OutputFile.flush();
 
 
			landing_object = IvyLandingDetection(m_time, m_lf_climb_rate, m_lf_g_normal, m_lf_g_side, m_lf_g_forward);
			m_ivy_landing_list.append(landing_object);
 
			m_landing_rated = 0;
			m_landing_sink_rate = 0;
			m_landing_g_normal = 0;
			m_landing_bounces = 0;
 
			// Check all touch downs. Rating is 0 if not in window;
			for obj_number in range(0,len(m_ivy_landing_list)){
				act_rating = m_ivy_landing_list[obj_number].GetCurrentRate(m_time, 10);
 
				if (act_rating > 0 ) {
					m_landing_sink_rate = max(m_landing_sink_rate, abs(m_ivy_landing_list[obj_number].sink_rate));
					m_landing_g_normal = max(m_landing_g_normal, abs(m_ivy_landing_list[obj_number].g_normal));
					m_landing_bounces = m_landing_bounces + 1;
 
 
 
				if (act_rating > m_landing_rated) { m_landing_rated = act_rating;
				buf = "Landing T=" + str(m_ivy_landing_list[obj_number].time) + " Sink Rate " + str(abs(m_ivy_landing_list[obj_number].sink_rate)) + " g{ " + str(abs(m_ivy_landing_list[obj_number].g_normal)) + " Grade{ " + str(act_rating) + " | ";
				m_OutputFile.write(buf);
			m_OutputFile.write("\n\r");
			m_OutputFile.flush();
 
		m_li_on_ground_old = m_li_on_ground;
		pass;
 
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
	// EndOfFlightEvaluation;
	//;
	// Here, all the touchdowns (if bouncing, it would have been more than one) are evaluated;
 
	def EndOfFlightEvaluation(self){
		error_rate = 0;
		m_landing_detected = 0;
 
		// Get the proper values to speak (before && after decimal point for g forces);
		sink_rate = int(m_landing_sink_rate);
		g_force_int = int(m_landing_g_normal);
		g_force_dec_2 = int(((m_landing_g_normal - g_force_int) * 100));
 
		// Count all the errors that occurred;
		for obj_number in range(0,len(m_ivy_object_list)){
			if (m_ivy_object_list[obj_number].is_error != 0){
				error_rate = error_rate + m_ivy_object_list[obj_number].error_count;
 
		// Evaluate Flight;
		if (error_rate == 0){
			m_play_mp3_queue.append(m_ivyConfig.mp3_path + "error_zero" + ".wav");
		else if (error_rate < 5){
			m_play_mp3_queue.append(m_ivyConfig.mp3_path + "error_good" + ".wav");
		else if (error_rate < 10){
			m_play_mp3_queue.append(m_ivyConfig.mp3_path + "error_bad" + ".wav");
		else{
			m_play_mp3_queue.append(m_ivyConfig.mp3_path + "error_xbad" + ".wav");
 
 
		if (error_rate > 0){ m_SpellOutNumber(error_rate);
 
		// Singular - Plural;
		if (error_rate == 1){
			m_play_mp3_queue.append(m_ivyConfig.mp3_path + "error_a" + ".wav");
		else if (error_rate > 1){
			m_play_mp3_queue.append(m_ivyConfig.mp3_path + "error_b" + ".wav");
 
		// Tell landing sinkrate && g forces;
		m_play_mp3_queue.append(m_ivyConfig.mp3_path + "landing_rate" + ".wav");
		m_SpellOutNumber(sink_rate);
		m_play_mp3_queue.append(m_ivyConfig.mp3_path + "landing_feet" + ".wav");
 
		m_play_mp3_queue.append(m_ivyConfig.mp3_path + "landing_g" + ".wav");
		m_SpellOutNumber(g_force_int);
		m_play_mp3_queue.append(m_ivyConfig.mp3_path + "dot" + ".wav");
		m_SpellOutNumber(g_force_dec_2);
 
		// Tell bounces;
		if (m_landing_bounces <= 1){
			m_play_mp3_queue.append(m_ivyConfig.mp3_path + "no_bounce" + ".wav");
		else{
 
			m_play_mp3_queue.append(m_ivyConfig.mp3_path + "bounce1" + ".wav");
			m_SpellOutNumber(m_landing_bounces-1);
			if (m_landing_bounces == 2){
				m_play_mp3_queue.append(m_ivyConfig.mp3_path + "bounce2s" + ".wav") // singular;
			else{
				m_play_mp3_queue.append(m_ivyConfig.mp3_path + "bounce2" + ".wav");
 
		flight_time 		= int(m_time - m_ivyPosRateClimb.time_activated);
		flight_hours 		= str(int(flight_time/3600));
		flight_minutes 		= str(int((flight_time % 3600)/60));
		flight_seconds  	= str(flight_time % 60);
 
		if (len(flight_hours) <= 1){ 	flight_hours 	= "0" + flight_hours;
		if (len(flight_minutes) <= 1){ 	flight_minutes 	= "0" + flight_minutes;
		if (len(flight_seconds) <= 1){ 	flight_seconds 	= "0" + flight_seconds;
 
		// Logbook;
 
		lba_acf_descrip= [];
		XPLMGetDatab(m_s_acf_descrip,lba_acf_descrip,0,240);
		aircraft_name = str(lba_acf_descrip);
 
		airport_arrival_ref = XPLMFindNavAid(None, None, m_ld_latitude, m_ld_longitude, None, xplm_Nav_Airport);
		airport_name = [];
		XPLMGetNavAidInfo(airport_arrival_ref, None, None, None, None, None, None, airport_name, None, None);
		m_airport_arrival = airport_name[0];
		acf_len = int(m_ivyConfig.log_afc_name_length);
		aircraft_short = aircraft_name + (" " * acf_len);
		aircraft_short = aircraft_short[{acf_len];
 
		now = datetime.datetime.now();
		year = str(now.year);
 
		if (m_landing_rated == 1){	grade="A";
		else if (m_landing_rated == 2){	grade="B";
		else if (m_landing_rated == 3){	grade="C";
		else if (m_landing_rated == 4){	grade="D";
		else{							grade="F";
 
		if (m_landing_bounces >= 1){   m_landing_bounces = m_landing_bounces - 1;
 
		// Format strings caused random errors, using manual alignment instead;
		sink_rate_str 		= (max(5-len(str(sink_rate)),0) * " ") 				+ str(sink_rate);
		g_force_int_str 	= (max(2-len(str(g_force_int)),0) * " ") 			+ str(g_force_int);
		g_force_dec_2_str 	= str(g_force_dec_2) 								+ (max(2-len(str(g_force_dec_2)),0) * " ") // decimal part needs spaces afterwards;
		bounces_str 		= (max(3-len(str(m_landing_bounces)),0) * " ")	+ str(m_landing_bounces);
		error_rate_str		= (max(3-len(str(error_rate)),0) * " ") 			+ str(error_rate);
 
		dep_str 			= (max(6-len(str(m_airport_departure)),0) * " ") + str(m_airport_departure);
		app_str				= (max(6-len(str(m_airport_arrival)),0) * " ") 	+ str(m_airport_arrival);
		month				= (max(2-len(str(now.month)),0) * " ") 				+ str(now.month);
		day					= (max(2-len(str(now.day)),0) * " ") 				+ str(now.day);
 
		logbook_entry   = "";
		logbook_entry 	= logbook_entry + year + "/" + month + "/" + day + " ";
		logbook_entry 	= logbook_entry + "Aircraft{ " + aircraft_short + ", ";
		logbook_entry   = logbook_entry + "Dep{ " + dep_str + ", ";
		logbook_entry   = logbook_entry + "Arr{ " + app_str + ", ";
		logbook_entry   = logbook_entry + "Flight Time{ " + flight_hours + "{" + flight_minutes + "{" + flight_seconds + ", ";
		logbook_entry   = logbook_entry + "Errors{ " + error_rate_str + ", ";
 
		logbook_entry   = logbook_entry + "Landing{ " + grade + ", " + sink_rate_str+ " ft/min, " + g_force_int_str + "." + g_force_dec_2_str + "g, " + bounces_str + " bounce(s)\n\r";
 
		// Do not write in replay mode;
		if (m_li_replay == 0){
			logbook_file 	= open(m_ivyConfig.logbook_path, 'a+');
			logbook_file.write(logbook_entry);
			logbook_file.close();
 
			// Reset error counters;
			for obj_number in range(0,len(m_ivy_object_list)){
				m_ivy_object_list[obj_number].error_count = 0;
 
		pass;
 
 
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
	// FlightLoopCallback;
	//;
	// This is where all the error detection is performed;
 
	def FlightLoopCallback(self, elapsedMe, elapsedSim, counter, refcon){
 
		m_time = m_time + m_ivyConfig.data_rate;
 
		m_passengersScreaming = false;
		m_passengerVolume = 0.3;
 
		// We reset the aircraft loaded situation after 60 seconds;
		if (m_time > (60 + m_ivyConfig.disable_after_loading)){
			m_aircraft_loaded = 0;
 
		// Get all the fresh data from the datarefs;
		if (m_plugin_enabled == 1){
			m_ReadData();
 
		// If started to play queue file, we deactivate for X cycles;
		// Currently deactivated, as it seems we do not need this;
		//if (m_deact_queue > 0){
		//	m_deact_queue = m_deact_queue - 1;
 
		// Playlist. Here we can queue text that is longer than a single mp3;
		// If we still have to say something, error detection is disabled. We would not have time to say it anyways.;
		if (m_plugin_enabled == 0){
			pass;
		else if (len(m_play_mp3_queue) > 0){
			if (m_ivyChannel.get_busy() == false){
				actsound = pygame.mixer.Sound(m_play_mp3_queue[0]);
				m_ivyChannel.play(actsound);
				del m_play_mp3_queue[0];
				m_deact_queue = m_ivyConfig.deact_after_queue;
 
		////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
		// NOT after Load && NOT after Crash;
 
		else if ((m_time > m_ivyConfig.disable_after_loading) && (m_aircraft_crashed == 0) && (m_li_replay == 0)){
 
			if (m_lf_g_normal > m_f_g_normal_max){ m_f_g_normal_max = m_lf_g_normal;
			if (m_lf_g_side > m_f_g_side_max){ m_f_g_side_max = m_lf_g_side;
			if (m_lf_g_forward > m_f_g_forward_max){ m_f_g_forward_max = m_lf_g_forward;
 
			if (m_lf_g_normal < m_f_g_normal_min){ m_f_g_normal_min = m_lf_g_normal;
			if (m_lf_g_side < m_f_g_side_min){ m_f_g_side_min = m_lf_g_side;
			if (m_lf_g_forward < m_f_g_forward_min){ m_f_g_forward_min = m_lf_g_forward;
 
 
 
			m_f_g_normal_delta = (m_lf_g_normal - m_f_g_normal_old) / m_ivyConfig.data_rate;
			m_f_g_side_delta = (m_lf_g_side - m_f_g_side_old) / m_ivyConfig.data_rate;
			m_f_g_front_delta = (m_lf_g_forward - m_f_g_forward_old) / m_ivyConfig.data_rate;
 
			m_f_g_normal_old = m_lf_g_normal;
			m_f_g_side_old = m_lf_g_side;
			m_f_g_forward_old = m_lf_g_forward;
 
			if (m_cab_press_old != 0){ 	m_cab_press_rate = 60 * (m_lf_cab_press - m_cab_press_old) / (m_li_sim_ground_speed * m_ivyConfig.data_rate);
			m_cab_press_old = m_lf_cab_press;
 
 
 
			m_DetectLanding();
 
 
			// Ouch when bumping on ground;
			if ((m_li_on_ground == 1) && ((m_lf_g_normal) > m_ivyConfig.ivy_ouch_g)){ //play ouch;
				actsound = pygame.mixer.Sound(m_ivyConfig.mp3_path + "ouch_1.wav");
				m_ivyChannel.play(actsound);
 
			// Check for announcemnt to make;
			m_CheckAnnouncement();
 
 
 
			// Announcement deactivation only. Either activated by command || by CheckAnnouncement;
			if (m_li_on_ground == 1){																												m_ivyAnnounceLanding.Deactivate(m_time);
			if (m_li_on_ground == 0){																												m_ivyAnnounceTakeOff.Deactivate(m_time);
 
			if ((m_li_on_ground == 0) && (m_lf_climb_rate > m_ivyConfig.pos_rate_climb)){														m_ivyPosRateClimb.Activate(m_time);
			else if (m_li_on_ground == 1){																												m_ivyPosRateClimb.Deactivate(m_time);
 
			// Decision Height Arm;
			if ((m_li_on_ground == 0) && (m_lf_radio_alt > (m_lf_decision_height + m_ivyConfig.decition_height_arm))){						m_ivyArmMinimums.Activate(m_time);
			else if (m_li_on_ground == 1){																												m_ivyArmMinimums.Deactivate(m_time);
 
			if ((m_li_on_ground == 0) &&
			   (m_ivyArmMinimums.played == 1) &&
			   (m_lf_decision_height > 0) &&
			   (m_lf_radio_alt < (m_lf_decision_height + m_ivyConfig.decition_height_plus))){													m_ivyMinimums.Activate(m_time);
			else if (m_lf_radio_alt > (m_lf_decision_height + m_ivyConfig.decition_height_arm)){													m_ivyMinimums.Deactivate(m_time);
 
 
			// Fasten Seatbelts;
			if (m_li_fastenseatbelts > 0){
																																						m_ivySeatBelts.Activate(m_time);
			else{																																		m_ivySeatBelts.Deactivate(m_time);
 
			// Gear down callout;
			//if (m_lf_gear1_ratio > 0.999){																											m_ivyGearDown.Activate(m_time);
			//else{																																		m_ivyGearDown.Deactivate(m_time);
 
			if ((m_lf_gear1_ratio == 1) &&
			   (m_lf_gear2_ratio in range(0,2)) &&
			   (m_lf_gear3_ratio in range(0,2)) &&
			   (m_lf_gear4_ratio in range(0,2)) &&
			   (m_lf_gear5_ratio in range(0,2))){																									m_ivyGearDown.Activate(m_time);
			else{																																		m_ivyGearDown.Deactivate(m_time);
 
			// Gear up callout;
			//if (m_lf_gear1_ratio < 0.001){																											m_ivyGearUp.Activate(m_time);
			//else{																																		m_ivyGearUp.Deactivate(m_time);
 
			if ((m_lf_gear1_ratio == 0) &&
			   (m_lf_gear2_ratio in range(0,2)) &&
			   (m_lf_gear3_ratio in range(0,2)) &&
			   (m_lf_gear4_ratio in range(0,2)) &&
			   (m_lf_gear5_ratio in range(0,2))){																									m_ivyGearUp.Activate(m_time);
			else{																																		m_ivyGearUp.Deactivate(m_time);
 
			// Tire blown;
			if ((m_li_tire1 + m_li_tire2 + m_li_tire3 + m_li_tire4 + m_li_tire5) > 0){													m_ivyTyre.Activate(m_time);
			else{																																		m_ivyTyre.Deactivate(m_time);
 
			// Hard braking;
			if ((m_li_on_ground == 1) && (m_lf_g_forward > m_ivyConfig.brake_max_forward_g)){ 												m_ivyBrake.Activate(m_time);
			else{																																		m_ivyBrake.Deactivate(m_time);
 
			// Transponder not active when airborne;
			if ((m_li_on_ground == 0) && (m_li_transponder_mode < 2)){																			m_ivyTransponder.Activate(m_time) // Dataref{ Mode2=ON, B407 4=ON;
			else if (m_li_on_ground == 1){																												m_ivyTransponder.Deactivate(m_time);
 
			// Landing lights not on when landing in the night;
			if ((m_li_on_ground == 0) && (m_lf_radio_alt < m_ivyConfig.alt_landing_lights_low) &&
			    (m_lf_world_light_precent > m_ivyConfig.night_world_light_precent) && (m_li_landing_lights == 0)){							m_ivyLandingLights.Activate(m_time);
			else{																																		m_ivyLandingLights.Deactivate(m_time);
 
			// Landing lights not off on high altitude;
			if ((m_li_on_ground == 0) && (m_lf_radio_alt > 3000) && (m_lf_baro_alt > m_ivyConfig.alt_landing_lights_high) &&
			   (m_li_landing_lights == 1)){																											m_ivyLandingLightsHigh.Activate(m_time);
			else{																																		m_ivyLandingLightsHigh.Deactivate(m_time);
 
			// Beacon lights not when taxiing;
			if ((m_li_on_ground == 1) && (m_lf_ground_speed > m_ivyConfig.taxi_ground_speed_min) && (m_li_beacon_lights == 0)){			m_ivyBeaconLights.Activate(m_time);
			else if (m_li_beacon_lights != 0){																											m_ivyBeaconLights.Deactivate(m_time);
 
			// Nav lights lights not when airborne;
			if ((m_li_on_ground == 0) && (m_li_nav_lights == 0)){																				m_ivyNavLights.Activate(m_time);
			else{																																		m_ivyNavLights.Deactivate(m_time);
 
			// Strobes not on when airborne;
			if ((m_li_on_ground == 0) && (m_li_strobe_lights == 0)){																				m_ivyStrobes.Activate(m_time);
			else{																																		m_ivyStrobes.Deactivate(m_time);
 
			// Comment on X-Plane tire blown message when aircraft has skid;
			if (((m_li_tire1 + m_li_tire2 + m_li_tire3 + m_li_tire4 + m_li_tire5) > 0) && (m_li_has_skid == 1)){						m_ivySkidTyres.Activate(m_time);
			else{																																		m_ivySkidTyres.Deactivate(m_time);
 
			// Battery low;
			if ((m_li_batt1 + m_li_batt2) > 0){																									m_ivyBatteryOut.Activate(m_time);
			else{																																		m_ivyBatteryOut.Deactivate(m_time);
 
			// Engine fire;
			if ((m_li_fire1 + m_li_fire2 + m_li_fire3 + m_li_fire4 + m_li_fire5 + m_li_fire6 + m_li_fire7 + m_li_fire8) > 0){	m_ivyEngineFire.Activate(m_time);
			else{																																		m_ivyEngineFire.Deactivate(m_time);
 
			// Engine flameout;
			if ((m_li_flameout1 + m_li_flameout2 + m_li_flameout3 + m_li_flameout4 +;
				 m_li_flameout5 + m_li_flameout6 + m_li_flameout7 + m_li_flameout8) > 0){													m_ivyEngineFlameout.Activate(m_time);
			else{																																		m_ivyEngineFlameout.Deactivate(m_time);
 
			// Engine ground failure;
			if ((m_li_on_ground == 1) &&
			   ((m_li_engine_failure1 + m_li_engine_failure2 + m_li_engine_failure3 + m_li_engine_failure4 +;
				 m_li_engine_failure5 + m_li_engine_failure6 + m_li_engine_failure7 + m_li_engine_failure8) > 0)){							m_ivyEngineFailureGround.Activate(m_time);
			else{																																		m_ivyEngineFailureGround.Deactivate(m_time);
 
			// Engine airborne failure;
			if ((m_li_on_ground == 0) &&
			   ((m_li_engine_failure1 + m_li_engine_failure2 + m_li_engine_failure3 + m_li_engine_failure4 +;
				 m_li_engine_failure5 + m_li_engine_failure6 + m_li_engine_failure7 + m_li_engine_failure8) > 0)){							m_ivyEngineFailureAir.Activate(m_time);
			else{																																		m_ivyEngineFailureAir.Deactivate(m_time);
 
			// Engine hot start;
			if ((m_li_hot1 + m_li_hot2 + m_li_hot3 + m_li_hot4 + m_li_hot5 + m_li_hot6 + m_li_hot7 + m_li_hot8) > 0){			m_ivyEngineHotStart.Activate(m_time);
			else{																																		m_ivyEngineHotStart.Deactivate(m_time);
 
			// Battery not on;
			if ((m_li_battery_on == 0) && (m_li_gpu_on == 0)){																					m_ivyNoBatt.Activate(m_time);
			else{																																		m_ivyNoBatt.Deactivate(m_time);
 
			// Flaps Overspeed;
			if (m_li_flaps_overspeed > 0){																											m_ivyOverspeedFlaps.Activate(m_time);
			else{																																		m_ivyOverspeedFlaps.Deactivate(m_time);
 
			// Gear Overspeed;
			if (m_li_gear_overspeed > 0){																											m_ivyOverspeedGear.Activate(m_time);
			else{																																		m_ivyOverspeedGear.Deactivate(m_time);
 
			// Stall;
			if (m_li_on_ground == 0) && (m_li_stall > 0){																						m_ivyStall.Activate(m_time);
			else{																																		m_ivyStall.Deactivate(m_time);
 
			// Aircraft Overspeed;
			if (m_lf_ias > m_lf_aircraft_vne) && (m_lf_aircraft_vne > 1){																		m_ivyOverspeedAircraft.Activate(m_time);
			else{																																		m_ivyOverspeedAircraft.Deactivate(m_time);
 
			// Hello - Depending on weather;
			if ((m_aircraft_loaded == 1) &&
				(m_li_cloud_0 < 1) && (m_li_cloud_1 < 1) && (m_li_cloud_2 < 1) &&
				(m_lf_visibility > m_ivyConfig.vis_is_fog) && (m_li_rain == 0) && (m_li_thunder == 0)){									m_ivyHelloSun.Activate(m_time);
			else{																																		m_ivyHelloSun.Deactivate(m_time);
 
			if ((m_aircraft_loaded == 1) &&
				(m_lf_visibility > m_ivyConfig.vis_is_fog) && (m_li_rain > 0) && (m_li_thunder == 0)){									m_ivyHellorain.Activate(m_time);
			else{																																		m_ivyHellorain.Deactivate(m_time);
 
			//ToDo{
			//if ((m_aircraft_loaded == 1) &&
			//	(m_lf_visibility > m_ivyConfig.vis_is_fog) && (m_li_thunder > 0)){															m_ivyHelloThunder.Activate(m_time);
			//else{																																		m_ivyHelloThunder.Deactivate(m_time);
 
			if ((m_aircraft_loaded == 1) &&
				(m_lf_visibility <= m_ivyConfig.vis_is_fog)){																						m_ivyHelloFog.Activate(m_time);
			else{																																		m_ivyHelloFog.Deactivate(m_time);
 
			if ((m_aircraft_loaded == 1) &&
				((m_li_cloud_0 >= 1) || (m_li_cloud_1 >= 1) || (m_li_cloud_2 >= 1)) &&
				(m_lf_visibility > m_ivyConfig.vis_is_fog) && (m_li_rain == 0) && (m_li_thunder == 0)){									m_ivyHelloNormal.Activate(m_time);
			else{																																		m_ivyHelloNormal.Deactivate(m_time);
 
			// Cabin pressure falling too fast;
			// Some aircraft do not get it right, when you increase the ground speed. Hence, I use both, my own && the Aircraft computation;
			if ((m_li_on_ground == 0) && (max(m_lf_cab_rate, m_lf_climb_rate) < m_ivyConfig.cab_rate_low)){								m_ivyCabinDownNormal.Activate(m_time);
			else if (max(m_lf_cab_rate, m_lf_climb_rate) > (m_ivyConfig.cab_rate_low + m_ivyConfig.cab_rate_reset_hysteresis)){				m_ivyCabinDownNormal.Deactivate(m_time);
 
			// Cabin pressure falling rapidely;
			if ((m_li_on_ground == 0) && (max(m_lf_cab_rate, m_lf_climb_rate) < m_ivyConfig.cab_rate_high)){
																																						m_ivyCabinDownFast.Activate(m_time);
																																						m_ivyCabinDownNormal.SetAsPlayed(m_time);
			else if (max(m_lf_cab_rate, m_lf_climb_rate) > (m_ivyConfig.cab_rate_high + m_ivyConfig.cab_rate_reset_hysteresis)){				m_ivyCabinDownFast.Deactivate(m_time);
 
			// Bank angle pre-warning;
			if ((m_li_on_ground == 0) && (abs(m_lf_roll) > m_ivyConfig.bank_low)){															m_ivyBankNormal.Activate(m_time);
			else if (abs(m_lf_roll) < m_ivyConfig.bank_reset_low){																					m_ivyBankNormal.Deactivate(m_time);
 
			// Bank angle too high;
			if ((m_li_on_ground == 0) && (abs(m_lf_roll) > m_ivyConfig.bank_high)){
																																						m_ivyBankHigh.Activate(m_time);
																																						m_ivyBankNormal.SetAsPlayed(m_time);
			else if (abs(m_lf_roll) < m_ivyConfig.bank_low){																							m_ivyBankHigh.Deactivate(m_time);
 
			// Bank angle extremely high;
			if ((m_li_on_ground == 0) && (abs(m_lf_roll) > m_ivyConfig.bank_xhigh)){
																																						m_passengersScreaming = true;
																																						m_ivyBankXHigh.Activate(m_time);
																																						m_ivyBankHigh.SetAsPlayed(m_time);
																																						m_ivyBankNormal.SetAsPlayed(m_time);
			else if (abs(m_lf_roll) < m_ivyConfig.bank_high){																						m_ivyBankXHigh.Deactivate(m_time);
 
 
			// Pitch down pre-warning;
			if ((m_li_on_ground == 0) && (m_lf_pitch < m_ivyConfig.pitch_low)){																m_ivyPitchDownNormal.Activate(m_time);
			else if (m_lf_pitch > m_ivyConfig.pitch_reset_low){																						m_ivyPitchDownNormal.Deactivate(m_time);
 
			// Pitch too low;
			if ((m_li_on_ground == 0) && (m_lf_pitch <= m_ivyConfig.pitch_high)){
																																						m_passengersScreaming = true;
																																						m_ivyPitchDownHigh.Activate(m_time);
																																						m_ivyPitchDownNormal.SetAsPlayed(m_time);
			else if (m_lf_pitch > m_ivyConfig.pitch_low){																							m_ivyPitchDownHigh.Deactivate(m_time);
 
 
			// Normal G Force high;
			if ((m_li_on_ground == 0) && (m_lf_g_normal >= m_ivyConfig.max_g_down_low)){
																																						m_passengersScreaming = true;
																																						m_passengerVolume = max (m_passengerVolume, abs(m_lf_g_normal) / 6);
																																						m_ivyGNormalFlightNormal.Activate(m_time);
			else if (m_lf_g_normal <= m_ivyConfig.max_g_down_low_reset){																				m_ivyGNormalFlightNormal.Deactivate(m_time);
 
			// Normal G Force very high;
			if ((m_li_on_ground == 0) && (m_lf_g_normal >= m_ivyConfig.max_g_down_high)){
																																						m_ivyGNormalFlightHigh.Activate(m_time);
																																						m_ivyGNormalFlightNormal.SetAsPlayed(m_time);
			else if (m_lf_g_normal <= m_ivyConfig.max_g_down_low_reset){																				m_ivyGNormalFlightHigh.Deactivate(m_time);
 
			// Normal G Force very, very high;
			if ((m_li_on_ground == 0) && (m_lf_g_normal >= m_ivyConfig.max_g_down_xhigh)){
																																						m_ivyGNormalFlightXHigh.Activate(m_time);
																																						m_ivyGNormalFlightHigh.SetAsPlayed(m_time);
																																						m_ivyGNormalFlightNormal.SetAsPlayed(m_time);
			else if (m_lf_g_normal <= m_ivyConfig.max_g_down_low_reset){																				m_ivyGNormalFlightXHigh.Deactivate(m_time);
 
 
			// Normal G Force too low;
			if ((m_li_on_ground == 0) && (m_lf_g_normal <= 0.5)){
																																						m_passengersScreaming = true;
																																						m_passengerVolume = max (m_passengerVolume, abs(m_lf_g_normal - 0.5) / 2);
																																						m_ivyGNormalNegativeLow.Activate(m_time);
			else if (m_lf_g_normal > 0.8){																												m_ivyGNormalNegativeLow.Deactivate(m_time);
 
			// Normal G Force negative;
			if ((m_li_on_ground == 0) && (m_lf_g_normal <= 0)){
																																						m_ivyGNormalNegativeHigh.Activate(m_time);
																																						m_ivyGNormalNegativeLow.SetAsPlayed(m_time);
			else if (m_lf_g_normal > 0.5){																												m_ivyGNormalNegativeHigh.Deactivate(m_time);
 
			// TBD;
			//m_li_turbulence = XPLMGetDatai(m_i_turbulence);
			//if ((m_li_on_ground == 0) && (m_li_turbulence > 10)){																				m_ivyTurbulenceNormal.Activate(m_time);
			//else if (m_li_turbulence < 2){																												m_ivyTurbulenceNormal.Deactivate(m_time);
 
			//if ((m_li_on_ground == 0) && (m_li_turbulence > 30)){																				m_ivyTurbolenceHigh.Activate(m_time);
			//else if (m_li_turbulence < 5){																												m_ivyTurbolenceHigh.Deactivate(m_time);
 
			// Barometric pressure not set accordingly while close to ground || taxiing (within tolerance);
			if ((m_lf_radio_alt < m_ivyConfig.baro_alt_low) &&
			    (abs(m_li_baro_set - m_li_baro_sea_level) > m_ivyConfig.baro_tolerance) &&
				(m_lf_ground_speed > m_ivyConfig.taxi_ground_speed_min)){
																																						m_ivyBaroGround.Activate(m_time);
																																						if ((m_ivyBaroGround.played == 1) && (m_pressure_said == 0)){
																																							m_pressure_said = 1;
																																							m_SayBaro();
			else if ((abs(m_li_baro_set - m_li_baro_sea_level) <= m_ivyConfig.baro_tolerance) || (m_lf_baro_alt > m_ivyConfig.trans_alt)) {
																																						m_ivyBaroGround.Deactivate(m_time);
																																						m_pressure_said = 0;
 
			// Barometric pressure not set to standard above transition altitude;
			if ((m_lf_baro_alt > (m_ivyConfig.trans_alt + m_ivyConfig.trans_hysteresis)) &&
			    (abs(2992 - m_li_baro_set) > m_ivyConfig.baro_tolerance)){																		m_ivyBaroHigh.Activate(m_time);
			else{																																		m_ivyBaroHigh.Deactivate(m_time);
 
			// 60 knots callout;
			if ((m_li_on_ground == 1) && (m_ivyConfig.kt60_enabled == true) && (m_lf_ias > 58) && (m_lf_ias < 70)){						m_ivy60kt.Activate(m_time);
			else{																																		m_ivy60kt.Deactivate(m_time);
 
			// 80 knots callout;
			if ((m_li_on_ground == 1) && (m_ivyConfig.kt80_enabled == true) && (m_lf_ias > 78) && (m_lf_ias < 90)){						m_ivy80kt.Activate(m_time);
			else{																																		m_ivy80kt.Deactivate(m_time);
 
			// 100 knots callout;
			if ((m_li_on_ground == 1) && (m_ivyConfig.kt100_enabled == true) && (m_lf_ias > 98) && (m_lf_ias < 110)){					m_ivy100kt.Activate(m_time);
			else{																																		m_ivy100kt.Deactivate(m_time);
 
			// Not rotated;
			if ((m_li_on_ground == 1) && (m_lf_ias > 180) && (m_landing_detected == 0)){														m_ivyRotate.Activate(m_time);
			else{																																		m_ivyRotate.Deactivate(m_time);
 
			// Ice airframe low;
			if (m_lf_ice_frame > m_ivyConfig.ice_low){																							m_ivyIceAirframeLow.Activate(m_time);
			else{																																		m_ivyIceAirframeLow.Deactivate(m_time);
 
			// Ice airframe high;
			if (m_lf_ice_frame > m_ivyConfig.ice_high){
																																						m_ivyIceAirframeHigh.Activate(m_time);
																																						m_ivyIceAirframeLow.SetAsPlayed(m_time);
			else{																																		m_ivyIceAirframeHigh.Deactivate(m_time);
 
			// Ice pitot low;
			if (m_lf_ice_pitot > m_ivyConfig.ice_low){																							m_ivyIcePitotLow.Activate(m_time);
			else{																																		m_ivyIcePitotLow.Deactivate(m_time);
 
			// Ice pitot high;
			if (m_lf_ice_pitot > m_ivyConfig.ice_high){
																																						m_ivyIcePitotHigh.Activate(m_time);
																																						m_ivyIcePitotLow.SetAsPlayed(m_time);
			else{																																		m_ivyIcePitotHigh.Deactivate(m_time);
 
			// Ice propeller low;
			if (m_lf_ice_propeller > m_ivyConfig.ice_low){																						m_ivyIcePropellerLow.Activate(m_time);
			else{																																		m_ivyIcePropellerLow.Deactivate(m_time);
 
			// Ice propeller high;
			if (m_lf_ice_propeller > m_ivyConfig.ice_high){
																																						m_ivyIcePropellerHigh.Activate(m_time);
																																						m_ivyIcePropellerLow.SetAsPlayed(m_time);
			else{																																		m_ivyIcePropellerHigh.Deactivate(m_time);
 
			// Ice cockpit window low;
			if (m_lf_ice_window > m_ivyConfig.ice_low){																							m_ivyIceWindowLow.Activate(m_time);
			else{																																		m_ivyIceWindowLow.Deactivate(m_time);
 
			// Ice cockpit window high;
			if (m_lf_ice_window > m_ivyConfig.ice_high){
																																						m_ivyIceWindowHigh.Activate(m_time);
																																						m_ivyIceWindowLow.SetAsPlayed(m_time);
			else{																																		m_ivyIceWindowHigh.Deactivate(m_time);
 
			// Cabin pressure low;
			if (m_lf_cab_press > m_ivyConfig.cab_press_low){																						m_ivyPressureLow.Activate(m_time);
			else{																																		m_ivyPressureLow.Deactivate(m_time);
 
			// Cabin pressure too low to breath;
			if (m_lf_cab_press > m_ivyConfig.cab_press_high){
																																						m_ivyPressureXLow.Activate(m_time);
																																						m_ivyPressureLow.SetAsPlayed(m_time);
			else{																																		m_ivyPressureXLow.Deactivate(m_time);
 
			// Birdstrike;
			if (m_li_bird != 0){																														m_ivyBirdStrike.Activate(m_time);
			else{																																		m_ivyBirdStrike.Deactivate(m_time);
 
			////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
			// V-Speed callouts if configured in IvyAircraft ini file;
			// V1;
			// VR;
			// V2;
			// V2 not achieved within 5 seconds after take off;
 
			if ((m_li_on_ground == 1) && (m_ivyAircraft.li_v1 > 0) &&
			    (m_lf_ias >= m_ivyAircraft.li_v1) && (m_lf_ground_speed > m_ivyConfig.taxi_ground_speed_min)){								m_ivyV1.Activate(m_time);
			else if ((m_li_on_ground == 1) && (m_lf_ias < 10)){																						m_ivyV1.Deactivate(m_time);
 
			if ((m_li_on_ground == 1) && (m_ivyAircraft.li_vr > 0) &&
			    (m_lf_ias >= m_ivyAircraft.li_vr) && (m_lf_ground_speed > m_ivyConfig.taxi_ground_speed_min)){								m_ivyVR.Activate(m_time);
			else if ((m_li_on_ground == 1) && (m_lf_ias < 10)){																						m_ivyVR.Deactivate(m_time);
 
			if ((m_li_on_ground == 0) && (m_ivyAircraft.li_v2 > 0) &&
			    (m_lf_ias >= m_ivyAircraft.li_v2)){																								m_ivyAboveV2.Activate(m_time);
			else if (m_li_on_ground == 1){																												m_ivyAboveV2.Deactivate(m_time);
 
			if ((m_li_on_ground == 0) && (m_ivyAircraft.li_v2 > 0) &&
			    (m_lf_ias < m_ivyAircraft.li_v2) && (m_ivyAboveV2.played == 0)){
																																						m_ivyBelowV2.Activate(m_time);
																																						m_ivyAboveV2.Deactivate(m_time);
			else if (m_li_on_ground == 1){																												m_ivyBelowV2.Deactivate(m_time);
 
 
			////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
			// Slats callout if configured in IvyAircraft ini file;
			if ((m_ivyAircraft.slats_enabled == true) && (m_ivyAircraft.lf_slats == 0)){															m_ivySlatsRetracted.Activate(m_time);
			else{ 																																		m_ivySlatsRetracted.Deactivate(m_time);
 
			if (m_ivyAircraft.slats_enabled == true){
				slats_activated = false;
				for index in range(0,len(m_ivyAircraft.slats_deploy_value)){
					if (abs(m_ivyAircraft.lf_slats - m_ivyAircraft.slats_deploy_value[index]) < m_ivyAircraft.slats_tolerance){
						slats_activated = true;
						if (m_ivySlatsPosition.active == 0) && (m_ivyChannel.get_busy() == false){
																																						m_ivySlatsPosition.Activate(m_time);
																																						m_SpellOutNumber(m_ivyAircraft.slats_deploy_pos[index]);
				if (slats_activated == false){																											m_ivySlatsPosition.Deactivate(m_time);
 
 
			////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
			// Flaps callout if configured in IvyAircraft ini file;
			if ((m_ivyAircraft.flaps_enabled == true) && (m_ivyAircraft.lf_flaps < m_ivyAircraft.flaps_tolerance)){							m_ivyFlapsRetracted.Activate(m_time);
			else{ 																																		m_ivyFlapsRetracted.Deactivate(m_time);
 
			if (m_ivyAircraft.flaps_enabled == true){
				flaps_activated = false;
				for index in range(0,len(m_ivyAircraft.flaps_deploy_value)){
					if (abs(m_ivyAircraft.lf_flaps - m_ivyAircraft.flaps_deploy_value[index]) < m_ivyAircraft.flaps_tolerance){
						flaps_activated = true;
						if (m_ivyFlapsPosition.active == 0) && (m_ivyChannel.get_busy() == false){
																																						m_ivyFlapsPosition.Activate(m_time);
																																						m_SpellOutNumber(m_ivyAircraft.flaps_deploy_pos[index]);
				if (flaps_activated == false){																											m_ivyFlapsPosition.Deactivate(m_time);
 
			////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
			// After landing{
			// Rating of the Landing;
			// End of flight evaluation;
 
			// We want to get airborne before landing evaluation - too many false alarms on load;
			if ((m_li_on_ground == 0) && (m_lf_radio_alt > 100) && (m_lf_climb_rate > 100)){													m_ivyArmLanding.Activate(m_time);
 
			if ((m_landing_detected == 1) && (m_landing_rated > 0) &&
			    (m_ivyArmLanding.played == 1) && (m_ivyConfig.passengers_enabled == true)){														m_ivyApplause.Activate(m_time);
			else if (m_li_on_ground == 0){																												m_ivyApplause.Deactivate(m_time);
 
 
			if ((m_landing_detected == 1) && (m_landing_rated == 1) && (m_lf_ground_speed < m_ivyConfig.taxi_ground_speed_min) && (m_ivyArmLanding.played == 1)){
																																						m_ivyLandingXGood.Activate(m_time);
																																						if (m_ivyLandingXGood.played == 1){
																																							m_EndOfFlightEvaluation();
																																							m_ivyArmLanding.Deactivate(m_time);
			else{																																		m_ivyLandingXGood.Deactivate(m_time);
 
			if ((m_landing_detected == 1) && (m_landing_rated == 2) && (m_lf_ground_speed < m_ivyConfig.taxi_ground_speed_min) && (m_ivyArmLanding.played == 1)){
																																						m_ivyLandingGood.Activate(m_time);
																																						if (m_ivyLandingGood.played == 1){
																																							m_EndOfFlightEvaluation();
																																							m_ivyArmLanding.Deactivate(m_time);
			else{																																		m_ivyLandingGood.Deactivate(m_time);
 
			if ((m_landing_detected == 1) && (m_landing_rated == 3) && (m_lf_ground_speed < m_ivyConfig.taxi_ground_speed_min) && (m_ivyArmLanding.played == 1)){
																																						m_ivyLandingNormal.Activate(m_time);
																																						if (m_ivyLandingNormal.played == 1){
																																							m_EndOfFlightEvaluation();
																																							m_ivyArmLanding.Deactivate(m_time);
			else{																																		m_ivyLandingNormal.Deactivate(m_time);
 
			if ((m_landing_detected == 1) && (m_landing_rated == 4) && (m_lf_ground_speed < m_ivyConfig.taxi_ground_speed_min) && (m_ivyArmLanding.played == 1)){
																																						m_ivyLandingBad.Activate(m_time);
																																						if (m_ivyLandingBad.played == 1){
																																							m_EndOfFlightEvaluation();
																																							m_ivyArmLanding.Deactivate(m_time);
			else{																																		m_ivyLandingBad.Deactivate(m_time);
 
 
			if ((m_landing_detected == 1) && (m_landing_rated == 5) && (m_lf_ground_speed < m_ivyConfig.taxi_ground_speed_min) && (m_ivyArmLanding.played == 1)){
																																						m_ivyLandingXBad.Activate(m_time);
																																						if (m_ivyLandingXBad.played == 1){
																																							m_EndOfFlightEvaluation();
																																							m_ivyArmLanding.Deactivate(m_time);
			else{																																		m_ivyLandingXBad.Deactivate(m_time);
 
		////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
		// After Load || after Crash;
 
		if ((m_aircraft_crashed == 1) && (m_time > m_ivyConfig.disable_after_loading)){														m_ivyCrash.Activate(m_time);
		else{																																			m_ivyCrash.Deactivate(m_time);
 
		// Here comes the screaming;
		m_passengerVolume = max (m_passengerVolume, abs(m_lf_roll) / 120);
		m_passengerVolume = max (m_passengerVolume, abs(m_lf_pitch) / 60);
 
		if (m_ivyConfig.passengers_enabled == true){		m_ivyPassengers.MakeScream(m_passengersScreaming, m_passengerVolume);
 
		//if ((m_lf_world_light_precent > 0.5) && (m_lf_climb_rate > 100)){  pass;
 
		//buf = "Normal{ " + "{{.2f}".format(m_f_g_normal_delta) + "Side{ " + "{{.2f}".format(m_f_g_side_delta) + "Normal{ " + "{{.2f}".format(m_f_g_forward_delta) + "\r\n";
		//m_OutputFile.write(buf);
 
		return m_ivyConfig.data_rate;
 
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
	// ReadData;
	//;
	// This function get's all new values from the DataRefs;
	// Calls IvyAircraft object for update too -> only call when aircraft is loaded;
 
	def ReadData(self){
		//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
		//;
		//						DATAREF to Local Variables;
		//;
		//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
 
 
 
		lba_acf_descrip= [];
		lba_acf_tailnumber = [];
 
		XPLMGetDatab(m_s_acf_descrip,lba_acf_descrip,0,240);
		XPLMGetDatab(m_s_acf_tailnumber,lba_acf_tailnumber,0,40);
 
		m_ls_acf_descrip = str(lba_acf_descrip) + str(lba_acf_tailnumber);
 
 
		m_li_on_ground= 				XPLMGetDatai(m_i_on_ground);
		m_lf_climb_rate= 			XPLMGetDataf(m_f_climb_rate);
 
		m_lf_gear1_ratio=			XPLMGetDataf(m_f_gear1_ratio);
		m_lf_gear2_ratio=			XPLMGetDataf(m_f_gear2_ratio);
		m_lf_gear3_ratio=			XPLMGetDataf(m_f_gear3_ratio);
		m_lf_gear4_ratio=			XPLMGetDataf(m_f_gear4_ratio);
		m_lf_gear5_ratio=			XPLMGetDataf(m_f_gear5_ratio);
 
		m_lf_ground_speed= 			XPLMGetDataf(m_f_ground_speed) 	* 3600/1852	// is m/s && we want nm/h;
		m_lf_ias= 					XPLMGetDataf(m_f_ias);
		m_lf_sun_pitch= 				XPLMGetDataf(m_f_sun_pitch);
		m_lf_airport_light= 			XPLMGetDataf(m_f_airport_light);
		m_lf_world_light_precent= 	XPLMGetDataf(m_f_world_light_precent);
		m_li_has_skid= 				XPLMGetDatai(m_i_has_skid);
		m_li_transponder_mode= 		XPLMGetDatai(m_i_transponder_mode);
		m_li_sim_ground_speed=		XPLMGetDatai(m_i_sim_ground_speed);
 
		m_li_temp_sl= 				XPLMGetDatai(m_i_temp_sl);
		m_li_dew_sl= 				XPLMGetDatai(m_i_dew_sl);
 
		m_li_landing_lights= 		XPLMGetDatai(m_i_landing_lights);
		m_li_beacon_lights= 			XPLMGetDatai(m_i_beacon_lights);
		m_li_nav_lights= 			XPLMGetDatai(m_i_nav_lights);
		m_li_strobe_lights= 			XPLMGetDatai(m_i_strobe_lights);
		m_li_taxi_lights= 			XPLMGetDatai(m_i_taxi_lights);
		m_li_cockpit_lights= 		XPLMGetDatai(m_i_cockpit_lights);
		m_lf_radio_alt= 				XPLMGetDataf(m_f_radio_alt);
		m_lf_decision_height=		XPLMGetDataf(m_f_decision_height);
		m_lf8_batter_charge= 		XPLMGetDataf(m_f8_batter_charge);
 
		m_li_battery_on = 			XPLMGetDatai(m_i_battery_on);
		m_li_gpu_on = 				XPLMGetDatai(m_i_gpu_on);
 
		m_li_flaps_overspeed = 	    XPLMGetDatai(m_i_flaps_overspeed);
		m_li_gear_overspeed = 	    XPLMGetDatai(m_i_gear_overspeed);
		m_li_aircraft_overspeed =    XPLMGetDatai(m_i_aircraft_overspeed);
		m_lf_aircraft_vne = 			XPLMGetDataf(m_f_aircraft_vne);
		m_li_stall = 				XPLMGetDatai(m_i_stall);
 
		m_li_cloud_0 = 				XPLMGetDatai(m_i_cloud_0);
		m_li_cloud_1 = 				XPLMGetDatai(m_i_cloud_1);
		m_li_cloud_2 = 				XPLMGetDatai(m_i_cloud_2);
		m_lf_visibility = 			XPLMGetDataf(m_f_visibility);
		m_li_rain = 					XPLMGetDatai(m_i_rain);
		m_li_thunder = 				XPLMGetDatai(m_i_thunder);
		m_li_turbulence = 			XPLMGetDatai(m_i_turbulence);
 
 
		m_li_batt1= 					XPLMGetDatai(m_i_batt1);
		m_li_batt2= 					XPLMGetDatai(m_i_batt2);
 
		m_li_tire1= 					XPLMGetDatai(m_i_tire1);
		m_li_tire2= 					XPLMGetDatai(m_i_tire2);
		m_li_tire3= 					XPLMGetDatai(m_i_tire3);
		m_li_tire4= 					XPLMGetDatai(m_i_tire4);
		m_li_tire5= 					XPLMGetDatai(m_i_tire5);
 
		m_li_fire1= 					XPLMGetDatai(m_i_fire1);
		m_li_fire2= 					XPLMGetDatai(m_i_fire2);
		m_li_fire3= 					XPLMGetDatai(m_i_fire3);
		m_li_fire4= 					XPLMGetDatai(m_i_fire4);
		m_li_fire5= 					XPLMGetDatai(m_i_fire5);
		m_li_fire6= 					XPLMGetDatai(m_i_fire6);
		m_li_fire7= 					XPLMGetDatai(m_i_fire7);
		m_li_fire8= 					XPLMGetDatai(m_i_fire8);
 
		m_li_flameout1= 				XPLMGetDatai(m_i_flameout1);
		m_li_flameout2= 				XPLMGetDatai(m_i_flameout2);
		m_li_flameout3=				XPLMGetDatai(m_i_flameout3);
		m_li_flameout4= 				XPLMGetDatai(m_i_flameout4);
		m_li_flameout5= 				XPLMGetDatai(m_i_flameout5);
		m_li_flameout6= 				XPLMGetDatai(m_i_flameout6);
		m_li_flameout7= 				XPLMGetDatai(m_i_flameout7);
		m_li_flameout8= 				XPLMGetDatai(m_i_flameout8);
 
 
 
		m_li_engine_failure1= 		XPLMGetDatai(m_i_engine_failure1);
		m_li_engine_failure2= 		XPLMGetDatai(m_i_engine_failure2);
		m_li_engine_failure3= 		XPLMGetDatai(m_i_engine_failure3);
		m_li_engine_failure4= 		XPLMGetDatai(m_i_engine_failure4);
		m_li_engine_failure5= 		XPLMGetDatai(m_i_engine_failure5);
		m_li_engine_failure6= 		XPLMGetDatai(m_i_engine_failure6);
		m_li_engine_failure7= 		XPLMGetDatai(m_i_engine_failure7);
		m_li_engine_failure8= 		XPLMGetDatai(m_i_engine_failure8);
 
		m_li_hot1= 					XPLMGetDatai(m_i_hot1);
		m_li_hot2= 					XPLMGetDatai(m_i_hot2);
		m_li_hot3= 					XPLMGetDatai(m_i_hot3);
		m_li_hot4= 					XPLMGetDatai(m_i_hot4);
		m_li_hot5= 					XPLMGetDatai(m_i_hot5);
		m_li_hot6= 					XPLMGetDatai(m_i_hot6);
		m_li_hot7= 					XPLMGetDatai(m_i_hot7);
		m_li_hot8= 					XPLMGetDatai(m_i_hot8);
 
		m_lf_ice_frame = 			XPLMGetDataf(m_f_ice_frame);
		m_lf_ice_pitot = 			XPLMGetDataf(m_f_ice_pitot);
		m_lf_ice_propeller = 		XPLMGetDataf(m_f_ice_propeller);
		m_lf_ice_window = 			XPLMGetDataf(m_f_ice_window);
 
		m_li_bird = 					XPLMGetDatai(m_i_bird);
 
		m_lf_g_normal= 				XPLMGetDataf(m_f_g_normal);
		m_lf_g_forward= 				XPLMGetDataf(m_f_g_forward);
		m_lf_g_side= 				XPLMGetDataf(m_f_g_side);
 
 
		m_lf_pitch= 					XPLMGetDataf(m_f_pitch);
		m_lf_roll= 					XPLMGetDataf(m_f_roll);
		m_lf_yaw= 					XPLMGetDataf(m_f_yaw);
 
 
		m_lf_cab_press= 				XPLMGetDataf(m_f_cab_press);
		m_lf_cab_rate= 				XPLMGetDataf(m_f_cab_rate);
		//cab humidity ?;
		//cab temp ?;
 
		m_lf_outside_temp1= 			XPLMGetDataf(m_f_outside_temp1);
		m_lf_outside_temp2= 			XPLMGetDataf(m_f_outside_temp2);
		m_lf_outside_temp3= 			XPLMGetDataf(m_f_outside_temp3);
 
		m_lf_baro_set = 				XPLMGetDataf(m_f_baro_set);
		m_li_baro_set = 				int(m_lf_baro_set * 100);
		m_lf_baro_sea_level = 		XPLMGetDataf(m_f_baro_sea_level);
		m_li_baro_sea_level = 		int(m_lf_baro_sea_level * 100);
		m_lf_baro_alt = 				XPLMGetDataf(m_f_baro_alt);
 
		m_lf_wind_direction = 		XPLMGetDataf(m_f_wind_direction);
		m_lf_wind_speed_kt = 		XPLMGetDataf(m_f_wind_speed_kt);
 
		m_lf_slats_1 = 				XPLMGetDataf(m_f_slats_1);
		m_lf_flaps_1 = 				XPLMGetDataf(m_f_flaps_1);
 
		m_ld_latitude = 				XPLMGetDatad(m_d_latitude);
		m_ld_longitude = 			XPLMGetDatad(m_d_longitude);
 
		m_li_nonsmoking =            XPLMGetDatai(m_i_nonsmoking);
		m_li_fastenseatbelts =       XPLMGetDatai(m_i_fastenseatbelt);
		m_li_replay = 				XPLMGetDatai(m_i_replay);
 
		m_ivyAircraft.UpdateData();
 
		m_data_read_valid = true;
 
		////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// End of DATAREF Local Variables;
		pass;
 