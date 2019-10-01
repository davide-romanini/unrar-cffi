#include "raros.hpp"
#ifdef _WIN_ALL
#include <windows.h>
#endif // _WIN_ALL
#include "unrarlib_ext.h"

void   PASCAL RARSetCallbackPtr(HANDLE hArcData,UNRARCALLBACKPtr Callback,void * UserData) {
     RARSetCallback(hArcData, (UNRARCALLBACK)Callback, (LPARAM)UserData);
}
