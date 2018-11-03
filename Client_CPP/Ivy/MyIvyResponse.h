#pragma once

#include "Ivy.h"

#define IVY_RESPONSE_MAX_FILE 20

class MyIvyResponse
{
public:
	int m_queue_output = 0;
	int m_deactivating = 0;
	float m_time_activated = 0;
	float m_time_deactivated = 0;
	float m_time_deactivating = 0;
	float m_time_active = 0;
	int m_mute = 0;
	int m_error_count = 0;

	std::string m_event_name;
	int m_is_error;
	float m_minimum_occ;
	float m_deactivate_time;
	int m_active;
	int m_played;
	int m_active_on_load;
	int *mp_pitch;
	ALuint m_channel_number;
	ALuint m_ivyChannel;

	XPSound *mXPSound;
	
	std::vector<ALuint> m_sounds;

	MyIvyResponse(std::string event_name, std::string mp3_path, int active_on_load, float minimum_occ, float deactivate_time, int is_error, std::list<MyIvyResponse> *ivy_object_list, ALuint sound_channel, XPSound *xpSound);
	~MyIvyResponse();

	void Activate(float time);
	void Deactivate(float time);
	void SetAsPlayed(float time);
	int Play(void);
};

