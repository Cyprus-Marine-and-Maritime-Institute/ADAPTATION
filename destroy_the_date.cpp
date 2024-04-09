#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <filesystem>
#include <sstream>
namespace fs = std::filesystem;



int count=0;
int total_count=0;
std::vector<std::string> data;

// Function to read a single CSV file and print its contents
void readCSV(const fs::path& file) {
    std::ifstream inFile(file);
    std::string line;
    std::string header="";
    if (header.empty()) {
        getline(inFile, header);
    }
    while (getline(inFile, line)) {
        // Process each line of the file
        std::istringstream tokenStream(line);
        int token_index=0;
            while (std::getline(tokenStream, line, ',')) {
                

                if (token_index==)
                tokens.push_back(token);
                token_index++;
            }
        data.push_back(line);
        count++;
    }
    inFile.close();
}

int main() {
    std::string folderPath = "/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_position/"; // Change this to your folder path

    // Iterate over each item in the directory
    for (const auto& entry : fs::directory_iterator(folderPath)) {
        if (entry.path().extension() == ".csv") {
            // If the entry is a CSV file, read it
            // std::cout << "Reading file: " << entry.path().filename() << std::endl;
            readCSV(entry.path());
            // break;
        }
    }

    return 0;
}
