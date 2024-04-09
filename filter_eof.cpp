#include <fstream>
#include <iostream>
#include <filesystem>
#include <sstream>
#include <algorithm>
#include "ShipStaticDataRow.h"
namespace fs = std::filesystem;

int main(){

    std::string folderPath = "/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_position"; // Change this to your folder path
    // Iterate over each item in the directory
    for (const auto &entry : fs::directory_iterator(folderPath)){
        if (entry.path().extension() == ".csv"){
            std::ifstream inFile(entry.path(), std::ios::binary);   // Open in binary mode to read EOF character
            // new file path = entry.path()+'_revised'
            std::string new_file_path = entry.path().string() + "_revised";
            std::ofstream outFile(new_file_path, std::ios::binary); // Open in binary mode to write

            if (!inFile.is_open() || !outFile.is_open()){
                std::cerr << "Could not open file(s)." << std::endl;
                return 1;
            }

            char ch;
            while (inFile.get(ch)){ // Read character by character
                if (ch != '\x1A'){// Assuming '\x1A' is the EOF character you want to exclude
                    outFile.put(ch); // Write the character if it's not EOF character
                }
            }

            inFile.close();
            outFile.close();

            std::cout << "File processed successfully." << std::endl;
        }
    }

    return 0;
}
