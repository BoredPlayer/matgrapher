#ifndef MATGRAPHERGATE_H
#define MATGRAPHERGATE_H

#ifdef _WIN32
#define OS_WINDOWS
#elif __linux__
#define OS_LINUX
#else
#error "Unsupported operating system"
#endif

#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>
#ifdef OS_WINDOWS
#include <winsock2.h>
#elif defined(OS_LINUX)
#include <cstring>
#include <cstdlib>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#endif

class matgraphergate
{
    public:
        /** Default constructor */
        matgraphergate(int PORT, std::string SERVER, int MAXLINE);
        /** Default destructor */
        virtual ~matgraphergate();

        int readFile(std::string filename, std::vector<std::vector<double>> &contents, unsigned long int last_index);
        std::vector<std::string> split_line(std::string line, char del);
        int setAxisNames(std::string x_axis, std::string y_axis);
        int setExportMethod(int method);
        int setTitle(std::string title);
        int setFilename(std::string filename);
        int setAxisRange(double x_min, double y_min, double x_max, double y_max);
        int loadLabels(std::vector<std::string> labels, int length);
        int loadMulData(std::vector<std::vector<double>> arguments, std::vector<std::vector<double>> values);
        int loadDataArgs(std::vector<double> arguments, std::vector<double> values, int length);
        int loadData(std::vector<double> arguments, std::vector<double> values, int length);
        int sendCommand(const char* command);
		
		char split_char = ' ';

    protected:

    private:
        int PORT_NUMBER;
        std::string SERVER_ADDRESS;
        int MAXLINE_LENGTH;
};

#endif // MATGRAPHERGATE_H
