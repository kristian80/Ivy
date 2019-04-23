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
#include "Ivy.h"
#include "MyIvyConfiguration.h"
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////;
// IvyPassengers
//
// Small class to make our passenger noise

class IvyPassengers
{
	MyIvyConfiguration *mp_ivyConfig = NULL;
	ALuint m_passengerChannel = 0;
	ALuint m_screamSound = 0;
	float m_gain = 0;
	float m_gain_step = 0.05;
	bool m_is_screaming = false;
	XPSound *mXPSound;

public:
	IvyPassengers(MyIvyConfiguration *pivyConfig, ALuint channel, XPSound *xpSound);
	~IvyPassengers();
	void LoadSound(MyIvyConfiguration *pivyConfig, ALuint channel, XPSound *xpSound);
	void MakeScream(bool screaming, float gain);
};

