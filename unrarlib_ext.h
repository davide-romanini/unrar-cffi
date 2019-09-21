#include "raros.hpp"
#include "dll.hpp"

typedef int (CALLBACK *UNRARCALLBACKPtr)(UINT msg,void * UserData,LPARAM P1,LPARAM P2);
void   PASCAL RARSetCallbackPtr(HANDLE hArcData,UNRARCALLBACKPtr Callback,void * UserData);
