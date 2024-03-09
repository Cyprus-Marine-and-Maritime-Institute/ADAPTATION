from . import *
from . import Base

class ShipStaticData(Base):
    __tablename__ = "shipstaticdata"

    ShipStaticDataID = Column(Integer, primary_key=True, autoincrement=True)
    ShipCommonDataID = Column(UUID(as_uuid=True), ForeignKey('shipcommondata.ShipCommonDataID'))
    AisVersion = Column(Integer)
    CallSign = Column(String(10))
    Destination = Column(String(255))
    DimensionA = Column(Integer)
    DimensionB = Column(Integer)
    DimensionC = Column(Integer)
    DimensionD = Column(Integer)
    Dte = Column(Boolean)
    EtaDay = Column(Integer)
    EtaHour = Column(Integer)
    EtaMinute = Column(Integer)
    EtaMonth = Column(Integer)
    FixType = Column(Integer)
    ImoNumber = Column(Integer)
    MaximumStaticDraught = Column(Float)
    Name = Column(String(255))
    RepeatIndicator = Column(Integer)
    Spare = Column(Boolean)
    ShipType = Column(Integer)

    idx_shipstaticdata_ship_type = Index('idx_shipstaticdata_ship_type', ShipType)
    idx_shipstaticdata_ShipCommonDataID = Index('idx_shipstaticdata_ShipCommonDataID', ShipCommonDataID)
    idx_shipstaticdata_imo_number = Index('idx_shipstaticdata_imo_number', ImoNumber)

    def serialize(self):
        return {
            "ShipCommonDataID": self.ShipCommonDataID,
            "ShipCommonDataID": self.ShipCommonDataID,
            "AisVersion": self.AisVersion,
            "CallSign": self.CallSign,
            "Destination": self.Destination,
            "DimensionA": self.DimensionA,
            "DimensionB": self.DimensionB,
            "DimensionC": self.DimensionC,
            "DimensionD": self.DimensionD,
            "Dte": self.Dte,
            "EtaDay": self.EtaDay,
            "EtaHour": self.EtaHour,
            "EtaMinute": self.EtaMinute,
            "EtaMonth": self.EtaMonth,
            "FixType": self.FixType,
            "ImoNumber": self.ImoNumber,
            "MaximumStaticDraught": self.MaximumStaticDraught,
            "Name": self.Name,
            "RepeatIndicator": self.RepeatIndicator,
            "Spare": self.Spare,
            "ShipType": self.ShipType
        }