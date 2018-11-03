#include "MyIvyConfigAircraft.h"

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>





MyIvyConfigAircraft::MyIvyConfigAircraft(char * aircraft_config_path)
{
	if (aircraft_config_path != "")
		ReadConfigFile(aircraft_config_path);
}


MyIvyConfigAircraft::~MyIvyConfigAircraft()
{
}

void MyIvyConfigAircraft::InitDataRefs()
{
	m_dataref_init = true;

	if (m_vspeeds_enabled == true)
	{
		if (m_v_array == false)
		{
			m_i_v1 = XPLMFindDataRef(m_li_v1_data_ref.c_str());
				m_i_vr = XPLMFindDataRef(m_li_vr_data_ref.c_str());
				m_i_v2 = XPLMFindDataRef(m_li_v2_data_ref.c_str());
		}
		else m_i_v1 = XPLMFindDataRef(m_li_v1_data_ref.c_str());

		if (m_slats_enabled == true)
			m_f_slats = XPLMFindDataRef(m_lf_slats_data_ref.c_str());

		if (m_flaps_enabled == true) 
			m_f_flaps = XPLMFindDataRef(m_lf_flaps_data_ref.c_str());
	}


}

void MyIvyConfigAircraft::UpdateData()
{
	if (m_dataref_init == false) InitDataRefs();

	if (m_vspeeds_enabled == true)
	{
		// Handling via direct variables, e.g., CL300
		if (m_v_array == false)
		{
			if (m_li_v1_data_ref != "")		m_li_v1 = XPLMGetDatai(m_i_v1);
			if (m_li_vr_data_ref != "")		m_li_vr = XPLMGetDatai(m_i_vr);
			if (m_li_v2_data_ref != "")		m_li_v2 = XPLMGetDatai(m_i_v2);
		}

		// Handling for the Rotate MD80
		else if (m_li_v1_data_ref != "")
		{
			float v_array[20];
			XPLMGetDatavf(m_i_v1, v_array, 0, m_v_array_size);
			if (m_v1_pos != -1)
				m_li_v1 = v_array[m_v1_pos];
			if (m_vr_pos != -1)
				m_li_vr = v_array[m_vr_pos];
			if (m_v2_pos != -1)
				m_li_v2 = v_array[m_v2_pos];
		}
	}

	if (m_slats_enabled == true)
		if (m_lf_slats_data_ref != "")	m_lf_slats = XPLMGetDataf(m_f_slats);

	if (m_flaps_enabled == true)
		if (m_lf_flaps_data_ref != "")	m_lf_flaps = XPLMGetDataf(m_f_flaps);
}

void MyIvyConfigAircraft::ReadConfigFile(char * aircraft_config_path)
{
	boost::property_tree::ptree pt;
	boost::property_tree::ini_parser::read_ini(aircraft_config_path, pt);

	try { strcpy(m_name, pt.get<std::string>("IVY_AIRCRAFT.aircraft_name").c_str()); }
	catch(...) { XPLMDebugString("IvyAircraftConfig: No aircraft_name.\n"); }

	try { m_vspeeds_enabled = pt.get<bool>("IVY_AIRCRAFT.vspeeds_enabled"); }
	catch (...) { XPLMDebugString("IvyAircraftConfig: No vspeeds_enabled.\n"); }

	try { m_li_v1_data_ref = pt.get<std::string>("IVY_AIRCRAFT.v1_data_ref"); }
	catch (...) { XPLMDebugString("IvyAircraftConfig: No v1_data_ref.\n"); }

	try { m_li_vr_data_ref = pt.get<std::string>("IVY_AIRCRAFT.vr_data_ref"); }
	catch (...) { XPLMDebugString("IvyAircraftConfig: No vr_data_ref.\n"); }

	try { m_li_v2_data_ref = pt.get<std::string>("IVY_AIRCRAFT.v2_data_ref"); }
	catch (...) { XPLMDebugString("IvyAircraftConfig: No v2_data_ref.\n"); }

	try { m_v_array = pt.get<bool>("IVY_AIRCRAFT.v_array"); }
	catch (...) { XPLMDebugString("IvyAircraftConfig: No v_array.\n"); }

	try { m_v_array_size = pt.get<int>("IVY_AIRCRAFT.v_array_size"); }
	catch (...) { XPLMDebugString("IvyAircraftConfig: No v_array_size.\n"); }

	try { m_v1_pos = pt.get<int>("IVY_AIRCRAFT.v1_pos"); }
	catch (...) { XPLMDebugString("IvyAircraftConfig: No v1_pos.\n"); }

	try { m_v2_pos = pt.get<int>("IVY_AIRCRAFT.v2_pos"); }
	catch (...) { XPLMDebugString("IvyAircraftConfig: No v2_pos.\n"); }

	try { m_vr_pos = pt.get<int>("IVY_AIRCRAFT.vr_pos"); }
	catch (...) { XPLMDebugString("IvyAircraftConfig: No vr_pos.\n"); }

	try { m_li_v1 = pt.get<int>("IVY_AIRCRAFT.v1_static"); }
	catch (...) { XPLMDebugString("IvyAircraftConfig: No v1_static.\n"); }

	try { m_li_v2 = pt.get<int>("IVY_AIRCRAFT.v2_static"); }
	catch (...) { XPLMDebugString("IvyAircraftConfig: No v2_static.\n"); }

	try { m_li_vr = pt.get<int>("IVY_AIRCRAFT.vr_static"); }
	catch (...) { XPLMDebugString("IvyAircraftConfig: No vr_static.\n"); }

	try { m_slats_enabled = pt.get<bool>("IVY_AIRCRAFT.slats_enabled"); }
	catch (...) { XPLMDebugString("IvyAircraftConfig: No slats_enabled.\n"); }

	try { m_lf_slats_data_ref = pt.get<std::string>("IVY_AIRCRAFT.slats_data_ref"); }
	catch (...) { XPLMDebugString("IvyAircraftConfig: No slats_data_ref.\n"); }

	try { m_slats_tolerance = pt.get<float>("IVY_AIRCRAFT.slats_tolerance"); }
	catch (...) { XPLMDebugString("IvyAircraftConfig: No slats_tolerance.\n"); }

	try { m_flaps_enabled = pt.get<bool>("IVY_AIRCRAFT.flaps_enabled"); }
	catch (...) { XPLMDebugString("IvyAircraftConfig: No flaps_enabled.\n"); }

	try { m_lf_flaps_data_ref = pt.get<std::string>("IVY_AIRCRAFT.flaps_data_ref"); }
	catch (...) { XPLMDebugString("IvyAircraftConfig: No flaps_data_ref.\n"); }

	try { m_flaps_tolerance = pt.get<float>("IVY_AIRCRAFT.flaps_tolerance"); }
	catch (...) { XPLMDebugString("IvyAircraftConfig: No flaps_tolerance.\n"); }

	for (int index_number = 0; index_number < IVY_FS_MAX; index_number++)
	{
		char buffer[1024];

		sprintf(buffer,"IVY_AIRCRAFT.slats_value_%i", index_number);
		try { m_slats_deploy_value[index_number] = pt.get<float>(buffer); }
		catch (...) {}

		sprintf(buffer, "IVY_AIRCRAFT.slats_position_%i", index_number);
		try { m_slats_deploy_pos[index_number] = pt.get<float>(buffer); }
		catch (...) {}

	}

	for (int index_number = 0; index_number < IVY_FS_MAX; index_number++)
	{
		char buffer[1024];

		sprintf(buffer, "IVY_AIRCRAFT.slats_value_%i", index_number);
		try { m_slats_deploy_value[index_number] = pt.get<float>(buffer); }
		catch (...) {}

		sprintf(buffer, "IVY_AIRCRAFT.slats_position_%i", index_number);
		try { m_slats_deploy_pos[index_number] = pt.get<float>(buffer); }
		catch (...) {}

	}

	for (int index_number = 0; index_number < IVY_FS_MAX; index_number++)
	{
		char buffer[1024];

		sprintf(buffer, "IVY_AIRCRAFT.flaps_value_%i", index_number);
		try { m_flaps_deploy_value[index_number] = pt.get<float>(buffer); }
		catch (...) {}

		sprintf(buffer, "IVY_AIRCRAFT.flaps_position_%i", index_number);
		try { m_flaps_deploy_pos[index_number] = pt.get<float>(buffer); }
		catch (...) {}

	}

}
