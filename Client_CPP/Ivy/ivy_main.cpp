#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "XPLMUtilities.h"
#include "XPLMProcessing.h"
#include "XPLMPlugin.h"
#include "XPSound.h"

// OS X: we use this to convert our file path.
#if APL
#include <Carbon/Carbon.h>
#endif






/**************************************************************************************************************
 * Global Variables 
 **************************************************************************************************************/

static XPSound *pIvySound = NULL;
ALuint my_buffer = 0;
ALuint my_sound = 0;
char * p_mp3_path = "";



// Mac specific: this converts file paths from HFS (which we get from the SDK) to Unix (which the OS wants).
// See this for more info:
//
// http://www.xsquawkbox.net/xpsdk/mediawiki/FilePathsAndMacho

#if APL
int ConvertPath(const char * inPath, char * outPath, int outPathMaxLen) {

	CFStringRef inStr = CFStringCreateWithCString(kCFAllocatorDefault, inPath, kCFStringEncodingMacRoman);
	if (inStr == NULL)
		return -1;
	CFURLRef url = CFURLCreateWithFileSystemPath(kCFAllocatorDefault, inStr, kCFURLHFSPathStyle, 0);
	CFStringRef outStr = CFURLCopyFileSystemPath(url, kCFURLPOSIXPathStyle);
	if (!CFStringGetCString(outStr, outPath, outPathMaxLen, kCFURLPOSIXPathStyle))
		return -1;
	CFRelease(outStr);
	CFRelease(url);
	CFRelease(inStr);
	return 0;
}
#endif

// Initialization code.

static float InitPlugin(float elapsed, float elapsed_sim, int counter, void * ref)
{
	XPLMDebugString("Ivy: Initializing.\n");
	pIvySound = new XPSound();

	// Get MP3 Directory
	char p_dir_path[2048];
	char dirchar = *XPLMGetDirectorySeparator();
	XPLMGetPluginInfo(XPLMGetMyID(), NULL, p_dir_path, NULL, NULL);
	char * p_char = p_dir_path;
	char * p_slash = p_char;
	while (*p_char)
	{
		if (*p_char == dirchar) p_slash = p_char;
		++p_char;
	}
	++p_slash;
	*p_slash = 0;



	pIvySound->InitSound(p_dir_path);
	my_sound = pIvySound->CreateSound(AL_FALSE);
	//my_buffer = pIvySound->CreateBuffer("sound.wav");
	return 0.0f;
}

PLUGIN_API int XPluginStart(char * name, char * sig, char * desc)
{
	XPLMDebugString("Ivy: Startup.\n");
	strcpy(name, "Ivy, the nagging co-pilot");
	strcpy(sig, "xpsdk.plugin.ivy");
	strcpy(desc, "Tells you when not flying properly");

	if (sizeof(unsigned int) != 4 ||
		sizeof(unsigned short) != 2)
	{
		XPLMDebugString("Ivy: This plugin was compiled with a compiler with weird type sizes.\n");
		return 0;
	}

	// Do deferred sound initialization. See http://www.xsquawkbox.net/xpsdk/mediawiki/DeferredInitialization
	// for more info.
	XPLMRegisterFlightLoopCallback(InitPlugin, -1.0, NULL);

	

	return 1;
}

PLUGIN_API void XPluginStop(void)
{
	if (pIvySound)	delete pIvySound;
}

PLUGIN_API int XPluginEnable(void)
{
	
	return 1;
}

PLUGIN_API void XPluginDisable(void)
{
}

PLUGIN_API void XPluginReceiveMessage(XPLMPluginID from, int msg, void * p)
{
	switch (msg) {
	case XPLM_MSG_PLANE_LOADED:
		if (pIvySound)
		{
			XPLMDebugString("Ivy: Playing Sound.\n");
			// An example of actually playing the sound.  First we change to our 
			// context, then we play the sound at pitch, then we change the context back.
			// We check for null contexts both for us (our init failed) and the old context
			// (X-plane's sound failed).

			pIvySound->PlaySingleSound(my_sound, my_buffer);
			
		}
		break;
	}
}