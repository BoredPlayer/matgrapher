#include "matgraphergate.h"
#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>
#include <winsock2.h>

matgraphergate::matgraphergate(int PORT, std::string SERVER, int MAXLINE){
    this->PORT_NUMBER = PORT;
    this->SERVER_ADDRESS = SERVER;
    this->MAXLINE_LENGTH = MAXLINE;
}

int matgraphergate::sendCommand(const char* command){
    WSADATA ws;
    if (WSAStartup(MAKEWORD(2, 2), &ws) != 0)
    {
        std::cout<<"WSAStartup Failed! Error code: " << WSAGetLastError()<<std::endl;
        return 1;
    }

    int sockfd;
    char buffer[this->MAXLINE_LENGTH];
    struct sockaddr_in  servaddr;
    if((sockfd=socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == SOCKET_ERROR){
        perror("socket creation failed");
        exit(EXIT_FAILURE);
    }
    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(this->PORT_NUMBER);
    servaddr.sin_addr.s_addr = inet_addr(this->SERVER_ADDRESS.c_str());

    int n, len;

    sendto(sockfd, (const char*) command, strlen(command), 0, (const struct sockaddr *) &servaddr, sizeof(servaddr));
    closesocket(sockfd);
    return 0;
}

int matgraphergate::loadData(std::vector<double> arguments, std::vector<double> values, int length){
    this->sendCommand("load data");
    this->sendCommand("index 0");
    std::ostringstream var;
    std::cout<<"sending arguments: "<<std::endl;
    for(int i=0; i<length; i++){
        if((i*100)%length==0) std::cout<<((float)i/(float)length)*100.0<<"%"<<std::endl;
        this->sendCommand(std::to_string(arguments[i]).c_str());
    }
    this->sendCommand("index 1");
    std::cout<<"sending data: "<<std::endl;
    for(int i=0; i<length; i++){
        if((i*100)%length==0) std::cout<<((float)i/(float)length)*100.0<<"%"<<std::endl;
        this->sendCommand(std::to_string(values[i]).c_str());
    }
    this->sendCommand("end load data");
    return 0;
}

int matgraphergate::loadDataArgs(std::vector<double> arguments, std::vector<double> values, int length){
    this->sendCommand("load dataargs");
    std::cout<<"sending arguments and data: "<<std::endl;
    for(int i=0; i<length; i++){
        if((i*100)%length==0) std::cout<<((float)i/(float)length)*100.0<<"%"<<std::endl;
        this->sendCommand((std::to_string(arguments[i])+","+std::to_string(values[i])).c_str());
    }
    this->sendCommand("end load dataargs");
    return 0;
}

int matgraphergate::loadMulData(std::vector<std::vector<double>> arguments, std::vector<std::vector<double>> values){
    this->sendCommand("load muldata");
    std::cout<<"sending multiple arguments and data"<<std::endl;
    std::string commandline = "";
    std::vector<int> sizes;
    unsigned long int maxsize = 0;
    for(int o=0; o<(int)values.size(); o++){
        std::cout<<"values: "<<o<<", size: "<<(int)values.at(o).size()<<std::endl;
    }
    for(int i=0; i<values.size(); i++){
        sizes.push_back((int)values.at(i).size());
        if(maxsize<values.at(i).size()){
            maxsize = values.at(i).size();
        }
    }
    sizes.push_back(0);//adding a dummy 0 not to break loop;
    for(int i=0; i<maxsize; i++){
        commandline="";
        if((i*100)%maxsize==0) std::cout<<((float)i/(float)maxsize)*100.0<<"%"<<std::endl;
        for(int o=0; o<(int)values.size(); o++){
            if(i<sizes.at(o)){
                commandline += std::to_string(arguments.at(o).at(i));
                commandline += ",";
                commandline += std::to_string(values.at(o).at(i));
                if(o<(int)values.size()-1 && i<sizes.at(o+1)) commandline+=",";
            }
        }
        this->sendCommand(commandline.c_str());
    }
    this->sendCommand("end load muldata");
}

int matgraphergate::loadLabels(std::vector<std::string> labels, int length){
    this->sendCommand("load labels");
    for(int i=0; i<length; i++){
        this->sendCommand(labels[i].c_str());
    }
    this->sendCommand("end load labels");
    return 0;
}

int matgraphergate::setTitle(std::string title){
    this->sendCommand("set title");
    this->sendCommand(title.c_str());
    return 0;
}

int matgraphergate::setExportMethod(int method){
    // 0 - save, 1 - show, 2 - show & save
    this->sendCommand("set exportmethod");
    this->sendCommand(std::to_string(method).c_str());
    return 0;
}

int matgraphergate::setAxisNames(std::string x_axis, std::string y_axis){
    this->sendCommand("set axisnames");
    this->sendCommand((x_axis+","+y_axis).c_str());
    return 0;
}

std::vector<std::string> matgraphergate::split_line(std::string line, char del){
    int beg = 0;
    std::vector<std::string> output_vec;
    std::string line_buffer = "";
    for(int i=0; i<(int)line.size(); i++){
        if((char)line[i]!=del && i<(int)line.size()-1){
            line_buffer+=line[i];
        }
        else{
            if(i==(int)line.size()-1) line_buffer+=line[i];
            output_vec.push_back(line_buffer);
            line_buffer = "";
        }
    }
    return output_vec;
}

int matgraphergate::readFile(std::string filename, std::vector<std::vector<double>> &contents, unsigned long int last_index){
    std::ifstream file;
    file.open(filename.c_str());
    std::string line;
    unsigned long int linenum = 0;
    unsigned long int end_indx = (last_index==0) ? 9999999999999 : last_index;
    std::vector<double> cur_line;
    if(file.is_open()){
        while(file && linenum<end_indx){
            cur_line.clear();
            std::getline(file, line);
            std::vector<std::string> ll =this->split_line(line, this->split_char);
            if(linenum>3&&(int)ll.size()>0){
                if(linenum==4) for(int i=0; i<ll.size(); i++) contents.push_back(cur_line);
                for(int i=0; i<ll.size(); i++) contents.at(i).push_back(std::stod(ll[i]));
            }
            linenum++;
        }
    }
    file.close();
    return 0;
}

matgraphergate::~matgraphergate()
{
    //dtor
}
