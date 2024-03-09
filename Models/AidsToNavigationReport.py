from . import Base
from . import *

class AidsToNavigationReport(Base):
    __tablename__ = 'aidstonavigationreport'
    
    AidsToNavigationReportID = Column(BIGINT, primary_key=True, autoincrement=True)
    MMSI = Column(BIGINT)
    MessageType = Column(String(255), nullable=False)
    ShipName = Column(String(255))
    TimeUtc = Column(DateTime, nullable=False)
    SubscribeMessageID = Column(UUID(as_uuid=True),ForeignKey('subscribemessage.SubscribeMessageID'))
    MessageID = Column(Integer)
    AssignedMode = Column(Boolean)
    AtoN = Column(Integer)
    DimensionA = Column(Integer)
    DimensionB = Column(Integer)
    DimensionC = Column(Integer)
    DimensionD = Column(Integer)
    Fixtype = Column(Integer)
    Geom = Column(Geometry(geometry_type='POINT', srid=4326, spatial_index=True, use_typmod=True))
    Name = Column(String(255))
    NameExtension = Column(String(255))
    OffPosition = Column(Boolean)
    PositionAccuracy = Column(Boolean)
    Raim = Column(Boolean)
    RepeatIndicator = Column(Integer)
    Spare = Column(Boolean)
    Timestamp = Column(Integer)
    Type = Column(Integer)
    Valid = Column(Boolean)
    VirtualAtoN = Column(Boolean)

    idx_aidstonavigationreport_time_utc = Index('idx_aidstonavigationreport_time_utc', TimeUtc)
    idx_aidstonavigationreport_geom = Index('idx_aidstonavigationreport_geom', Geom,postgresql_using='gist')
    idx_aidstonavigationreport_mmsi = Index('idx_aidstonavigationreport_mmsi', MMSI)
