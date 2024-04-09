
#include "PositionReportRow.h"

PositionReportRow::PositionReportRow(){


}

PositionReportRow::~PositionReportRow(){
    
}

std::stringstream PositionReportRow::print(){
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
std::string PositionReportRow::getRowString(){
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
std::string PositionReportRow::getRowStringWithTags(){
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
    ss << this -> TimeUtc << ',';
    ss <<'"' << this -> Tags<<'"';

    return ss.str();
}
// setters
void PositionReportRow::setMessageType(std::string MessageType){
    this -> MessageType = MessageType;
    }
void PositionReportRow::setCog(std::string Cog){
        this -> Cog = Cog;
    }
void PositionReportRow::setCommunicationState(std::string CommunicationState){
        this -> CommunicationState = CommunicationState;
    }
void PositionReportRow::setLatitude(std::string Latitude){
        this -> Latitude = Latitude;
    }
void PositionReportRow::setLongitude(std::string Longitude){
        this -> Longitude = Longitude;
    }
void PositionReportRow::setMessageID(std::string MessageID){
        this -> MessageID = MessageID;
    }
void PositionReportRow::setNavigationalStatus(std::string NavigationalStatus){
        this -> NavigationalStatus = NavigationalStatus;
    }
void PositionReportRow::setPositionAccuracy(std::string PositionAccuracy){
        this -> PositionAccuracy = PositionAccuracy;
    }
void PositionReportRow::setRaim(std::string Raim){
        this -> Raim = Raim;
    }
void PositionReportRow::setRateOfTurn(std::string RateOfTurn){
        this -> RateOfTurn = RateOfTurn;
    }
void PositionReportRow::setRepeatIndicator(std::string RepeatIndicator){
        this -> RepeatIndicator = RepeatIndicator;
    }
void PositionReportRow::setSog(std::string Sog){
        this -> Sog = Sog;
    }
void PositionReportRow::setSpare(std::string Spare){
        this -> Spare = Spare;
    }
void PositionReportRow::setSpecialManoeuvreIndicator(std::string SpecialManoeuvreIndicator){
        this -> SpecialManoeuvreIndicator = SpecialManoeuvreIndicator;
    }
void PositionReportRow::setTimestamp(std::string Timestamp){
        this -> Timestamp = Timestamp;
    }
void PositionReportRow::setTrueHeading(std::string TrueHeading){
        this -> TrueHeading = TrueHeading;
    }
void PositionReportRow::setValid(std::string Valid){
        this -> Valid = Valid;
    }
void PositionReportRow::setMMSI(std::string MMSI){
        this -> MMSI = MMSI;
    }
void PositionReportRow::setShipName(std::string ShipName){
        this -> ShipName = ShipName;
    }
void PositionReportRow::setTimeUtc(std::string TimeUtc){
        this -> TimeUtc = TimeUtc;
    }
void PositionReportRow::setGeohash(std::string Geohash){
        this -> Geohash = Geohash;
    }
void PositionReportRow::setTags(std::string tags){
        this -> Tags = tags;
}
// getters
std::string PositionReportRow::getMessageType(){
        return this -> MessageType;
    }
std::string PositionReportRow::getCog(){
        return this -> Cog;
    }
std::string PositionReportRow::getCommunicationState(){
        return this -> CommunicationState;
    }
std::string PositionReportRow::getLatitude() const {
        return this -> Latitude;
    }
std::string PositionReportRow::getLongitude() const {
        return this -> Longitude;
    }
std::string PositionReportRow::getMessageID(){
        return this -> MessageID;
    }
std::string PositionReportRow::getNavigationalStatus(){
        return this -> NavigationalStatus;
    }
std::string PositionReportRow::getPositionAccuracy(){
        return this -> PositionAccuracy;
    }
std::string PositionReportRow::getRaim(){
        return this -> Raim;
    }
std::string PositionReportRow::getRateOfTurn(){
        return this -> RateOfTurn;
    }
std::string PositionReportRow::getRepeatIndicator(){
        return this -> RepeatIndicator;
    }
std::string PositionReportRow::getSog(){
        return this -> Sog;
    }
std::string PositionReportRow::getSpare(){
        return this -> Spare;
    }
std::string PositionReportRow::getSpecialManoeuvreIndicator(){
        return this -> SpecialManoeuvreIndicator;
    }
std::string PositionReportRow::getTimestamp(){
        return this -> Timestamp;
    }
std::string PositionReportRow::getTrueHeading(){
        return this -> TrueHeading;
    }
std::string PositionReportRow::getValid(){
        return this -> Valid;
    }
std::string PositionReportRow::getMMSI(){
        return this -> MMSI;
    }
std::string PositionReportRow::getShipName(){
        return this -> ShipName;
    }
std::string PositionReportRow::getTimeUtc(){
        return this -> TimeUtc;
    }
std::string PositionReportRow::getGeohash(){
        return this -> Geohash;
    }
std::string PositionReportRow::getTags(){
        return this -> Tags;
    }