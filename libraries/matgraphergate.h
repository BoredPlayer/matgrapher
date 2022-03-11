#ifndef MATGRAPHERGATE_H
#define MATGRAPHERGATE_H

#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>
#include <winsock2.h>

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
