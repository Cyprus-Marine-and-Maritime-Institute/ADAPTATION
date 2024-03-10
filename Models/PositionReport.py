from . import *
from . import Base
from . import ShipCommonData
class PositionReport(Base):
    __tablename__ = "positionreport"

    PositionReportID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ShipCommonDataID = Column(UUID(as_uuid=True), ForeignKey(ShipCommonData.ShipCommonData.ShipCommonDataID))
    Cog = Column(Float)
    CommunicationState = Column(Integer)
    NavigationalStatus = Column(Integer)
    PositionAccuracy = Column(Boolean)
    Raim = Column(Boolean)
    RateOfTurn = Column(Integer)
    Sog = Column(Float)
    Spare = Column(Integer)
    SpecialManoeuvreIndicator = Column(Integer)
    Timestamp = Column(Integer)
    TrueHeading = Column(Integer)

    idx_positionreport_ShipCommonDataID = Index('idx_positionreport_ShipCommonDataID', ShipCommonDataID)
    
    def serialize(self):
        return {
            "positionreportID": self.PositionReportID,
            "ShipCommonDataID": self.ShipCommonDataID,
            "Cog": self.Cog,
            "CommunicationState": self.CommunicationState,
            "NavigationalStatus": self.NavigationalStatus,
            "PositionAccuracy": self.PositionAccuracy,
            "Raim": self.Raim,
            "RateOfTurn": self.RateOfTurn,
            "Sog": self.Sog,
            "Spare": self.Spare,
            "SpecialManoeuvreIndicator": self.SpecialManoeuvreIndicator,
            "Timestamp": self.Timestamp,
            "TrueHeading": self.TrueHeading
        }