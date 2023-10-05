#include "../headers/matgraphergate.h"

matgraphergate::matgraphergate(int PORT, std::string SERVER, int MAXLINE){
    this->PORT_NUMBER = PORT;
    this->SERVER_ADDRESS = SERVER;
    this->MAXLINE_LENGTH = MAXLINE;
}

#ifdef OS_WINDOWS
int matgraphergate::sendCommand(const char* command){
    WSADATA ws;
    if (WSAStartup(MAKEWORD(2, 2), &ws) != 0)
    {
        std::cout<<"WSAStartup Failed! Error code: " << WSAGetLastError()<<std::endl;
        return 1;
    }

    int sockfd;
    //char buffer[this->MAXLINE_LENGTH];
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
#elif defined(OS_LINUX)
int matgraphergate::sendCommand(const char* command) {
    int sockfd;
    //char buffer[this->MAXLINE_LENGTH];
    struct sockaddr_in servaddr;

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd == -1) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(this->PORT_NUMBER);
    if (inet_pton(AF_INET, this->SERVER_ADDRESS.c_str(), &servaddr.sin_addr) <= 0) {
        perror("Invalid server address");
        exit(EXIT_FAILURE);
    }

    sendto(sockfd, command, strlen(command), 0, (struct sockaddr*)&servaddr, sizeof(servaddr));
    close(sockfd);

    return 0;
}
#endif


int matgraphergate::loadData(std::vector<double> arguments, std::vector<double> values, int length){
    this->sendCommand("load data");
    this->sendCommand("index 0");
    std::ostringstream var;
    std::cout<<"sending arguments: "<<std::endl;
    for(int i=0; i<length; i++){
        if((i*20)%length==0) std::cout<<((float)i/(float)length)*100.0<<"%"<<std::endl;
        this->sendCommand(std::to_string(arguments[i]).c_str());
    }
    this->sendCommand("index 1");
    std::cout<<"sending data: "<<std::endl;
    for(int i=0; i<length; i++){
        if((i*20)%length==0) std::cout<<((float)i/(float)length)*100.0<<"%"<<std::endl;
        this->sendCommand(std::to_string(values[i]).c_str());
    }
    this->sendCommand("end load data");
    return 0;
}

int matgraphergate::loadDataArgs(std::vector<double> arguments, std::vector<double> values, int length){
    this->sendCommand("load dataargs");
    std::cout<<"sending arguments and data: "<<std::endl;
    for(int i=0; i<length; i++){
        if((i*20)%length==0) std::cout<<((float)i/(float)length)*100.0<<"%"<<std::endl;
        this->sendCommand((std::to_string(arguments[i])+","+std::to_string(values[i])).c_str());
    }
    this->sendCommand("end load dataargs");
    return 0;
}

int matgraphergate::loadMulData(std::vector<std::vector<double>> arguments, std::vector<std::vector<double>> values){
    this->sendCommand("load muldata");
    std::cout<<"sending multiple arguments and data"<<std::endl;
    std::string commandline = "";
    std::vector<size_t> sizes;
    size_t maxsize = 0;
    for(int o=0; o<(int)values.size(); o++){
        std::cout<<"values: "<<o<<", size: "<<(int)values.at(o).size()<<std::endl;
    }
    for(size_t i=0; i<values.size(); i++){
        sizes.push_back((int)values.at(i).size());
        if(maxsize<values.at(i).size()){
            maxsize = values.at(i).size();
        }
    }
    sizes.push_back(0);//adding a dummy 0 not to break loop;
    for(size_t i=0; i<maxsize; i++){
        commandline="";
        if((i*20)%maxsize==0) std::cout<<((float)i/(float)maxsize)*100.0<<"%"<<std::endl;
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
    return 0;
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

int matgraphergate::setFilename(std::string filename){
    this->sendCommand("set filename");
    this->sendCommand(filename.c_str());
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

int matgraphergate::setAxisRange(double x_min, double y_min, double x_max, double y_max){
    std::stringstream xstring;
    std::stringstream ystring;
    xstring<<std::scientific<<x_min<<","<<x_max;
    ystring<<std::scientific<<y_min<<","<<y_max;
    std::string xstr = xstring.str();
    std::string ystr = ystring.str();
    this->sendCommand("set xlims");
    this->sendCommand(xstr.c_str());
    this->sendCommand("set ylims");
    this->sendCommand(ystr.c_str());
    return 0;
}

std::vector<std::string> matgraphergate::split_line(std::string line, char del){
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
    size_t linenum = 0;
    size_t end_indx = (last_index==0) ? 9999999999999 : last_index;
    std::vector<double> cur_line;
    if(file.is_open()){
        while(file && linenum<end_indx){
            cur_line.clear();
            std::getline(file, line);
            std::vector<std::string> ll =this->split_line(line, this->split_char);
            if(linenum>3&&(int)ll.size()>0){
                if(linenum==4) for(size_t i=0; i<ll.size(); i++) contents.push_back(cur_line);
                for(size_t i=0; i<ll.size(); i++) contents.at(i).push_back(std::stod(ll[i]));
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
