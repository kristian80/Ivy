#include "IvyPassengers.h"



IvyPassengers::IvyPassengers(MyIvyConfiguration *pivyConfig, ALuint channel, XPSound *xpSound)
{
	LoadSound(pivyConfig, channel, xpSound);
}


IvyPassengers::~IvyPassengers()
{
}

void IvyPassengers::LoadSound(MyIvyConfiguration *pivyConfig, ALuint channel, XPSound *xpSound)
{
	mp_ivyConfig = pivyConfig;
	m_is_screaming = false;
	//m_fading = false;
	mXPSound = xpSound;
	m_passengerChannel = channel;
	m_gain = 0;


	m_screamSound = mXPSound->CreateBuffer(pivyConfig->m_mp3_path + "passenger_screams.wav");
	mXPSound->SetSoundGain(m_passengerChannel, m_gain);
	mXPSound->PlaySingleSound(m_passengerChannel, m_screamSound);
}

void IvyPassengers::MakeScream(bool screaming, float gain)
{
	
	if ((screaming == true) && (m_gain < gain))
	{
		m_gain = min(m_gain + m_gain_step, 1); // Limit gain to 1
		m_is_screaming = true;
	}
	else if ((screaming == true) && (m_gain > gain))
	{
		m_gain = max(m_gain - m_gain_step, 0); // Limit gain to 1
		m_is_screaming = true;
	}
	else if ((screaming == false) && (m_gain > 0))
	{
		m_gain = max(m_gain - m_gain_step, 0);
		m_is_screaming = false;
	}
	mXPSound->SetSoundGain(m_passengerChannel, m_gain);
}
