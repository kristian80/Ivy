#include "IvyLandingDetection.h"



IvyLandingDetection::IvyLandingDetection(float time, float sink_rate, float g_normal, float g_side, float g_forward)
{
	m_time = time;
	m_sink_rate = sink_rate;
	m_g_normal = g_normal;
	m_g_side = g_side;
	m_g_forward = g_forward;
	m_rating = 0;
	RateLanding();
}


IvyLandingDetection::~IvyLandingDetection()
{
}

void IvyLandingDetection::RateLanding(void)
{
	if ((m_sink_rate > -100) && (m_g_normal < 1.5)) 
		m_rating = 1;
	else if ((m_sink_rate > -250) && (m_g_normal < 2)) 
		m_rating = 2;
	else if ((m_sink_rate > -400) && (m_g_normal < 3))
		m_rating = 3;
	else if ((m_sink_rate > -500) && (m_g_normal < 4))
		m_rating = 4;
	else 
		m_rating = 5;
}

int IvyLandingDetection::GetCurrentRate(float last_landing_time, float max_time)
{
	if ((last_landing_time - m_time) < max_time)
		return m_rating;
	else
		return 0;
}
