#include "XPSound.h"



XPSound::XPSound()
{


}


XPSound::~XPSound()
{
	/*for (std::list<ALuint>::iterator it_buffer = m_buffer_list.begin(); it_buffer != m_buffer_list.end(); ++it_buffer)
	{
		ALuint ali_buffer = *it_buffer;
		RemoveBuffer(ali_buffer);
	}
	for (std::list<ALuint>::iterator it_sound = m_sound_list.begin(); it_sound != m_sound_list.end(); ++it_sound)
	{
		ALuint ali_sound = *it_sound;
		RemoveSound(ali_sound);
	}*/

	while (m_sound_list.size() != 0)
	{
		ALuint ali_sound = *m_sound_list.begin();
		m_sound_list.pop_front();
		RemoveSound(ali_sound);
	}

	while (m_buffer_list.size() != 0)
	{
		ALuint ali_buffer = *m_buffer_list.begin();
		m_buffer_list.pop_front();
		RemoveBuffer(ali_buffer);
	}

	if (mpSoundCtx) alcDestroyContext(mpSoundCtx);
	if (mpSoundDevice) alcCloseDevice(mpSoundDevice);
}


// Initialize OpenAL
int XPSound::InitSound(char * p_file_path)
{
	char buf[2048];
	XPLMDebugString("Ivy: Init Sound.\n");
	// We have to save the old context and restore it later, so that we don't interfere with X-Plane
	// and other plugins.

	ALCcontext * old_ctx = alcGetCurrentContext();

	// Try to create our own default device and context.  If we fail, we're dead, we won't play any sound.

	strcpy(mp_mp3_path, p_file_path);

	mpSoundDevice = alcOpenDevice(NULL);
	if (mpSoundDevice == NULL)
	{
		XPLMDebugString("Ivy: Could not open the default OpenAL device.\n");
		return 0;
	}
	mpSoundCtx = alcCreateContext(mpSoundDevice, NULL);
	if (mpSoundCtx == NULL)
	{
		if (old_ctx)
			alcMakeContextCurrent(old_ctx);
		alcCloseDevice(mpSoundDevice);
		mpSoundDevice = NULL;
		XPLMDebugString("Ivy: Could not create a context.\n");
		return 0;
	}

	// Make our context current, so that OpenAL commands affect our, um, stuff.

	alcMakeContextCurrent(mpSoundCtx);


	if (old_ctx)
		alcMakeContextCurrent(old_ctx);
	return 0.0f;
}

// Given a chunk, find its end by going back to the header.
char * XPSound::WaveChunkEnd(char * chunk_start, int swapped)
{
	chunk_header * h = (chunk_header *)(chunk_start - sizeof(chunk_header));
	return chunk_start + (swapped ? SWAP_32(h->size) : h->size);
}

// Load a Wave file OpenAL
ALuint XPSound::LoadWave(char * p_file_name)
{
	// First: we open the file and copy it into a single large memory buffer for processing.
	
	char p_full_path[2048];

	strcpy(p_full_path, mp_mp3_path);
	strcat(p_full_path, p_file_name);

	FILE * fp = fopen(p_full_path, "rb");
	char debug_msg[1024];

	sprintf(debug_msg, "Ivy: reading file: %s\n", p_full_path);
	XPLMDebugString(debug_msg);

	if (fp == NULL)
	{
		XPLMDebugString("Ivy: WAVE file load failed - could not open.\n");
		sprintf(debug_msg, "Ivy: Filename: %s", p_full_path);
		XPLMDebugString(debug_msg);
		return 0;
	}

	fseek(fp, 0, SEEK_END);
	int file_size = ftell(fp);
	fseek(fp, 0, SEEK_SET);
	char * mem = (char*)malloc(file_size);


	if (mem == NULL)
	{
		XPLMDebugString("Ivy: WAVE file load failed - could not allocate memory.\n");
		sprintf(debug_msg, "Ivy: Filename: %s", p_full_path);
		XPLMDebugString(debug_msg);
		fclose(fp);
		return 0;
	}

	if (fread(mem, 1, file_size, fp) != file_size)
	{
		XPLMDebugString("Ivy: WAVE file load failed - could not read file.\n");
		sprintf(debug_msg, "Ivy: Filename: %s", p_full_path);
		XPLMDebugString(debug_msg);
		free(mem);
		fclose(fp);
		return 0;
	}
	fclose(fp);
	char * mem_end = mem + file_size;

	// Second: find the RIFF chunk.  Note that by searching for RIFF both normal
	// and reversed, we can automatically determine the endian swap situation for
	// this file regardless of what machine we are on.

	int swapped = 0;
	char * riff = WaveFindChunk(mem, mem_end, RIFF_ID, 0);
	if (riff == NULL)
	{
		riff = WaveFindChunk(mem, mem_end, RIFF_ID, 1);
		if (riff)
			swapped = 1;
		else
			FAIL("Could not find RIFF chunk in wave file.\n")
	}

	// The wave chunk isn't really a chunk at all. :-(  It's just a "WAVE" tag 
	// followed by more chunks.  This strikes me as totally inconsistent, but
	// anyway, confirm the WAVE ID and move on.

	if (riff[0] != 'W' ||
		riff[1] != 'A' ||
		riff[2] != 'V' ||
		riff[3] != 'E')
		FAIL("Ivy: Could not find WAVE signature in wave file.\n")

		char * format = WaveFindChunk(riff + 4, WaveChunkEnd(riff, swapped), FMT_ID, swapped);
	if (format == NULL)
		FAIL("Ivy: Could not find FMT  chunk in wave file.\n")

		// Find the format chunk, and swap the values if needed.  This gives us our real format.

		format_info * fmt = (format_info *)format;
	if (swapped)
	{
		fmt->format = SWAP_16(fmt->format);
		fmt->num_channels = SWAP_16(fmt->num_channels);
		fmt->sample_rate = SWAP_32(fmt->sample_rate);
		fmt->byte_rate = SWAP_32(fmt->byte_rate);
		fmt->block_align = SWAP_16(fmt->block_align);
		fmt->bits_per_sample = SWAP_16(fmt->bits_per_sample);
	}

	// Reject things we don't understand...expand this code to support weirder audio formats.

	if (fmt->format != 1) FAIL("Ivy: Wave file is not PCM format data.\n")
		if (fmt->num_channels != 1 && fmt->num_channels != 2) FAIL("Must have mono or stereo sound.\n")
			if (fmt->bits_per_sample != 8 && fmt->bits_per_sample != 16) FAIL("Must have 8 or 16 bit sounds.\n")
				char * data = WaveFindChunk(riff + 4, WaveChunkEnd(riff, swapped), DATA_ID, swapped);
	if (data == NULL)
		FAIL("Ivy: I could not find the DATA chunk.\n")

	int sample_size = fmt->num_channels * fmt->bits_per_sample / 8;
	int data_bytes = WaveChunkEnd(data, swapped) - data;
	int data_samples = data_bytes / sample_size;

	// If the file is swapped and we have 16-bit audio, we need to endian-swap the audio too or we'll 
	// get something that sounds just astoundingly bad!

	if (fmt->bits_per_sample == 16 && swapped)
	{
		short * ptr = (short *)data;
		int words = data_samples * fmt->num_channels;
		while (words--)
		{
			*ptr = SWAP_16(*ptr);
			++ptr;
		}
	}

	// Finally, the OpenAL crud.  Build a new OpenAL buffer and send the data to OpenAL, passing in
	// OpenAL format enums based on the format chunk.

	ALuint buf_id = 0;
	alGenBuffers(1, &buf_id);
	if (buf_id == 0) FAIL("Ivy: Could not generate openal buffer id.\n");

	alBufferData(buf_id, fmt->bits_per_sample == 16 ?
		(fmt->num_channels == 2 ? AL_FORMAT_STEREO16 : AL_FORMAT_MONO16) :
		(fmt->num_channels == 2 ? AL_FORMAT_STEREO8 : AL_FORMAT_MONO8),
		data, data_bytes, fmt->sample_rate);
	free(mem);
	XPLMDebugString("Ivy: WAVE loaded.\n");
	return buf_id;
}

// This utility returns the start of data for a chunk given a range of bytes it might be within.  Pass 1 for
// swapped if the machine is not the same endian as the file.
char *	XPSound::WaveFindChunk(char * file_begin, char * file_end, int desired_id, int swapped)
{
	while (file_begin < file_end)
	{
		chunk_header * h = (chunk_header *)file_begin;
		if (h->id == desired_id && !swapped)
			return file_begin + sizeof(chunk_header);
		if (h->id == SWAP_32(desired_id) && swapped)
			return file_begin + sizeof(chunk_header);
		int chunk_size = swapped ? SWAP_32(h->size) : h->size;
		char * next = file_begin + chunk_size + sizeof(chunk_header);
		if (next > file_end || next <= file_begin)
			return NULL;
		file_begin = next;
	}
	return NULL;
}

// This is a stupid logging error function...useful for debugging, but not good error checking.
void XPSound::CheckOpenALError(void)
{
	ALuint e = alGetError();
	if (e != AL_NO_ERROR)
		printf("ERROR: %d\n", e);
}

ALuint XPSound::CreateBuffer(char * file_name)
{
	// Context Switch
	if (mpSoundCtx == NULL)
	{
		XPLMDebugString("Ivy: No Sound Context.\n");
		return false;
	}
	ALCcontext * old_ctx = alcGetCurrentContext();
	alcMakeContextCurrent(mpSoundCtx);

#if APL
	ConvertPath(file_name, file_name, sizeof(file_name));
#endif

	// Generate 1 source and load a buffer of audio.
	
	ALuint ali_sound_buffer = LoadWave(file_name);
	CheckOpenALError();

	// Basic initializtion code to play a sound: specify the buffer the source is playing, as well as some 
	// sound parameters. This doesn't play the sound - it's just one-time initialization.
	
	//alSourcei(ali_sound_source, AL_BUFFER, m_snd_buffer);

	// Restore old Context
	if (old_ctx)	alcMakeContextCurrent(old_ctx);

	m_buffer_list.push_back(ali_sound_buffer);
	return ali_sound_buffer;
}

void XPSound::RemoveBuffer(ALuint ali_sound_buffer)
{
	// Context Switch
	if (mpSoundCtx == NULL)		return;
	ALCcontext * old_ctx = alcGetCurrentContext();
	alcMakeContextCurrent(mpSoundCtx);

	alDeleteBuffers(1, &ali_sound_buffer);
	m_buffer_list.remove(ali_sound_buffer);

	// Restore old Context
	if (old_ctx)	alcMakeContextCurrent(old_ctx);
}

ALuint XPSound::CreateSound(ALenum looping)
{
	// Context Switch
	if (mpSoundCtx == NULL)
	{
		XPLMDebugString("Ivy: No Sound Context.\n");
		return false;
	}
	ALCcontext * old_ctx = alcGetCurrentContext();
	alcMakeContextCurrent(mpSoundCtx);


	ALuint ali_sound_source = 0;
	ALfloat	zero[3] = { 0 };

	alGenSources(1, &ali_sound_source);
	CheckOpenALError();

	m_sound_list.push_back(ali_sound_source);

	alSourcef(ali_sound_source, AL_PITCH, 1.0f);
	alSourcef(ali_sound_source, AL_GAIN, 1.0f);
	alSourcei(ali_sound_source, AL_LOOPING, looping);
	alSourcefv(ali_sound_source, AL_POSITION, zero);
	alSourcefv(ali_sound_source, AL_VELOCITY, zero);
	CheckOpenALError();

	// Restore old Context
	if (old_ctx)	alcMakeContextCurrent(old_ctx);

	return ali_sound_source;
}

bool XPSound::PlaySingleSound(ALuint ali_sound_source, ALuint ali_buffer_source, float pitch)
{
	char debug_msg[1024];
	XPLMDebugString("Ivy: PlaySingleSound.\n");

	sprintf(debug_msg, "Ivy: Play CTX: %i, Sound %i, Buffer %i\n", (int) mpSoundCtx, (int) ali_sound_source, (int) ali_buffer_source);
	XPLMDebugString(debug_msg);

	bool played = false;
	// Context Switch
	if (mpSoundCtx == NULL)
	{
		XPLMDebugString("Ivy: No Sound Context.\n");
		return false;
	}
	ALCcontext * old_ctx = alcGetCurrentContext();
	alcMakeContextCurrent(mpSoundCtx);
	
	// get the state
	ALint source_state = 0;
	alGetSourcei(ali_sound_source, AL_SOURCE_STATE, &source_state);

	sprintf(debug_msg, "Ivy: Source State %i\n", (int)source_state);
	XPLMDebugString(debug_msg);

	// do not interrupt currently played sound
	if (source_state != AL_PLAYING)
	{
		XPLMDebugString("Ivy: AL_STOPPED.\n");
		alSourcei(ali_sound_source, AL_BUFFER, ali_buffer_source);
		alSourcef(ali_sound_source, AL_PITCH, pitch);
		alSourcePlay(ali_sound_source);
		played = true;
	}
	else
	{
		XPLMDebugString("Ivy: NOT AL_STOPPED.\n");
	}
	
	// Restore old Context
	if (old_ctx)	alcMakeContextCurrent(old_ctx);
	return played;
}

bool XPSound::IsPlayingSound(ALuint ali_sound_source)
{
	bool playing = true;
	// Context Switch
	if (mpSoundCtx == NULL)		return false;
	ALCcontext * old_ctx = alcGetCurrentContext();
	alcMakeContextCurrent(mpSoundCtx);

	// get the state
	ALint source_state = 0;
	alGetSourcei(ali_sound_source, AL_SOURCE_STATE, &source_state);

	// do not interrupt currently played sound
	if (source_state != AL_PLAYING) playing = false;

	// Restore old Context
	if (old_ctx)	alcMakeContextCurrent(old_ctx);
	return playing;
}

void XPSound::SetSoundPitch(ALuint ali_sound_source, float pitch)
{
	// Context Switch
	if (mpSoundCtx == NULL)
	{
		XPLMDebugString("Ivy: No Sound Context.\n");
		return;
	}
	ALCcontext * old_ctx = alcGetCurrentContext();
	alcMakeContextCurrent(mpSoundCtx);

	alSourcef(ali_sound_source, AL_PITCH, pitch);

	// Restore old Context
	if (old_ctx)	alcMakeContextCurrent(old_ctx);
}

void XPSound::RemoveSound(ALuint ali_sound_source)
{
	// Context Switch
	if (mpSoundCtx == NULL)
	{
		XPLMDebugString("Ivy: No Sound Context.\n");
		return ;
	}
	ALCcontext * old_ctx = alcGetCurrentContext();
	alcMakeContextCurrent(mpSoundCtx);

	alDeleteSources(1, &ali_sound_source);
	m_sound_list.remove(ali_sound_source);

	// Restore old Context
	if (old_ctx)	alcMakeContextCurrent(old_ctx);
}
