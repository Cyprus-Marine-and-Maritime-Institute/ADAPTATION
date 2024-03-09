
from . import *
from . import Base
class SubscribeMessage(Base):
    __tablename__ = "subscribemessage"

    SubscribeMessageID = Column(UUID(as_uuid=True), primary_key=True)
    APIKey = Column(String(255))
    Name = Column(String(255))

    
    
    def serialize(self):
        return {
            "SubscribeMessageID": self.SubscribeMessageID,
            "APIKey": self.APIKey,
            "Name": self.Name
        }