
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
class ShipStaticDataRow{
    public:
        ShipStaticDataRow();
        ~ShipStaticDataRow();
        std::stringstream print();
        std::string getRowString();
        // Setters
        void setMessageType(std::string MessageType);
        void setAisVersion(std::string AisVersion);
        void setCallSign(std::string CallSign);
        void setDestination(std::string Destination);
        void setDimensionA(std::string DimensionA);
        void setDimensionB(std::string DimensionB);
        void setDimensionC(std::string DimensionC);
        void setDimensionD(std::string DimensionD);
        void setDte(std::string Dte);
        void setEtaDay(std::string EtaDay);
        void setEtaHour(std::string EtaHour);
        void setEtaMinute(std::string EtaMinute);
        void setEtaMonth(std::string EtaMonth);
        void setFixType(std::string FixType);
        void setImoNumber(std::string ImoNumber);
        void setMaximumStaticDraught(std::string MaximumStaticDraught);
        void setRepeatIndicator(std::string RepeatIndicator);
        void setSpare(std::string Spare);
        void setShipType(std::string ShipType);
        void setValid(std::string Valid);
        void setMMSI(std::string MMSI);
        void setShipName(std::string ShipName);
        void setTimeUtc(std::string TimeUtc);
        // Getters

        std::string getMessageType();
        std::string getAisVersion();
        std::string getCallSign();
        std::string getDestination();
        std::string getDimensionA();
        std::string getDimensionB();
        std::string getDimensionC();
        std::string getDimensionD();
        std::string getDte();
        std::string getEtaDay();
        std::string getEtaHour();
        std::string getEtaMinute();
        std::string getEtaMonth();
        std::string getFixType();
        std::string getImoNumber();
        std::string getMaximumStaticDraught();
        std::string getRepeatIndicator();
        std::string getSpare();
        std::string getShipType();
        std::string getValid();
        std::string getMMSI();
        std::string getShipName();
        std::string getTimeUtc();
    private:
        std::string MessageType;
        std::string AisVersion;
        std::string CallSign;
        std::string Destination;
        std::string DimensionA;
        std::string DimensionB;
        std::string DimensionC;
        std::string DimensionD;
        std::string Dte;
        std::string EtaDay;
        std::string EtaHour;
        std::string EtaMinute;
        std::string EtaMonth;
        std::string FixType;
        std::string ImoNumber;
        std::string MaximumStaticDraught;
        std::string RepeatIndicator;
        std::string Spare;
        std::string ShipType;
        std::string Valid;
        std::string MMSI;
        std::string ShipName;
        std::string TimeUtc;
};