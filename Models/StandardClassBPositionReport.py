from . import *

from . import Base
class StandardClassBPositionReport(Base):
    __tablename__ = "standardclassbpositionreport"

    StandardClassBPositionReportID = Column(Integer, primary_key=True, autoincrement=True)
    ShipCommonDataID = Column(UUID(as_uuid=True), ForeignKey('shipcommondata.ShipCommonDataID'))
    AssignedMode = Column(Boolean)
    ClassBBand = Column(Boolean)
    ClassBDisplay = Column(Boolean)
    ClassBDsc = Column(Boolean)
    ClassBMsg22 = Column(Boolean)
    ClassBUnit = Column(Boolean)
    Cog = Column(Float)
    CommunicationState = Column(Integer)
    CommunicationStateIsItdma = Column(Boolean)
    PositionAccuracy = Column(Boolean)
    Raim = Column(Boolean)
    Sog = Column(Float)
    Spare1 = Column(Integer)
    Spare2 = Column(Integer)
    Timestamp = Column(Integer)
    TrueHeading = Column(Integer)

    idx_standardclassbpositionreport_ShipCommonDataID = Index('idx_standardclassbpositionreport_ShipCommonDataID', ShipCommonDataID)

    def serialize(self):
        return {
            "StandardClassBPositionReportID": self.StandardClassBPositionReportID,
            "ShipCommonDataID": self.ShipCommonDataID,
            "AssignedMode": self.AssignedMode,
            "ClassBBand": self.ClassBBand,
            "ClassBDisplay": self.ClassBDisplay,
            "ClassBDsc": self.ClassBDsc,
            "ClassBMsg22": self.ClassBMsg22,
            "ClassBUnit": self.ClassBUnit,
            "Cog": self.Cog,
            "CommunicationState": self.CommunicationState,
            "CommunicationStateIsItdma": self.CommunicationStateIsItdma,
            "PositionAccuracy": self.PositionAccuracy,
            "Raim": self.Raim,
            "Sog": self.Sog,
            "Spare1": self.Spare1,
            "Spare2": self.Spare2,
            "Timestamp": self.Timestamp,
            "TrueHeading": self.TrueHeading

        }