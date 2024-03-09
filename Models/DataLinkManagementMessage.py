from . import Base
from . import *

class DataLinkManagementMessage(Base):
    __tablename__ = 'datalinkmanagementmessage'
    
    DataLinkManagementMessageID = Column(BIGINT, primary_key=True, autoincrement=True)
    MMSI = Column(BIGINT)
    MessageType = Column(String(255), nullable=False)
    RepeatIndicator = Column(Integer)
    ShipName = Column(String(255))
    Geom = Column(Geometry(geometry_type='POINT', srid=4326, spatial_index=True, use_typmod=True))
    TimeUtc = Column(DateTime)
    SubscribeMessageID = Column(UUID(as_uuid=True),ForeignKey('subscribemessage.SubscribeMessageID'))
    data_hash = Column(CHAR(36), unique=True)
    MessageID = Column(Integer)
    Spare = Column(Integer)
    Valid = Column(Boolean)
    Increment1 = Column(Integer)
    Offset1 = Column(Integer)
    TimeOut1 = Column(Integer)
    Valid1 = Column(Boolean)
    integerOfSlots1 = Column(Integer)
    Increment2 = Column(Integer)
    Offset2 = Column(Integer)
    TimeOut2 = Column(Integer)
    Valid2 = Column(Boolean)
    integerOfSlots2 = Column(Integer)
    Increment3 = Column(Integer)
    Offset3 = Column(Integer)
    TimeOut3 = Column(Integer)
    Valid3 = Column(Boolean)
    integerOfSlots3 = Column(Integer)
    Increment4 = Column(Integer)
    Offset4 = Column(Integer)
    TimeOut4 = Column(Integer)
    Valid4 = Column(Boolean)
    integerOfSlots4 = Column(Integer)

    
    idx_datalinkmanagementmessage_time_utc = Index('idx_datalinkmanagementmessage_time_utc', TimeUtc)
    idx_datalinkmanagementmessage_geom = Index('idx_datalinkmanagementmessage_geom', Geom,postgresql_using='gist')
    idx_datalinkmanagementmessage_mmsi = Index('idx_datalinkmanagementmessage_mmsi', MMSI)
