from . import Base
from . import *

class AddressedSafetyMessage(Base):
    __tablename__ = 'addressedsafetymessage'
    
    AddressedSafetyMessageID = Column(BIGINT, primary_key=True, autoincrement=True)
    MMSI = Column(BIGINT)
    MessageType = Column(String(255), nullable=False)
    ShipName = Column(String(255))
    Geom = Column(Geometry(geometry_type='POINT', srid=4326, spatial_index=True, use_typmod=True))
    TimeUtc = Column(DateTime, nullable=False)
    SubscribeMessageID = Column(UUID(as_uuid=True),ForeignKey('subscribemessage.SubscribeMessageID'))
    MessageID = Column(Integer)
    DestinationID = Column(BIGINT)
    RepeatIndicator = Column(Integer)
    Retransmission = Column(Boolean)
    Sequenceinteger = Column(Integer)
    Spare = Column(Boolean)
    Text = Column(TEXT)
    Valid = Column(Boolean)

    
    idx_addressedsafetymessage_time_utc = Index('idx_addressedsafetysessage_time_utc', TimeUtc)
    idx_addressedsafetymessage_geom = Index('idx_addressedsafetymessage_geom', Geom,postgresql_using='gist')
    idx_addressedsafetymessage_mmsi = Index('idx_sddressedsafetymessage_mmsi', MMSI)
