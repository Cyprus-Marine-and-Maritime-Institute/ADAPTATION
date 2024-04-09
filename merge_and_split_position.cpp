#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <filesystem>
#include <sstream>
#include <algorithm>
#include "PositionReportRow.h"
namespace fs = std::filesystem;

std::string header = "";
int count = 0;
int total_count = 0;
std::vector<std::string> data;

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
    if (tokens[0].empty())
    {
        tokens.erase(tokens.begin());
    }
    // std::cout << "Tokens size: " << tokens.size() << std::endl;
    return tokens;
}

std::string getUntil(const std::string &s, char delimiter)
{
    std::vector<std::string> tokens = split(s, delimiter);
    return tokens[0];
}
// Function to read a single CSV file and print its contents
void readCSV(const fs::path &file)
{
    std::ifstream inFile(file);
    std::string line;
    std::stringstream ss;
    PositionReportRow row;
    if (header.empty())
    {
        getline(inFile, header);
    }
    else
    {
        getline(inFile, line);
    }
    int count_commas = std::count(header.begin(), header.end(), ',');

    if (count_commas == 25)
    {

        while (getline(inFile, line))
        {
            std::vector<std::string> tokens = split(line, ',');

            row.setMessageType(tokens[0]);
            row.setCog(tokens[1]);
            row.setCommunicationState(tokens[2]);
            row.setLatitude(tokens[3]);
            row.setLongitude(tokens[4]);
            row.setMessageID(tokens[5]);
            row.setNavigationalStatus(tokens[6]);
            row.setPositionAccuracy(tokens[7]);
            row.setRaim(tokens[8]);
            row.setRateOfTurn(tokens[9]);
            row.setRepeatIndicator(tokens[10]);
            row.setSog(tokens[11]);
            row.setSpare(tokens[12]);
            row.setSpecialManoeuvreIndicator(tokens[13]);
            row.setTimestamp(tokens[14]);
            row.setTrueHeading(tokens[15]);
            row.setValid(tokens[17]);
            row.setMMSI(tokens[18]);
            row.setShipName(tokens[20]);
            row.setTimeUtc(tokens[23]);

            row.setTimeUtc(getUntil(row.getTimeUtc(), '.'));
            data.push_back(row.getRowString());
            count++;
            // std::fstream outFile("/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_position/data_compare.csv", std::ios::app);
            // outFile << "MessageType,Cog,CommunicationState,Latitude,Longitude,MessageID,NavigationalStatus,PositionAccuracy,Raim,RateOfTurn,RepeatIndicator,Sog,Spare,SpecialManoeuvreIndicator,Timestamp,TrueHeading,Valid,MMSI,ShipName,TimeUtc" << std::endl;
            // outFile << row.getRowString() << std::endl;
            // outFile << header << std::endl;
            // outFile << line << std::endl;
            // outFile.close();
        }
    }else{
        while (getline(inFile, line))
        {
            std::vector<std::string> tokens = split(line, ',');
            row.setMessageType(tokens[1]);
            row.setCog(tokens[2]);
            row.setCommunicationState(tokens[3]);
            row.setLatitude(tokens[4]);
            row.setLongitude(tokens[5]);
            row.setMessageID(tokens[6]);
            row.setNavigationalStatus(tokens[7]);
            row.setPositionAccuracy(tokens[8]);
            row.setRaim(tokens[9]);
            row.setRateOfTurn(tokens[10]);
            row.setRepeatIndicator(tokens[11]);
            row.setSog(tokens[12]);
            row.setSpare(tokens[13]);
            row.setSpecialManoeuvreIndicator(tokens[14]);
            row.setTimestamp(tokens[15]);
            row.setTrueHeading(tokens[16]);
            row.setValid(tokens[18]);
            row.setMMSI(tokens[19]);
            row.setShipName(tokens[21]);
            row.setTimeUtc(tokens[24]);

            row.setTimeUtc(getUntil(row.getTimeUtc(), '.'));
            data.push_back(row.getRowString());
            count++;
            // std::fstream outFile("/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_position/data_compare.csv", std::ios::app);
            // outFile << "MessageType,Cog,CommunicationState,Latitude,Longitude,MessageID,NavigationalStatus,PositionAccuracy,Raim,RateOfTurn,RepeatIndicator,Sog,Spare,SpecialManoeuvreIndicator,Timestamp,TrueHeading,Valid,MMSI,ShipName,TimeUtc" << std::endl;
            // outFile << row.getRowString() << std::endl;
            // outFile << header << std::endl;
            // outFile << line << std::endl;
            // outFile.close();
        }
    }

    if (count > 20000000)
    {
        total_count += count;
        std::cout << "Writing file: " << total_count << std::endl;
        std::ofstream outFile("/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_position/data_" + std::to_string(total_count) + ".csv");
        outFile << "MessageType,Cog,CommunicationState,Latitude,Longitude,MessageID,NavigationalStatus,PositionAccuracy,Raim,RateOfTurn,RepeatIndicator,Sog,Spare,SpecialManoeuvreIndicator,Timestamp,TrueHeading,Valid,MMSI,ShipName,TimeUtc" << std::endl;
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
    // std::string folderPath = "/srv/sharedfolder/MostData/dataCSV/PositionReports"; // Change this to your folder path
    // std::string folderPath = "/srv/sharedfolder/MostData/dataCSV_added/PositionReports"; // Change this to your folder path
    std::string folderPath = "/srv/sharedfolder/dataCSV/PositionReport"; // Change this to your folder path
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
    if (count > 0)
    {
        total_count += count;
        std::cout << "Writing file: " << total_count << std::endl;
        std::ofstream outFile("/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_position/data_" + std::to_string(total_count) + ".csv");
        outFile << "MessageType,Cog,CommunicationState,Latitude,Longitude,MessageID,NavigationalStatus,PositionAccuracy,Raim,RateOfTurn,RepeatIndicator,Sog,Spare,SpecialManoeuvreIndicator,Timestamp,TrueHeading,Valid,MMSI,ShipName,TimeUtc" << std::endl;
        for (auto line : data){
            outFile << line << std::endl;
        }
        outFile.close();
        data.clear();
        count = 0;
    }

    return 0;
}
