#include <iostream>
#include <string>
#include <sstream>
#include <iomanip>
#include <fstream>
#include <vector>
#include <filesystem>
#include <algorithm>
#include <string>
namespace fs = std::filesystem;
std::vector<std::string> split(const std::string &s, char delimiter)
{
    std::stringstream ss(s);
    std::string item;
    std::vector<std::string> tokens;
    int i = 0;
    while (getline(ss, item, delimiter))
    {
        tokens.push_back(item);
    }
    // std::cout << "Tokens size: " << tokens.size() << std::endl;
    return tokens;
}


int main(){




    std::string folderPath = "/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_position"; // Change this to your folder path
    // Iterate over each item in the directory
    // for (const auto &entry : fs::directory_iterator(folderPath))    {

        // if (entry.path().extension() == ".csv"){
            std::string entry= "/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_position/data_80005306 copy.csv-new";
            std::string line;
            std::ifstream inFile(entry);
            std::ofstream outFile(entry+ "-new-new");
            getline(inFile, line);
            outFile << line << std::endl;
            int header_count= split(line, ',').size();
            int i = 0;
            while (getline(inFile, line))
                {
                    std::vector<std::string> tokens = split(line, ',');
                    if (tokens.size() == header_count)
                    {
                        // std::cout << "Tokens size: " << tokens.size() << std::endl;
                        outFile << line << std::endl;
                    }else{
                        std::cout << "Tokens size: " << tokens.size() << std::endl;
                    }
                    // outFile << line << std::endl;
                    // i++;
                    // if (i>1000000){
                    //     break;
                    // }
                }
            outFile.close();
            inFile.close();

        // }
    // }

    return 0;
}