from . import *
from . import Base
class BoundingBox(Base):

    __tablename__ = "boundingbox"

    BoundingBoxID = Column(Integer, primary_key=True, autoincrement=True)
    SubscribeMessageID = Column(UUID(as_uuid=True),ForeignKey('subscribemessage.SubscribeMessageID'))
    Polygon = Column(Geometry('POLYGON'))

    index_boundingbox_SubscribeMessageID = Index('index_boundingbox_SubscribeMessageID', SubscribeMessageID)

    def serialize(self):
        return {
            "BoundingBoxID": self.BoundingBoxID,
            "SubscribeMessageID": self.SubscribeMessageID,
            "Polygon": self.Polygon
        }