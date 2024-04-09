
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <chrono>
#include <any>
#include <bitset>
#include <ctime>
#include <iomanip>
#include <sstream>
class PositionReportRow{
    public:
        PositionReportRow();
        ~PositionReportRow();
        std::stringstream print();
        std::string getRowString();
        std::string getRowStringWithTags();
        // Setters
        void setMessageType(std::string MessageType);
        void setCog(std::string Cog);
        void setCommunicationState(std::string CommunicationState);
        void setLatitude(std::string Latitude);
        void setLongitude(std::string Longitude);
        void setMessageID(std::string MessageID);
        void setNavigationalStatus(std::string NavigationalStatus);
        void setPositionAccuracy(std::string PositionAccuracy);
        void setRaim(std::string Raim);
        void setRateOfTurn(std::string RateOfTurn);
        void setRepeatIndicator(std::string RepeatIndicator);
        void setSog(std::string Sog);
        void setSpare(std::string Spare);
        void setSpecialManoeuvreIndicator(std::string SpecialManoeuvreIndicator);
        void setTimestamp(std::string Timestamp);
        void setTrueHeading(std::string TrueHeading);
        void setValid(std::string Valid);
        void setMMSI(std::string MMSI);
        void setShipName(std::string ShipName);
        void setTimeUtc(std::string TimeUtc);
        void setTags(std::string tags);
        void setGeohash(std::string Geohash);
        // Getters
        std::string getMessageType();
        std::string getCog();
        std::string getCommunicationState();
        std::string getLatitude() const;
        std::string getLongitude() const;
        std::string getMessageID();
        std::string getNavigationalStatus();
        std::string getPositionAccuracy();
        std::string getRaim();
        std::string getRateOfTurn();
        std::string getRepeatIndicator();
        std::string getSog();
        std::string getSpare();
        std::string getSpecialManoeuvreIndicator();
        std::string getTimestamp();
        std::string getTrueHeading();
        std::string getValid();
        std::string getMMSI();
        std::string getShipName();
        std::string getTimeUtc();
        std::string getTags();
        std::string getGeohash();
    private:
        std::string MessageType;
        std::string Cog;
        std::string CommunicationState;
        std::string Latitude;
        std::string Longitude;
        std::string MessageID;
        std::string NavigationalStatus;
        std::string PositionAccuracy;
        std::string Raim;
        std::string RateOfTurn;
        std::string RepeatIndicator;
        std::string Sog;
        std::string Spare;
        std::string SpecialManoeuvreIndicator;
        std::string Timestamp;
        std::string TrueHeading;
        std::string Valid;
        std::string MMSI;
        std::string ShipName;
        std::string Tags;
        std::string TimeUtc;
        std::string Geohash;
};