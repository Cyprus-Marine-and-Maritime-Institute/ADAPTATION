#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <filesystem>
#include <sstream>
#include <algorithm>
#include "PositionReportRow.h"
#include <map>
#include <cmath>
namespace fs = std::filesystem;
const double EarthRadiusKm = 6371.0;
std::string header = "";
int count = 0;
int total_count = 0;
std::vector<std::string> data;
// Define a simple structure for a point
struct Point
{
    double latitude;
    double longitude;
};

// Define a polygon as a vector of points
using Polygon = std::vector<Point>;
Point polygonCentroid(const Polygon &polygon)
{
    Point centroid = {0, 0};
    double signedArea = 0.0;
    double x0 = 0.0; // Current vertex X
    double y0 = 0.0; // Current vertex Y
    double x1 = 0.0; // Next vertex X
    double y1 = 0.0; // Next vertex Y
    double a = 0.0;  // Partial signed area

    // For all vertices except last
    int n = polygon.size();
    for (int i = 0; i < n; ++i)
    {
        x0 = polygon[i].latitude;
        y0 = polygon[i].longitude;
        x1 = polygon[(i + 1) % n].latitude;
        y1 = polygon[(i + 1) % n].longitude;
        a = x0 * y1 - x1 * y0;
        signedArea += a;
        centroid.latitude += (x0 + x1) * a;
        centroid.longitude += (y0 + y1) * a;
    }

    signedArea *= 0.5;
    centroid.latitude /= (6.0 * signedArea);
    centroid.longitude /= (6.0 * signedArea);

    return centroid;
}

// Function to parse a single point from a string, e.g., "[36.184613, -5.456758]"
Point parsePoint(const std::string &pointStr)
{
    if (pointStr.length() < 3)
        return Point{0, 0};
    std::stringstream ss(pointStr.substr(2, pointStr.size() - 3)); // Remove '[' and ']'
    std::string lat, lon;
    getline(ss, lat, ',');
    getline(ss, lon);
    // std::cout << "Lat: " << lat << " Lon: " << lon << std::endl;
    return Point{std::stod(lat), std::stod(lon)};
}

// Function to parse a polygon from a string, e.g., "[[36.184613, -5.456758], ...]"
Polygon parsePolygon(const std::string &polygonStr)
{
    Polygon polygon;
    std::stringstream ss(polygonStr.substr(1, polygonStr.size() - 2)); // Remove '[' and ']'
    std::string pointStr;
    while (getline(ss, pointStr, ']'))
    {
        if (pointStr[0] == ',')
            pointStr = pointStr.substr(2);             // Remove ", " from the beginning
        polygon.push_back(parsePoint(pointStr + ']')); // Add ']' back for parsing
        if (ss.peek() == ',')
            ss.ignore(); // Ignore ',' between points
    }
    return polygon;
}
bool isPointInPolygon(const Point &point, const Polygon &polygon)
{
    bool inside = false;
    for (size_t i = 0, j = polygon.size() - 1; i < polygon.size(); j = i++)
    {
        if (((polygon[i].longitude > point.longitude) != (polygon[j].longitude > point.longitude)) &&
            (point.latitude < (polygon[j].latitude - polygon[i].latitude) * (point.longitude - polygon[i].longitude) /
                                      (polygon[j].longitude - polygon[i].longitude) +
                                  polygon[i].latitude))
        {
            inside = !inside;
        }
    }
    return inside;
}
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
// Convert degrees to radians
double degToRad(double degree){
    return degree * M_PI / 180.0;
}

// Haversine formula to calculate distance between two points given in geographic coordinates
double haversineDistance(const Point &p1, const Point &p2){
    double latRad1 = degToRad(p1.latitude);
    double latRad2 = degToRad(p2.latitude);
    double diffLat = degToRad(p2.latitude - p1.latitude);
    double diffLon = degToRad(p2.longitude - p1.longitude);

    double a = sin(diffLat / 2) * sin(diffLat / 2) +
               cos(latRad1) * cos(latRad2) *
                   sin(diffLon / 2) * sin(diffLon / 2);
    double c = 2 * atan2(sqrt(a), sqrt(1 - a));

    return EarthRadiusKm * c; // Distance in kilometers
}
void saveTheMap(std::map<std::string, std::vector<PositionReportRow>> polygons_map,std::string month,std::string year){
    // for each key in the map
    for (const auto &pair : polygons_map){
        // check if directory exists
        if (!fs::exists("/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_position_by_month_by_port/"+year+"/"+month)){
            if (!fs::exists("/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_position_by_month_by_port/"+year)){
                if (!fs::exists("/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_position_by_month_by_port")){
                    fs::create_directory("/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_position_by_month_by_port");
                }
                fs::create_directory("/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_position_by_month_by_port/"+year);
            }
            fs::create_directory("/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_position_by_month_by_port/"+year+"/"+month);
        }
        std::fstream outFile("/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_position_by_month_by_port/"+year+"/"+month+"/" + pair.first + ".csv", std::ios::app);
        // if file doesn't exists write the header
        if (outFile.tellp() == 0){
            outFile << "MessageType,Cog,CommunicationState,Latitude,Longitude,MessageID,NavigationalStatus,PositionAccuracy,Raim,RateOfTurn,RepeatIndicator,Sog,Spare,SpecialManoeuvreIndicator,Timestamp,TrueHeading,Valid,MMSI,ShipName,TimeUtc,Tags" << std::endl;
        }
        for (auto polygons : pair.second){
            outFile << polygons.getRowStringWithTags() << std::endl;
        }
        outFile.close();
    }
}

std::map<std::string,std::vector<PositionReportRow>> assignThePort(std::vector<PositionReportRow> datapoints,
                   std::map<std::string, Point> centeroids,
                   std::map<std::string, Polygon> polygons){
    std::map<std::string,std::vector<PositionReportRow>> polygons_map;
    int inside_count = 0;
    for (PositionReportRow datapoint : datapoints){
        const std::string Latitude = datapoint.getLatitude();
        const auto Longitude = datapoint.getLongitude();
        Point point{std::stod(Latitude), std::stod(Longitude)};
        std::map<std::string, double> distances;
        for (const auto &pair : polygons){
            if (isPointInPolygon(point, pair.second)){
                // std::cout << "Point is inside " << pair.first << " the polygon" << std::endl;
                inside_count++;
                // datapoint.setTags(pair.first);
                // std::cout << "Point is "  << (isPointInPolygon(point, pair.second) ? "inside " : "outside ")<< pair.first << " the polygon" << std::endl;
            }
            distances[pair.first] = haversineDistance(point, centeroids[pair.first]);
        }
        std::map<std::string, int> counts;
        // get the minimum distance
        auto min = std::min_element(distances.begin(), distances.end(), [](const auto &l, const auto &r)
                                    { return l.second < r.second; });
        if (min != distances.end()){
            // std::cout << "Min distance: " << min->second << " Port: " << min->first << std::endl;
            datapoint.setTags(min->first);
            polygons_map[min->first].push_back(datapoint);
            // check if the port is already in the map
            if (counts.find(min->first) == counts.end()){
                counts[min->first] = 1;
            }
            else{
                counts[min->first]++;
            }
        }
    }
    return polygons_map;
}
// Function to read a single CSV file and print its contents
std::vector<PositionReportRow> readCSV(const fs::path &file,
                                         std::map<std::string, Point> centeroids,
                                          std::map<std::string, Polygon> polygons,
                                          std::string month,
                                          std::string year
                                          ){
    std::cout << "Reading file: " << file << std::endl;
    std::ifstream inFile(file);
    std::string line;
    std::stringstream ss;
    PositionReportRow row;
    std::vector<PositionReportRow> position_reports;
    if (header.empty()){
        getline(inFile, header);
    }
    else{
        getline(inFile, line);
    }
    int count_commas = std::count(header.begin(), header.end(), ',');
    std::cout << "Count commas: " << count_commas << std::endl;
    int total_count = 0;
    if (count_commas == 21 || count_commas == 19){
        while (getline(inFile, line)){
            if (position_reports.size() % 2000000 == 0){
                std::cout << "Count: " << position_reports.size() << std::endl;
            }
            std::vector<std::string> tokens = split(line, ',');
            // std::cout << "Line: " << line << std::endl;
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
            row.setValid(tokens[16]);
            row.setMMSI(tokens[17]);
            tokens[18].erase(std::remove(tokens[18].begin(), tokens[18].end(), ' '), tokens[18].end());
            row.setShipName(tokens[18]);
            row.setTimeUtc(tokens[19]);
            row.setTimeUtc(getUntil(row.getTimeUtc(), '.'));
            // data.push_back(row.getRowString());
            // count++;
            position_reports.push_back(row);
            // get the current line pointer and save it so I can seek to it later
            // std::streampos current_pos = inFile.tellg();
            // std::cout << "Current pos: " << current_pos << std::endl;
            if (position_reports.size() == 2000000){
                auto polygon_maps=assignThePort(position_reports, centeroids, polygons);
                saveTheMap(polygon_maps,month,year);
                position_reports.clear();
            }
        }
    }

    inFile.close();

    return position_reports;
}




int main(){
    std::string year = "2024";
    std::string month = "3";
    std::string folderPath = "/home/charalambos/Documents/Projects/ADAPTATION/grouped_data_position_by_month/"+year+"/"+month+".csv"; // Change this to your folder path
    // std::string folderPath = "/home/charalambos/Documents/Projects/ADAPTATION/subset_test/data_0_200000.csv";
    // string folder path to actual path
    auto path = fs::path(folderPath);
    std::map<std::string, Point> centeroids;
    std::map<std::string, std::vector<PositionReportRow>> polygons_map;

    std::cout << "Path: " << path << std::endl;
    std::ifstream file("port_coords.csv");
    std::string line;
    // map to store the polygons
    std::map<std::string, Polygon> polygons;
    getline(file, line);
    while (getline(file, line)){
        std::stringstream linestream(line);
        std::string port, coordsStr;
        getline(linestream, port, ',');
        getline(linestream, coordsStr);

        Polygon polygon = parsePolygon(coordsStr);
        polygons[port] = polygon;
        centeroids[port] = polygonCentroid(polygon);
        // For demonstration, print out the first point of each polygon
        if (!polygon.empty()){
            std::cout << "First point of " << port << ": (" << polygon[0].latitude << ", " << polygon[0].longitude << ")" << std::endl;
        }
    }
    std::cout << "Polygons size: " << polygons.size() << std::endl;
    const std::vector<PositionReportRow> datapoints = readCSV(path, centeroids, polygons,month,year);
    return 0;
}
