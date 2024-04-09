
#include "ShipStaticDataRow.h"

ShipStaticDataRow::ShipStaticDataRow(){


}

ShipStaticDataRow::~ShipStaticDataRow(){
    
}

std::stringstream ShipStaticDataRow::print(){
    std::stringstream ss;
    ss << "MessageType"<< this -> MessageType << ',';
    ss << "AisVersion"<< this -> AisVersion << ',';
    ss << "CallSign"<< this -> CallSign << ',';
    ss << "Destination"<< this -> Destination << ',';
    ss << "DimensionA"<< this -> DimensionA << ',';
    ss << "DimensionB"<< this -> DimensionB << ',';
    ss << "DimensionC"<< this -> DimensionC << ',';
    ss << "DimensionD"<< this -> DimensionD << ',';
    ss << "Dte"<< this -> Dte << ',';
    ss << "EtaDay"<< this -> EtaDay << ',';
    ss << "EtaHour"<< this -> EtaHour << ',';
    ss << "EtaMinute"<< this -> EtaMinute << ',';
    ss << "EtaMonth"<< this -> EtaMonth << ',';
    ss << "FixType"<< this -> FixType << ',';
    ss << "ImoNumber"<< this -> ImoNumber << ',';
    ss << "MaximumStaticDraught"<< this -> MaximumStaticDraught << ',';
    ss << "RepeatIndicator"<< this -> RepeatIndicator << ',';
    ss << "Spare"<< this -> Spare << ',';
    ss << "ShipType"<< this -> ShipType << ',';
    ss << "Valid"<< this -> Valid << ',';
    ss << "MMSI"<< this -> MMSI << ',';
    ss << "ShipName"<< this -> ShipName << ',';
    ss << "TimeUtc"<< this -> TimeUtc << ',';
    // std::ss << "Geohash: " << this -> Geohash << ',';
    std::cout << ss.str();
    return ss;
}
std::string ShipStaticDataRow::getRowString(){
    std::stringstream ss;
    ss << this-> MessageType<< ',';
    ss << this-> AisVersion<< ',';
    ss << '"'<< this-> CallSign<<'"' << ',';
    ss << '"' << this-> Destination<< '"' << ',';
    ss << this-> DimensionA<< ',';
    ss << this-> DimensionB<< ',';
    ss << this-> DimensionC<< ',';
    ss << this-> DimensionD<< ',';
    ss << this-> Dte<< ',';
    ss << this-> EtaDay<< ',';
    ss << this-> EtaHour<< ',';
    ss << this-> EtaMinute<< ',';
    ss << this-> EtaMonth<< ',';
    ss << this-> FixType<< ',';
    ss << this-> ImoNumber<< ',';
    ss << this-> MaximumStaticDraught<< ',';
    ss << this-> RepeatIndicator<< ',';
    ss << this-> Spare<< ',';
    ss << this-> ShipType<< ',';
    ss << this-> Valid<< ',';
    ss << this-> MMSI<< ',';
    ss << '"' << this-> ShipName<< '"' << ',';
    ss << this-> TimeUtc;

    return ss.str();
}

// setters
void ShipStaticDataRow::setMessageType(std::string MessageType){
    this ->MessageType= MessageType;
}
void ShipStaticDataRow::setAisVersion(std::string AisVersion){
    this ->AisVersion= AisVersion;
}
void ShipStaticDataRow::setCallSign(std::string CallSign){
    this ->CallSign= CallSign;
}
void ShipStaticDataRow::setDestination(std::string Destination){
    this ->Destination= Destination;
}
void ShipStaticDataRow::setDimensionA(std::string DimensionA){
    this ->DimensionA= DimensionA;
}
void ShipStaticDataRow::setDimensionB(std::string DimensionB){
    this ->DimensionB= DimensionB;
}
void ShipStaticDataRow::setDimensionC(std::string DimensionC){
    this ->DimensionC= DimensionC;
}
void ShipStaticDataRow::setDimensionD(std::string DimensionD){
    this ->DimensionD=  DimensionD;
}
void ShipStaticDataRow::setDte(std::string Dte){
    this ->Dte= Dte;
}
void ShipStaticDataRow::setEtaDay(std::string EtaDay){
    this ->EtaDay= EtaDay;
}
void ShipStaticDataRow::setEtaHour(std::string EtaHour){
    this ->EtaHour= EtaHour;
}
void ShipStaticDataRow::setEtaMinute(std::string EtaMinute){
    this ->EtaMinute= EtaMinute;
}
void ShipStaticDataRow::setEtaMonth(std::string EtaMonth){
    this ->EtaMonth= EtaMonth;
}
void ShipStaticDataRow::setFixType(std::string FixType){
    this ->FixType= FixType;
}
void ShipStaticDataRow::setImoNumber(std::string ImoNumber){
    this ->ImoNumber= ImoNumber;
}
void ShipStaticDataRow::setMaximumStaticDraught(std::string MaximumStaticDraught){
    this ->MaximumStaticDraught= MaximumStaticDraught;
}
void ShipStaticDataRow::setRepeatIndicator(std::string RepeatIndicator){
    this ->RepeatIndicator= RepeatIndicator;
}
void ShipStaticDataRow::setSpare(std::string Spare){
    this ->Spare= Spare;
}
void ShipStaticDataRow::setShipType(std::string ShipType){
    this ->ShipType= ShipType;
}
void ShipStaticDataRow::setValid(std::string Valid){
    this ->Valid= Valid;
}
void ShipStaticDataRow::setMMSI(std::string MMSI){
    this ->MMSI= MMSI;
}
void ShipStaticDataRow::setShipName(std::string ShipName){
    this ->ShipName= ShipName;
}
void ShipStaticDataRow::setTimeUtc(std::string TimeUtc){
    this ->TimeUtc= TimeUtc;
}
// getters
std::string ShipStaticDataRow::getMessageType(){
    return this->MessageType;
}
std::string ShipStaticDataRow::getAisVersion(){
    return this->AisVersion;
}
std::string ShipStaticDataRow::getCallSign(){
    return this->CallSign;
}
std::string ShipStaticDataRow::getDestination(){
    return this->Destination;
}
std::string ShipStaticDataRow::getDimensionA(){
    return this->DimensionA;
}
std::string ShipStaticDataRow::getDimensionB(){
    return this->DimensionB;
}
std::string ShipStaticDataRow::getDimensionC(){
    return this->DimensionC;
}
std::string ShipStaticDataRow::getDimensionD(){
    return this->DimensionD;
}
std::string ShipStaticDataRow::getDte(){
    return this->Dte;
}
std::string ShipStaticDataRow::getEtaDay(){
    return this->EtaDay;
}
std::string ShipStaticDataRow::getEtaHour(){
    return this->EtaHour;
}
std::string ShipStaticDataRow::getEtaMinute(){
    return this->EtaMinute;
}
std::string ShipStaticDataRow::getEtaMonth(){
    return this->EtaMonth;
}
std::string ShipStaticDataRow::getFixType(){
    return this->FixType;
}
std::string ShipStaticDataRow::getImoNumber(){
    return this->ImoNumber;
}
std::string ShipStaticDataRow::getMaximumStaticDraught(){
    return this->MaximumStaticDraught;
}
std::string ShipStaticDataRow::getRepeatIndicator(){
    return this->RepeatIndicator;
}
std::string ShipStaticDataRow::getSpare(){
    return this->Spare;
}
std::string ShipStaticDataRow::getShipType(){
    return this->ShipType;
}
std::string ShipStaticDataRow::getValid(){
    return this->Valid;
}
std::string ShipStaticDataRow::getMMSI(){
    return this->MMSI;
}
std::string ShipStaticDataRow::getShipName(){
    return this->ShipName;
}
std::string ShipStaticDataRow::getTimeUtc(){
    return this->TimeUtc;
}
