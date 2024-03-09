from . import *
from . import Base
class BaseStationReport(Base):
    __tablename__ = 'basestationreport'
    
    BaseStationReportID = Column(BIGINT, primary_key=True, autoincrement=True)
    MMSI = Column(BIGINT)
    MessageType = Column(String(255), nullable=False)
    ShipName = Column(String(255))
    TimeUtc = Column(DateTime, nullable=False)
    SubscribeMessageID = Column(UUID(as_uuid=True),ForeignKey('subscribemessage.SubscribeMessageID'))
    MessageID = Column(Integer)
    CommunicationState = Column(Integer)
    FixType = Column(Integer)
    Geom = Column(Geometry(geometry_type='POINT', srid=4326, spatial_index=True, use_typmod=True))
    LongRangeEnable = Column(Boolean)
    PositionAccuracy = Column(Boolean)
    Raim = Column(Boolean)
    RepeatIndicator = Column(Integer)
    Spare = Column(Integer)
    UtcDay = Column(Integer)
    UtcHour = Column(Integer)
    UtcMinute = Column(Integer)
    UtcMonth = Column(Integer)
    UtcSecond = Column(Integer)
    UtcYear = Column(Integer)
    Valid = Column(Boolean)

    idx_basestationreport_time_utc = Index('idx_basestationreport_time_utc', TimeUtc)
    idx_basestationreport_geom = Index('idx_basestationreport_geom', Geom,postgresql_using='gist')
    idx_basestationreport_mmsi = Index('idx_basestationreport_mmsi', MMSI)


