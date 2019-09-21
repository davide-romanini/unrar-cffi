#include "unrarlib_ext.h"

void   PASCAL RARSetCallbackPtr(HANDLE hArcData,UNRARCALLBACKPtr Callback,void * UserData) {
     RARSetCallback(hArcData, (UNRARCALLBACK)Callback, (LPARAM)UserData);
}
