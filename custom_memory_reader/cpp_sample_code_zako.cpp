#include <iostream>
#include <string.h>
#ifdef _WIN32
    #include <windows.h>
#else
    #include <unistd.h>
#endif // _WIN32

using namespace std;

void sleepcp(int milliseconds);

void sleepcp(int milliseconds) // Cross-platform sleep function
{
    #ifdef _WIN32
        Sleep(milliseconds);
    #else
        usleep(milliseconds * 1000);
    #endif // _WIN32
}
int main()
{   
    string hdstr="Apachti main framinco alpha 123";
    cout << "Hi! At the count to 3, I'll die! :)" << endl;
    string s1;
    sleepcp(3000);
    
    cout<<"Input s: ";
    cin>>s1;
    while(true){
        sleepcp(3000);
        cout<<s1<<endl;
    }
    return 0;
}
