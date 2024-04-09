#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <filesystem>
#include <sstream>
#include <algorithm>
#include "ShipStaticDataRow.h"
namespace fs = std::filesystem;

std::string header = "";
int count = 0;
int total_count = 0;
std::vector<std::string> data;
std::vector<std::string> split_date(const std::string &s, char delimiter)
{
    std::stringstream ss(s);
    std::string item;
    std::vector<std::string> tokens;
    int i = 0;
    while (getline(ss, item, delimiter))
    {
        tokens.push_back(item);
    }
    if (tokens[0].empty())
    {
        tokens.erase(tokens.begin());
    }
    // std::cout << "Tokens size: " << tokens.size() << std::endl;
    return tokens;
}
std::vector<std::string> split(const std::string& s, char delimiter = ',') {
    std::vector<std::string> tokens;
    std::string token;
    std::istringstream tokenStream(s);
    bool insideQuotes = false;

    while (tokenStream) {
        char nextChar = tokenStream.get();
        if (nextChar == '"') {
            insideQuotes = !insideQuotes;  // Toggle the state of being inside quotes
        } else if (nextChar == delimiter && !insideQuotes) {
            tokens.push_back(token);
            token.clear();
        } else if (nextChar != EOF) {
            token += nextChar;
        }
    }

    // Adding the last token to the vector (if not empty)
    // if (!token.empty()) {
        tokens.push_back(token);
    // }
    if (tokens[0] != "ShipStaticData"){
        tokens.erase(tokens.begin());
    }
    return tokens;
}


std::string getUntil(const std::string &s, char delimiter)
{
    std::vector<std::string> tokens = split_date(s, delimiter);
    return tokens[0];
}
// Function to read a single CSV file and print its contents
void readCSV(const fs::path &file)
{
    std::ifstream inFile(file);
    std::string line;
    std::stringstream ss;
    ShipStaticDataRow row;
    int file_line = 0;
    int count_commas = 0;
    if (header.empty()){
        getline(inFile, header);
        header = "MessageType,AisVersion,CallSign,Destination,DimensionA,DimensionB,DimensionC,DimensionD,Dte,EtaDay,EtaHour,EtaMinute,EtaMonth,FixType,ImoNumber,MaximumStaticDraught,RepeatIndicator,Spare,ShipType,Valid,MMSI,ShipName,TimeUtc";
    }
    else{
        getline(inFile, line);
        // std::cout << "Header: " << line << std::endl; 
        count_commas= split(line, ',').size();
    }
    // std::cout << "Count commas: " << count_commas << std::endl;
    // std::cout << "Second line: " << std::count(line.begin(),line.end(),',') << std::endl;
    // return;
    if (count_commas == 29){
        while (getline(inFile, line)){
            try{
            std::vector<std::string> tokens = split(line, ',');

            // std::cout << "Tokens size: " << tokens.size() << std::endl;
            // std::cout << "Tokens: " << line << std::endl;
            if (tokens.size() != 29){
                std::ofstream outFile("/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_static/error.log", std::ios::app);
                outFile << "Error: " << file << std::endl;
                outFile << "Error: " << line << std::endl;
                outFile.close();
                std::cout << "Error: " << file << std::endl; 
                std::cout << "Error: " << tokens.size() << std::endl;   
                continue;
            }
            row.setMessageType(tokens[0]);
            row.setAisVersion(tokens[1]);
            row.setCallSign(tokens[2]);
            row.setDestination(tokens[3]);
            row.setDimensionA(tokens[4]);
            row.setDimensionB(tokens[5]);
            row.setDimensionC(tokens[6]);
            row.setDimensionD(tokens[7]);
            row.setDte(tokens[8]);
            row.setEtaDay(tokens[9]);
            row.setEtaHour(tokens[10]);
            row.setEtaMinute(tokens[11]);
            row.setEtaMonth(tokens[12]);
            row.setFixType(tokens[13]);
            row.setImoNumber(tokens[14]);
            row.setMaximumStaticDraught(tokens[15]);
            row.setRepeatIndicator(tokens[18]);
            row.setSpare(tokens[19]);
            row.setShipType(tokens[20]);
            row.setValid(tokens[22]);
            row.setMMSI(tokens[23]);
            row.setShipName(tokens[25]);
            row.setTimeUtc(tokens[28]);
            // std::cout << line << std::endl;
            // for (auto token : tokens){
            //     std::cout << token << ",";
            // }
            // std::cout << std::endl;


            // std::cout << "TimeUtc: " << row.getTimeUtc() << std::endl;
            row.setTimeUtc(getUntil(row.getTimeUtc(), '.'));

            data.push_back(row.getRowString());
            count++;
            file_line++;
            }
            catch(const std::exception& e){
                std::ofstream outFile("/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_static/error.log", std::ios::app);
                outFile << "Error: " << file << std::endl;
                outFile << "Error: " << e.what() << std::endl;
                outFile << "Error: " << line << std::endl;
                outFile.close();
            }
            // std::fstream outFile("/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_static/data_compare.csv", std::ios::app);
            // outFile << "MessageType,AisVersion,CallSign,Destination,DimensionA,DimensionB,DimensionC,DimensionD,Dte,EtaDay,EtaHour,EtaMinute,EtaMonth,FixType,ImoNumber,MaximumStaticDraught,RepeatIndicator,Spare,ShipType,Valid,MMSI,ShipName,TimeUtc" << std::endl;
            // outFile << row.getRowString() << std::endl;
            // outFile << header << std::endl;
            // outFile << line << std::endl;
            // outFile.close();
        }
        }else if (count_commas == 30){
            while (getline(inFile, line)){
                try{
                std::vector<std::string> tokens = split(line, ',');
                // std::cout << "Tokens size: " << tokens.size() << std::endl;
                // std::cout << "Tokens: " << line << std::endl;
                // std::string tokens_name[] ={"MessageType","AisVersion","CallSign","Destination","DimensionA","DimensionB","DimensionC","DimensionD","Dte","EtaDay","EtaHour","EtaMinute","EtaMonth","FixType","ImoNumber","MaximumStaticDraught","RepeatIndicator","Spare","ShipType","Valid","MMSI","ShipName","TimeUtc"};
                // for (int i = 0; i < tokens.size(); i++){
                //     std::cout << i << ": "<<tokens[i] << std::endl;
                // }
                // std::cout << std::endl;
                if (tokens.size() != 31){
                std::ofstream outFile("/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_static/error.log", std::ios::app);
                outFile << "Error: " << file << std::endl;
                outFile << "Error: " << line << std::endl;

                outFile.close();
                continue; 
            }
                row.setMessageType(tokens[0]);
                row.setAisVersion(tokens[1]);
                row.setCallSign(tokens[2]);
                row.setDestination(tokens[3]);
                row.setDimensionA(tokens[4]);
                row.setDimensionB(tokens[5]);
                row.setDimensionC(tokens[6]);
                row.setDimensionD(tokens[7]);
                row.setDte(tokens[8]);
                row.setEtaDay(tokens[9]);
                row.setEtaHour(tokens[10]);
                row.setEtaMinute(tokens[11]);
                row.setEtaMonth(tokens[12]);
                row.setFixType(tokens[13]);
                row.setImoNumber(tokens[14]);
                row.setMaximumStaticDraught(tokens[15]);
                row.setRepeatIndicator(tokens[18]);
                row.setSpare(tokens[19]);
                row.setShipType(tokens[20]);
                row.setValid(tokens[22]);
                row.setMMSI(tokens[23]);
                row.setShipName(tokens[25]);
                row.setTimeUtc(tokens[28]);
                // std::cout << "TimeUtc: " << tokens[28] << std::endl;
                // std::cout << "TimeUtc: " << row.getTimeUtc() << std::endl;
                row.setTimeUtc(getUntil(row.getTimeUtc(), '.'));

                //for (auto token : tokens){
                //     std::cout << token << ",";
                // }
                // std::cout << std::endl;
                // std::cout << line << std::endl;


                data.push_back(row.getRowString());
                count++;

                            }
            catch(const std::exception& e){
                std::ofstream outFile("/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_static/error.log", std::ios::app);
                outFile << "Error: " << file << std::endl;
                outFile << "Error: " << e.what() << std::endl;
                outFile << "Error: " << line << std::endl;
                outFile.close();
            }
                // std::fstream outFile("/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_static/data_compare.csv", std::ios::app);
                // outFile << "MessageType,AisVersion,CallSign,Destination,DimensionA,DimensionB,DimensionC,DimensionD,Dte,EtaDay,EtaHour,EtaMinute,EtaMonth,FixType,ImoNumber,MaximumStaticDraught,RepeatIndicator,Spare,ShipType,Valid,MMSI,ShipName,TimeUtc" << std::endl;
                // outFile << row.getRowString() << std::endl;
                // outFile << header << std::endl;
                // outFile << line << std::endl;
                // outFile.close();
            }
        }else{
            std::cout << "Error: " << file << std::endl;
            std::cout << "Count commas: " << count_commas << std::endl;
        }
    if (count > 20000000)
    {
        total_count += count;
        std::cout << "Writing file: " << total_count << std::endl;
        std::ofstream outFile("/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_static/data_" + std::to_string(total_count) + ".csv");
        outFile << header << std::endl;
        for (auto line : data){
            outFile << line << std::endl;
        }
        outFile.close();
        data.clear();
        count = 0;
    }

    inFile.close();
}

int main()
{
    std::string folderPath = "/srv/sharedfolder/dataCSV/ShipStaticData"; // Change this to your folder path
    // std::string folderPath = "/srv/sharedfolder/MostData/dataCSV_added/ShipStaticDatas"; // Change this to your folder path
    // std::string folderPath = "/srv/sharedfolder/MostData/dataCSV/ShipStaticDatas"; // Change this to your folder path
    // Iterate over each item in the directory

    for (const auto &entry : fs::directory_iterator(folderPath))
    {
        if (entry.path().extension() == ".csv")
        {
            // If the entry is a CSV file, read it
            // std::cout << "Reading file: " << entry.path().filename() << std::endl;
            readCSV(entry.path());
            // break;
        }
    }

    if (count > 0){
        total_count += count;
        std::cout << "Writing file: " << total_count << std::endl;
        std::ofstream outFile("/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_static/data_" + std::to_string(total_count) + ".csv");
        outFile << header << std::endl;
        for (auto line : data)
        {
            outFile << line << std::endl;
        }
        outFile.close();
        data.clear();
        count = 0;
    }

    return 0;
}
