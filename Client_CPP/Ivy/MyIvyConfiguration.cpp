#include "MyIvyConfiguration.h"

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>


MyIvyConfiguration::MyIvyConfiguration()
{
	char buffer[2048];
	XPLMGetSystemPath(buffer);

	m_system_path = buffer;

	m_mp3_dir = "IvyMP3s";
	m_mp3_path = m_system_path + "\\Resources\\plugins\\Ivy\\" + m_mp3_dir + "\\";
	m_number_path = m_mp3_path + "numbers\\";
	m_ini_path = m_system_path + "\\Resources\\plugins\\Ivy\\Ivy.ini";
	m_config_path = m_system_path + "\\Resources\\plugins\\Ivy\\IvyConfig\\";
	m_logbook_path = m_system_path + "\\Resources\\plugins\\Ivy\\IvyConfig\\IvyLogbook.txt";
}


MyIvyConfiguration::~MyIvyConfiguration()
{
}

void MyIvyConfiguration::WriteConfig()
{
	boost::property_tree::ptree pt;

	pt.put("IVY_SETTINGS.mp3_dir", m_mp3_dir);
	pt.put("IVY_SETTINGS.passengers_enabled", m_passengers_enabled);

	pt.put("IVY_SETTINGS.pos_rate_climb", m_pos_rate_climb);
	pt.put("IVY_SETTINGS.ivy_ouch_g", m_ivy_ouch_g);
	pt.put("IVY_SETTINGS.brake_max_forward_g", m_brake_max_forward_g);
	pt.put("IVY_SETTINGS.alt_landing_lights_low", m_alt_landing_lights_low);
	pt.put("IVY_SETTINGS.alt_landing_lights_high", m_alt_landing_lights_high);
	pt.put("IVY_SETTINGS.night_world_light_precent", m_night_world_light_precent);
	pt.put("IVY_SETTINGS.taxi_ground_speed_min", m_taxi_ground_speed_min);
	pt.put("IVY_SETTINGS.vis_is_fog", m_vis_is_fog);
	pt.put("IVY_SETTINGS.cab_rate_low", m_cab_rate_low);
	pt.put("IVY_SETTINGS.cab_rate_high", m_cab_rate_high);
	pt.put("IVY_SETTINGS.cab_rate_reset_hysteresis", m_cab_rate_reset_hysteresis);
	pt.put("IVY_SETTINGS.bank_reset_low", m_bank_reset_low);
	pt.put("IVY_SETTINGS.bank_low", m_bank_low);
	pt.put("IVY_SETTINGS.bank_high", m_bank_high);
	pt.put("IVY_SETTINGS.bank_xhigh", m_bank_xhigh);
	pt.put("IVY_SETTINGS.pitch_reset_low", m_pitch_reset_low);
	pt.put("IVY_SETTINGS.pitch_low", m_pitch_low);
	pt.put("IVY_SETTINGS.pitch_high", m_pitch_high);
	pt.put("IVY_SETTINGS.max_g_down_low_reset", m_max_g_down_low_reset);
	pt.put("IVY_SETTINGS.max_g_down_low", m_max_g_down_low);
	pt.put("IVY_SETTINGS.max_g_down_high", m_max_g_down_high);
	pt.put("IVY_SETTINGS.max_g_down_xhigh", m_max_g_down_xhigh);
	pt.put("IVY_SETTINGS.trans_alt", m_trans_alt);
	pt.put("IVY_SETTINGS.trans_hysteresis", m_trans_hysteresis);
	pt.put("IVY_SETTINGS.baro_tolerance", m_baro_tolerance);
	pt.put("IVY_SETTINGS.baro_alt_low", m_baro_alt_low);
	pt.put("IVY_SETTINGS.ice_low", m_ice_low);
	pt.put("IVY_SETTINGS.ice_high", m_ice_high);
	pt.put("IVY_SETTINGS.cab_press_low", m_cab_press_low);
	pt.put("IVY_SETTINGS.cab_press_high", m_cab_press_high);
	pt.put("IVY_SETTINGS.non_smoking_annoucetime", m_non_smoking_annoucetime);
	pt.put("IVY_SETTINGS.decition_height_arm", m_decition_height_arm);
	pt.put("IVY_SETTINGS.decition_height_plus", m_decition_height_plus);

	pt.put("IVY_SETTINGS.kt60_enabled", m_kt60_enabled);
	pt.put("IVY_SETTINGS.kt80_enabled", m_kt80_enabled);
	pt.put("IVY_SETTINGS.kt100_enabled", m_kt100_enabled);

	pt.put("IVY_SETTINGS.log_window_pos_x", m_log_window_pos_x);
	pt.put("IVY_SETTINGS.log_window_pos_y", m_log_window_pos_y);
	pt.put("IVY_SETTINGS.log_window_height", m_log_window_height);
	pt.put("IVY_SETTINGS.log_window_width", m_log_window_width);
	pt.put("IVY_SETTINGS.log_window_entries", m_log_window_entries);
	pt.put("IVY_SETTINGS.log_afc_name_length", m_log_afc_name_length);


	write_ini(m_ini_path, pt);
}

void MyIvyConfiguration::ReadConfig()
{
	boost::property_tree::ptree pt;
	boost::property_tree::ini_parser::read_ini(m_ini_path, pt);

	try { m_mp3_dir = pt.get<std::string>("IVY_SETTINGS.mp3_dir"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }

	try { m_passengers_enabled = pt.get<bool>("IVY_SETTINGS.passengers_enabled"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }

	try { m_pos_rate_climb = pt.get<float>("IVY_SETTINGS.pos_rate_climb"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_ivy_ouch_g = pt.get<float>("IVY_SETTINGS.ivy_ouch_g"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_brake_max_forward_g = pt.get<float>("IVY_SETTINGS.brake_max_forward_g"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_alt_landing_lights_low = pt.get<float>("IVY_SETTINGS.alt_landing_lights_low"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_alt_landing_lights_high = pt.get<float>("IVY_SETTINGS.alt_landing_lights_high"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_night_world_light_precent = pt.get<float>("IVY_SETTINGS.night_world_light_precent"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_taxi_ground_speed_min = pt.get<float>("IVY_SETTINGS.taxi_ground_speed_min"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_vis_is_fog = pt.get<float>("IVY_SETTINGS.vis_is_fog"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_cab_rate_low = pt.get<float>("IVY_SETTINGS.cab_rate_low"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_cab_rate_high = pt.get<float>("IVY_SETTINGS.cab_rate_high"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_cab_rate_reset_hysteresis = pt.get<float>("IVY_SETTINGS.cab_rate_reset_hysteresis"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }

	try { m_bank_reset_low = pt.get<float>("IVY_SETTINGS.bank_reset_low"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_bank_low = pt.get<float>("IVY_SETTINGS.bank_low"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_bank_high = pt.get<float>("IVY_SETTINGS.bank_high"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_bank_xhigh = pt.get<float>("IVY_SETTINGS.bank_xhigh"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }

	try { m_pitch_reset_low = pt.get<float>("IVY_SETTINGS.pitch_reset_low"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_pitch_low = pt.get<float>("IVY_SETTINGS.pitch_low"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_pitch_high = pt.get<float>("IVY_SETTINGS.pitch_high"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }

	try { m_max_g_down_low_reset = pt.get<float>("IVY_SETTINGS.max_g_down_low_reset"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_max_g_down_low = pt.get<float>("IVY_SETTINGS.max_g_down_low"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_max_g_down_high = pt.get<float>("IVY_SETTINGS.max_g_down_high"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_max_g_down_xhigh = pt.get<float>("IVY_SETTINGS.max_g_down_xhigh"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }


	try { m_trans_alt = pt.get<float>("IVY_SETTINGS.trans_alt"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_trans_hysteresis = pt.get<float>("IVY_SETTINGS.trans_hysteresis"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_baro_tolerance = pt.get<float>("IVY_SETTINGS.baro_tolerance"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_baro_alt_low = pt.get<float>("IVY_SETTINGS.baro_alt_low"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }

	try { m_ice_low = pt.get<float>("IVY_SETTINGS.ice_low"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_ice_high = pt.get<float>("IVY_SETTINGS.ice_high"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }

	try { m_cab_press_low = pt.get<float>("IVY_SETTINGS.cab_press_low"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_cab_press_high = pt.get<float>("IVY_SETTINGS.cab_press_high"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }

	try { m_non_smoking_annoucetime = pt.get<float>("IVY_SETTINGS.non_smoking_annoucetime"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }

	try { m_decition_height_arm = pt.get<float>("IVY_SETTINGS.decition_height_arm"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_decition_height_plus = pt.get<float>("IVY_SETTINGS.decition_height_plus"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }

	try { m_kt60_enabled = pt.get<bool>("IVY_SETTINGS.kt60_enabled"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_kt80_enabled = pt.get<bool>("IVY_SETTINGS.kt80_enabled"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_kt100_enabled = pt.get<bool>("IVY_SETTINGS.kt100_enabled"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }



	try { m_log_window_pos_x = pt.get<float>("IVY_SETTINGS.log_window_pos_x"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_log_window_pos_y = pt.get<float>("IVY_SETTINGS.log_window_pos_y"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_log_window_height = pt.get<float>("IVY_SETTINGS.log_window_height"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_log_window_width = pt.get<float>("IVY_SETTINGS.log_window_width"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_log_window_entries = pt.get<float>("IVY_SETTINGS.log_window_entries"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }
	try { m_log_afc_name_length = pt.get<float>("IVY_SETTINGS.log_afc_name_length"); }
	catch (...) { XPLMDebugString("IvyConfiguration: Entry not found.\n"); }

	m_mp3_path = m_system_path + "\\Resources\\plugins\\Ivy\\" + m_mp3_dir + "\\";
	m_number_path = m_mp3_path + "numbers\\";
}
