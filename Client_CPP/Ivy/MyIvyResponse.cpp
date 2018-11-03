#include "MyIvyResponse.h"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <list>
#include <sys/stat.h>




MyIvyResponse::MyIvyResponse(std::string event_name, std::string mp3_path, int active_on_load, float minimum_occ, float deactivate_time, int is_error, std::list<MyIvyResponse> *ivy_object_list, ALuint sound_channel, XPSound *xpSound)
{
	m_event_name = event_name;
	m_is_error = is_error;
	m_minimum_occ = minimum_occ;
	m_deactivate_time = deactivate_time;
	m_active = active_on_load;
	m_played = active_on_load;
	m_active_on_load = active_on_load;
	m_channel_number = sound_channel;
	m_ivyChannel = sound_channel;
	mXPSound = xpSound;
	
	std::list<std::string> m_play_files;
	
	// Append this response to the ivy_object_list
	ivy_object_list->push_back(*this);

	for (int file_number = 1; file_number <= IVY_RESPONSE_MAX_FILE; ++file_number)
	{
		std::string sound_file_path = mp3_path + event_name + "_" + std::to_string(file_number) + ".wav";
		if (file_exists(sound_file_path))
		{
			m_play_files.push_back(sound_file_path);
			ALuint act_sound = xpSound->CreateBuffer(sound_file_path);

			m_sounds.push_back(act_sound);
		}
	}
}


MyIvyResponse::~MyIvyResponse()
{
}

void MyIvyResponse::Activate(float time)
{
	if (m_active == 0)
		m_time_activated = time;

	m_active = 1;

	m_time_active = time - m_time_activated;

	if ((m_time_active >= m_minimum_occ) && (m_played == 0))
		Play();
}

void MyIvyResponse::Deactivate(float time)
{
	if (m_active == 0)
		return;

	if (m_deactivating == 0)
		m_time_deactivated = time;

	m_deactivating = 1;
	m_time_deactivating = time - m_time_deactivated;

	if (m_time_deactivating >= m_deactivate_time)
	{
		m_deactivating = 0;
		m_time_deactivated = 0;
		m_active = 0;
		m_time_activated = 0;
		m_time_active = 0;
		m_played = 0;
	}
}

void MyIvyResponse::SetAsPlayed(float time)
{
	m_active = 1;
	m_played = 1;
	m_time_activated = time;
}

int MyIvyResponse::Play(void)
{
	int random_number = 0;
	if (m_sounds.size() == 0)
	{
		m_played = 1;
		return 1;
	}

	if ((m_queue_output == 0) && (mXPSound->IsPlayingSound(m_ivyChannel) == true)) // No Modulo 
		return 0;

	if (m_played == 1)
		return 0;

	if (m_is_error > 0)
		m_error_count = m_error_count + 1;

	if (m_sounds.size() > 1)
		random_number = rand() % m_sounds.size();
	else
		random_number = 0;

	if (mXPSound->PlaySingleSound(m_ivyChannel, m_sounds.at(random_number)) == true)
		m_played = 1;

	return m_played;
}
