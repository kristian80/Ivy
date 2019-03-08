#pragma once
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <list>
#include <sys/stat.h>
#include <iostream>
#include <sstream>
#include <stdlib.h>
#include <time.h>
#include <vector>
#include <algorithm>
#include <queue>
#include <fstream>
#include <chrono>
#include <ctime>
#include <iomanip>
#include <set>

#include "XPLMDefs.h"
#include "XPLMProcessing.h"
#include "XPLMDisplay.h"
#include "XPLMGraphics.h"
#include "XPLMDataAccess.h"
#include "XPLMUtilities.h"
#include "XPLMNavigation.h"
#include "XPLMPlugin.h"
#include "XPLMMenus.h"
#include "XPWidgetDefs.h"
#include "XPWidgets.h"
#include "XPStandardWidgets.h"
#include "XPWidgetUtils.h"

#include "ImgWindow.h"
#include "imgui.h"

// OS X: we use this to convert our file path.
#if APL
#include <Carbon/Carbon.h>
#endif

// Your include paths for OpenAL may vary by platform.
#include "al.h"
#include "alc.h"

#include "XPSound.h"

#define IVY_MAX_AIRCRAFT_CONFIG 100

#define MAX_ERROR_HISTORY 100

#define MAX_GRAPH_DATA 1000
#define MAX_GRAPH_TIME 100



class MyIvy;
extern MyIvy * pIvy;
extern std::ofstream ivy_output_file;

inline bool file_exists(const std::string& name) 
{
	struct stat buffer;
	return (stat(name.c_str(), &buffer) == 0);
}

inline bool is_int(float f)
{
	if (f == ((int)f)) return true;
	return false;
}

inline void IvyDebugString(std::string output)
{
	ivy_output_file << output << std::endl;
	ivy_output_file.flush();
}


int WrapIvyVSpeedHandler(XPWidgetMessage  inMessage, XPWidgetID  inWidget, intptr_t inParam1, intptr_t inParam2);
int WrapIvyLogbookHandler(XPWidgetMessage  inMessage, XPWidgetID  inWidget, intptr_t  inParam1, intptr_t  inParam2);
int WrapIvyLogbookScrollHandler(XPWidgetMessage  inMessage, XPWidgetID  inWidget, intptr_t inParam1, intptr_t inParam2);


void WrapIvyDrawOutputWindow(XPLMWindowID in_window_id, void * in_refcon);
void WrapIvyMenuHandler(void * in_menu_ref, void * in_item_ref);
int WrapSayBaroCallback(XPLMCommandRef cmd, XPLMCommandPhase phase, void *refcon);
int WrapSayWindCallback(XPLMCommandRef cmd, XPLMCommandPhase phase, void *refcon);
int WrapAnnouncementCallback(XPLMCommandRef cmd, XPLMCommandPhase phase, void *refcon);
int WrapResetIvyCallback(XPLMCommandRef cmd, XPLMCommandPhase phase, void *refcon);
int WrapToogleWindowCallback(XPLMCommandRef cmd, XPLMCommandPhase phase, void *refcon);

void WrapKeyCallback(XPLMWindowID inWindowID, char inKey, XPLMKeyFlags inFlags, char inVirtualKey, void * inRefcon, int losingFocus);
int WrapMouseClickCallback(XPLMWindowID inWindowID, int x, int y, XPLMMouseStatus inMouse, void * inRefcon);

PLUGIN_API float WrapIvyFlightLoopCallback(float elapsedMe, float elapsedSim, int counter, void * refcon);