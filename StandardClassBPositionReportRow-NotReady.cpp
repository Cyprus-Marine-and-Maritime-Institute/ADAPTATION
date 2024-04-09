
#include "StandardClassBPositionReportRow.h"

StandardClassBPositionReportRow::StandardClassBPositionReportRow(){


}

StandardClassBPositionReportRow::~StandardClassBPositionReportRow(){
    
}

std::stringstream StandardClassBPositionReportRow::print(){
    std::stringstream ss;
    ss << "MessageType: " << this -> MessageType << ',';
    ss << "Cog: " << this -> Cog << ',';
    ss << "CommunicationState: " << this -> CommunicationState << ',';
    ss << "Latitude: " << this -> Latitude << ',';
    ss << "Longitude: " << this -> Longitude << ',';
    ss << "MessageID: " << this -> MessageID << ',';
    ss << "NavigationalStatus: " << this -> NavigationalStatus << ',';
    ss << "PositionAccuracy: " << this -> PositionAccuracy << ',';
    ss << "Raim: " << this -> Raim << ',';
    ss << "RateOfTurn: " << this -> RateOfTurn << ',';
    ss << "RepeatIndicator: " << this -> RepeatIndicator << ',';
    ss << "Sog: " << this -> Sog << ',';
    ss << "Spare: " << this -> Spare << ',';
    ss << "SpecialManoeuvreIndicator: " << this -> SpecialManoeuvreIndicator << ',';
    ss << "Timestamp: " << this -> Timestamp << ',';
    ss << "TrueHeading: " << this -> TrueHeading << ',';
    ss << "Valid: " << this -> Valid << ',';
    ss << "MMSI: " << this -> MMSI << ',';
    ss << "ShipName: " << '"' <<this -> ShipName << '"'<< ',';
    ss << "TimeUtc: " << this -> TimeUtc;
    // std::ss << "Geohash: " << this -> Geohash << ',';
    std::cout << ss.str();
    return ss;
}
std::string StandardClassBPositionReportRow::getRowString(){
    std::stringstream ss;
    ss << this -> MessageType << ',';
    ss << this -> Cog << ',';
    ss << this -> CommunicationState << ',';
    ss << this -> Latitude << ',';
    ss << this -> Longitude << ',';
    ss << this -> MessageID << ',';
    ss << this -> NavigationalStatus << ',';
    ss << this -> PositionAccuracy << ',';
    ss << this -> Raim << ',';
    ss << this -> RateOfTurn << ',';
    ss << this -> RepeatIndicator << ',';
    ss << this -> Sog << ',';
    ss << this -> Spare << ',';
    ss << this -> SpecialManoeuvreIndicator << ',';
    ss << this -> Timestamp << ',';
    ss << this -> TrueHeading << ',';
    ss << this -> Valid << ',';
    ss << this -> MMSI << ',';
    ss <<'"' << this -> ShipName <<'"' << ',';
    ss << this -> TimeUtc;

    return ss.str();
}

// setters
void StandardClassBPositionReportRow::setMessageType(std::string MessageType){
    this -> MessageType = MessageType;
    }
void StandardClassBPositionReportRow::setCog(std::string Cog){
        this -> Cog = Cog;
    }
void StandardClassBPositionReportRow::setCommunicationState(std::string CommunicationState){
        this -> CommunicationState = CommunicationState;
    }
void StandardClassBPositionReportRow::setLatitude(std::string Latitude){
        this -> Latitude = Latitude;
    }
void StandardClassBPositionReportRow::setLongitude(std::string Longitude){
        this -> Longitude = Longitude;
    }
void StandardClassBPositionReportRow::setMessageID(std::string MessageID){
        this -> MessageID = MessageID;
    }
void StandardClassBPositionReportRow::setNavigationalStatus(std::string NavigationalStatus){
        this -> NavigationalStatus = NavigationalStatus;
    }
void StandardClassBPositionReportRow::setPositionAccuracy(std::string PositionAccuracy){
        this -> PositionAccuracy = PositionAccuracy;
    }
void StandardClassBPositionReportRow::setRaim(std::string Raim){
        this -> Raim = Raim;
    }
void StandardClassBPositionReportRow::setRateOfTurn(std::string RateOfTurn){
        this -> RateOfTurn = RateOfTurn;
    }
void StandardClassBPositionReportRow::setRepeatIndicator(std::string RepeatIndicator){
        this -> RepeatIndicator = RepeatIndicator;
    }
void StandardClassBPositionReportRow::setSog(std::string Sog){
        this -> Sog = Sog;
    }
void StandardClassBPositionReportRow::setSpare(std::string Spare){
        this -> Spare = Spare;
    }
void StandardClassBPositionReportRow::setSpecialManoeuvreIndicator(std::string SpecialManoeuvreIndicator){
        this -> SpecialManoeuvreIndicator = SpecialManoeuvreIndicator;
    }
void StandardClassBPositionReportRow::setTimestamp(std::string Timestamp){
        this -> Timestamp = Timestamp;
    }
void StandardClassBPositionReportRow::setTrueHeading(std::string TrueHeading){
        this -> TrueHeading = TrueHeading;
    }
void StandardClassBPositionReportRow::setValid(std::string Valid){
        this -> Valid = Valid;
    }
void StandardClassBPositionReportRow::setMMSI(std::string MMSI){
        this -> MMSI = MMSI;
    }
void StandardClassBPositionReportRow::setShipName(std::string ShipName){
        this -> ShipName = ShipName;
    }
void StandardClassBPositionReportRow::setTimeUtc(std::string TimeUtc){
        this -> TimeUtc = TimeUtc;
    }
void StandardClassBPositionReportRow::setGeohash(std::string Geohash){
        this -> Geohash = Geohash;
    }
// getters
std::string StandardClassBPositionReportRow::getMessageType(){
        return this -> MessageType;
    }
std::string StandardClassBPositionReportRow::getCog(){
        return this -> Cog;
    }
std::string StandardClassBPositionReportRow::getCommunicationState(){
        return this -> CommunicationState;
    }
std::string StandardClassBPositionReportRow::getLatitude(){
        return this -> Latitude;
    }
std::string StandardClassBPositionReportRow::getLongitude(){
        return this -> Longitude;
    }
std::string StandardClassBPositionReportRow::getMessageID(){
        return this -> MessageID;
    }
std::string StandardClassBPositionReportRow::getNavigationalStatus(){
        return this -> NavigationalStatus;
    }
std::string StandardClassBPositionReportRow::getPositionAccuracy(){
        return this -> PositionAccuracy;
    }
std::string StandardClassBPositionReportRow::getRaim(){
        return this -> Raim;
    }
std::string StandardClassBPositionReportRow::getRateOfTurn(){
        return this -> RateOfTurn;
    }
std::string StandardClassBPositionReportRow::getRepeatIndicator(){
        return this -> RepeatIndicator;
    }
std::string StandardClassBPositionReportRow::getSog(){
        return this -> Sog;
    }
std::string StandardClassBPositionReportRow::getSpare(){
        return this -> Spare;
    }
std::string StandardClassBPositionReportRow::getSpecialManoeuvreIndicator(){
        return this -> SpecialManoeuvreIndicator;
    }
std::string StandardClassBPositionReportRow::getTimestamp(){
        return this -> Timestamp;
    }
std::string StandardClassBPositionReportRow::getTrueHeading(){
        return this -> TrueHeading;
    }
std::string StandardClassBPositionReportRow::getValid(){
        return this -> Valid;
    }
std::string StandardClassBPositionReportRow::getMMSI(){
        return this -> MMSI;
    }
std::string StandardClassBPositionReportRow::getShipName(){
        return this -> ShipName;
    }
std::string StandardClassBPositionReportRow::getTimeUtc(){
        return this -> TimeUtc;
    }
std::string StandardClassBPositionReportRow::getGeohash(){
        return this -> Geohash;
    }
