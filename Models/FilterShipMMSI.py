from . import *
from . import Base
class FilterShipMMSI(Base):
    __tablename__ = "filtershipmmsi"

    FilterShipMMSIID = Column(Integer, primary_key=True, autoincrement=True)
    SubscribeMessageID = Column(UUID(as_uuid=True),ForeignKey('subscribemessage.SubscribeMessageID'))
    MMSI = Column(TEXT)

    index_filtershipmmsi_SubscribeMessageID = Index('index_filtershipmmsi_SubscribeMessageID', SubscribeMessageID)

    def serialize(self):
        return {
            "filtershipmmsiID": self.FilterShipMMSI,
            "SubscribeMessageID": self.SubscribeMessageID,
            "MMSI": self.MMSI
        }

