from . import *
from . import Base
class FilterMessageTypes(Base):

    __tablename__ = "filtermessagetypes"

    FilterMessageTypesID = Column(Integer, primary_key=True, autoincrement=True)
    SubscribeMessageID = Column(UUID(as_uuid=True),ForeignKey('subscribemessage.SubscribeMessageID'))
    MessageType = Column(String(255))

    index_filtermessagetypes_SubscribeMessageID = Index('index_filtermessagetypes_SubscribeMessageID', SubscribeMessageID)

    def serialize(self):
        return {
            "filtermessagetypesID": self.FilterMessageTypes,
            "SubscribeMessageID": self.SubscribeMessageID,
            "MessageType": self.MessageType
        }