
from . import *
from . import Base
from sqlalchemy import literal_column
class ShipCommonData(Base):
    __tablename__ = "shipcommondata"

    ShipCommonDataID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    MMSI = Column(Integer)
    MessageType = Column(String(255))
    ShipName = Column(String(255))
    TimeUtc = Column(DateTime)
    SubscribeMessageID = Column(UUID(as_uuid=True),ForeignKey('subscribemessage.SubscribeMessageID'))
    MessageID = Column(Integer)
    RepeatIndicator = Column(Integer)
    Valid = Column(Boolean)
    Geom = Column(Geometry(geometry_type='POINT', srid=4326, spatial_index=True, use_typmod=True))

    
    idx_time_utc = Index('idx_common_time_utc', TimeUtc)
    idx_geom = Index('idx_common_geom', Geom,postgresql_using='gist')
    idx_mmsi = Index('idx_common_mmsi', MMSI)
    idx_ship_common_data_time_rounded_30m = Index(
    'idx_ship_common_data_time_rounded_30m',
    func.date_trunc('hour', TimeUtc) +
    literal_column("INTERVAL '30 min'") * func.round(func.date_part('minute', TimeUtc) / 30.0)
    )
    # composite indexes
    idx_time_utc_geom = Index('idx_time_utc_common_geom', TimeUtc, Geom)
    idx_time_utc_mmsi = Index('idx_time_utc_common_mmsi', TimeUtc, MMSI)


    idx_ship_common_data_mmsi_time_30m = Index(
    'idx_ship_common_data_mmsi_time_30m',
    MMSI,
    func.date_trunc('hour', TimeUtc) +
    literal_column("INTERVAL '30 min'") * func.round(func.date_part('minute', TimeUtc) / 30.0)
    )

    # Relationships back refs
    position_reports = relationship("PositionReport", backref="ship_common_data")
    static_data_reports = relationship("StaticDataReport", backref="ship_common_data")
    standard_class_b_position_reports = relationship("StandardClassBPositionReport", backref="ship_common_data")
    ship_static_data = relationship("ShipStaticData", backref="ship_common_data")




    def serialize(self):
        return {
            "ShipCommonDataID": self.ShipCommonDataID,
            "MMSI": self.MMSI,
            "MessageType": self.MessageType,
            "ShipName": self.ShipName,
            "TimeUtc": self.TimeUtc,
            "SubscribeMessageID": self.SubscribeMessageID,
            "MessageID": self.MessageID,
            "RepeatIndicator": self.RepeatIndicator,
            "Valid": self.Valid,
            "Geom": self.Geom
        }
    