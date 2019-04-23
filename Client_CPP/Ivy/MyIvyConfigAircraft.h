/*
 * This file is part of the Ivy distribution (https://github.com/kristian80/Ivy).
 * Copyright (c) 2019 Kristian80.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, version 3.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 */

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

	std::string m_config_path = "";
	int m_aircraft_number = 0;

	bool m_vspeeds_enabled = false;
	XPLMDataRef m_x_v1 = 0;
	XPLMDataRef m_x_vr = 0;
	XPLMDataRef m_x_v2 = 0;

	XPLMDataRef m_x_slats = 0;
	XPLMDataRef m_x_flaps = 0;

	XPLMDataTypeID m_t_v1 = 0;
	XPLMDataTypeID m_t_vr = 0;
	XPLMDataTypeID m_t_v2 = 0;

	XPLMDataTypeID m_t_slats = 0;
	XPLMDataTypeID m_t_flaps = 0;


	int m_li_v1 = 0;
	int m_li_vr = 0;
	int m_li_v2 = 0;

	std::string m_lx_v1_data_ref = "";
	std::string m_lx_vr_data_ref = "";
	std::string m_lx_v2_data_ref = "";

	bool m_v_array = false;
	int m_v_array_size = 0;
	int m_v1_pos = 0;
	int m_v2_pos = 0;
	int m_vr_pos = 0;

	bool m_slats_enabled = false;
	bool m_flaps_enabled = false;
	float m_lf_flaps = 0;
	float m_lf_slats = 0;
	float m_flaps_tolerance = 0.05;
	float m_slats_tolerance = 0.05;
	std::string m_lf_flaps_data_ref = "sim/cockpit2/controls/flap_handle_deploy_ratio";
	std::string m_lf_slats_data_ref = "sim/cockpit2/controls/flap_handle_deploy_ratio";

	float m_flaps_deploy_value[IVY_FS_MAX];
	int m_flaps_deploy_pos[IVY_FS_MAX];
	int m_flaps_count_max = 10;
	int m_slats_count_max = 10;

	float m_slats_deploy_value[IVY_FS_MAX];
	int m_slats_deploy_pos[IVY_FS_MAX];

	bool m_dataref_init = false;

	char m_name[1024] = "UnconfiguredIvyAircraft";

	MyIvyConfigAircraft(const char * aircraft_config_path, int aircraft_number = 0, std::string m_acf_name = "");
	~MyIvyConfigAircraft();

	float GetSingleDataref(XPLMDataRef x_dataref, XPLMDataTypeID t_dataref, int array_pos = 0);

	void InitDataRefs();
	void UpdateData();
	void ReadConfigFile(const char * aircraft_config_path);
	void WriteConfigFile();
};

