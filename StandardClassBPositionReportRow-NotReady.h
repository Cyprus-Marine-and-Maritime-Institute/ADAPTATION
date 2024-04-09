
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
class StandardClassBPositionReportRow{
    public:
        StandardClassBPositionReportRow();
        ~StandardClassBPositionReportRow();
        std::stringstream print();
        std::string getRowString();
        // Setters
        // The now count is 31
        // MessageType,[0]
        // AssignedMode,[1]
        // ClassBBand,[2]
        // ClassBDisplay,[3]
        // ClassBDsc,[4]
        // ClassBMsg22,[5]
        // ClassBUnit,[6]
        // Cog,[7]
        // CommunicationState,[8]
        // CommunicationStateIsItdma,[9]
        // Message.StandardClassBPositionReport.Latitude,[10]
        // Message.StandardClassBPositionReport.Longitude,[11]
        // MessageID,[12]
        // PositionAccuracy,[13]
        // Raim,[14]
        // RepeatIndicator,[15]
        // Sog,[16]
        // Spare1,[17]
        // Spare2,[18]
        // Timestamp,[19]
        // TrueHeading,[20]
        // Message.StandardClassBPositionReport.UserID,[21]
        // Valid,[22]
        // MMSI,[23]
        // MetaData.MMSI_String,[24]
        // ShipName,[25]
        // MetaData.latitude,[26]
        // MetaData.longitude,[27]
        // TimeUtc,[28]
        // Geom,[29]
        // ShipCommonDataID[30]
        // //Most Data count is 27
        // ,MessageType[0],
        // Message.StandardClassBPositionReport.Cog,[7]
        // Message.StandardClassBPositionReport.CommunicationState,[8]
        // Message.StandardClassBPositionReport.Latitude,[10]
        // Message.StandardClassBPositionReport.Longitude,[11]
        // Message.StandardClassBPositionReport.MessageID,[12]
        // Message.StandardClassBPositionReport.PositionAccuracy,[13]
        // Message.StandardClassBPositionReport.Raim,[14]
        // Message.StandardClassBPositionReport.RepeatIndicator,[15]
        // Message.StandardClassBPositionReport.Sog,[16]
        // Message.StandardClassBPositionReport.Spare1,[17]
        // Message.StandardClassBPositionReport.Timestamp,[19]
        // Message.StandardClassBPositionReport.TrueHeading,[20]
        // Message.StandardClassBPositionReport.Valid,[22]
        // MetaData.MMSI,[23]
        // MetaData.ShipName,[24]
        // MetaData.time_utc[26]
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
        void setGeohash(std::string Geohash);
        // Getters
        std::string getMessageType();
        std::string getCog();
        std::string getCommunicationState();
        std::string getLatitude();
        std::string getLongitude();
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
        std::string TimeUtc;
        std::string Geohash;
};