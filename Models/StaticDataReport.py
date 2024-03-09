
from . import *
from . import Base
class StaticDataReport(Base):
    __tablename__ = "staticdatareport"

    StaticDataReportID = Column(Integer, primary_key=True, autoincrement=True)
    ShipCommonDataID = Column(UUID(as_uuid=True), ForeignKey('shipcommondata.ShipCommonDataID'))
    PartNumber = Column(Boolean)
    ReportAName = Column(String(255))
    CallSign = Column(String(10))
    DimensionA = Column(Integer)
    DimensionB = Column(Integer)
    DimensionC = Column(Integer)
    DimensionD = Column(Integer)
    FixType = Column(Integer)
    ShipType = Column(Integer)
    Spare = Column(Integer)
    VenderIDModel = Column(Integer)
    VenderIDSerial = Column(Integer)
    VendorIDName = Column(String(255))
    Reserved = Column(Integer)


    idx_staticdatareport_ShipCommonDataID = Index('idx_staticdatareport_ShipCommonDataID', ShipCommonDataID)
    idx_staticdatareport_ship_type = Index('idx_staticdatareport_ship_type', ShipType)

    def serialize(self):
        return {
            "StaticDataReportID": self.StaticDataReportID,
            "ShipCommonDataID": self.ShipCommonDataID,
            "PartNumber": self.PartNumber,
            "CallSign": self.CallSign,
            "DimensionA": self.DimensionA,
            "DimensionB": self.DimensionB,
            "DimensionC": self.DimensionC,
            "DimensionD": self.DimensionD,
            "FixType": self.FixType,
            "ShipType": self.ShipType,
            "Spare": self.Spare,
            "VenderIDModel": self.VenderIDModel,
            "VenderIDSerial": self.VenderIDSerial,
            "VendorIDName": self.VendorIDName,
            "Reserved": self.Reserved
        }