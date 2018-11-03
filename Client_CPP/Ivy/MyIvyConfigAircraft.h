#pragma once
#define IVY_FS_MAX 10
#include "Ivy.h"

// OS X: we use this to convert our file path.
#if APL
#include <Carbon/Carbon.h>
#endif

// Your include paths for OpenAL may vary by platform.
#include "al.h"
#include "alc.h"

class MyIvyConfigAircraft
{
public:
	bool m_vspeeds_enabled = false;
	XPLMDataRef m_i_v1;
	XPLMDataRef m_i_vr;
	XPLMDataRef m_i_v2;

	XPLMDataRef m_f_slats;
	XPLMDataRef m_f_flaps;
	
	int m_li_v1 = 0;
	int m_li_vr = 0;
	int m_li_v2 = 0;

	std::string m_li_v1_data_ref = "";
	std::string m_li_vr_data_ref = "";
	std::string m_li_v2_data_ref = "";

	bool m_v_array = false;
	int m_v_array_size = 0;
	int m_v1_pos = -1;
	int m_v2_pos = -1;
	int m_vr_pos = -1;

	bool m_slats_enabled = false;
	bool m_flaps_enabled = false;
	float m_lf_flaps = 0;
	float m_lf_slats = 0;
	float m_flaps_tolerance = 0;
	float m_slats_tolerance = 0;
	std::string m_lf_flaps_data_ref = "";
	std::string m_lf_slats_data_ref = "";

	int m_flaps_deploy_value[IVY_FS_MAX];
	int m_flaps_deploy_pos[IVY_FS_MAX];
	int m_flaps_count_max = 10;
	int m_slats_count_max = 10;

	int m_slats_deploy_value[IVY_FS_MAX];
	float m_slats_deploy_pos[IVY_FS_MAX];

	bool m_dataref_init = false;

	char m_name[1024] = "UnconfiguredIvyAircraft";

	MyIvyConfigAircraft(char * aircraft_config_path);
	~MyIvyConfigAircraft();

	void InitDataRefs();
	void UpdateData();
	void ReadConfigFile(char * aircraft_config_path);
};

