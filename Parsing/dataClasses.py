from dataclasses import dataclass
from typing import Optional, Union
import uuid
from datetime import datetime
from geoalchemy2 import Geometry

@dataclass
class Dimension:
    A: int
    B: int
    C: int
    D: int
    def is_valid(self) -> bool:
        return all(0 <= x <= 511 for x in (self.A, self.B, self.C, self.D))

@dataclass
class Eta:
    Day: int
    Hour: int
    Minute: int
    Month: int

    def is_valid(self) -> bool:
        return 1 <= self.Day <= 31 and 0 <= self.Hour <= 23 and 0 <= self.Minute <= 59 and 1 <= self.Month <= 12


@dataclass
class MetaData:
    MMSI: int
    MMSI_String: str
    ShipName: str
    latitude: float
    longitude: float
    time_utc: str

    def is_valid(self) -> bool:
        return (
            0 <= self.MMSI <= 999999999 and
            -90 <= self.latitude <= 90 and
            -180 <= self.longitude <= 180
        )

    def is_valid(self) -> bool:
        return 0 <= self.MessageID <= 31 and 0 <= self.RepeatIndicator <= 3 and 0 <= self.UserID <= 999999 and self.Valid is True

@dataclass
class PositionReport:
    SubscribeMessageID: int
    MessageType: int
    Cog: float
    CommunicationState: int
    Latitude: float
    Longitude: float
    MessageID: int
    NavigationalStatus: int
    PositionAccuracy: bool
    Raim: bool
    RateOfTurn: int
    RepeatIndicator: int
    Sog: float
    Spare: int
    SpecialManoeuvreIndicator: int
    Timestamp: datetime  # Assuming Timestamp is a datetime object
    TrueHeading: int
    UserID: int
    Valid: bool
    MMSI: int
    MMSI_String: str  # Assuming MetaData.MMSI_String maps to this
    ShipName: str
    MetaData_latitude: float  # Assuming MetaData.latitude maps to this
    MetaData_longitude: float  # Assuming MetaData.longitude maps to this
    TimeUtc: datetime  # Assuming TimeUtc is a datetime object
    Geom: Geometry  # Assuming Geom is a geometry type from GeoAlchemy2
    ShipCommonDataID: uuid.UUID
    

    def is_valid(self) -> bool:
        r=(
            0 <= self.Cog <= 360 or self.Cog == 3600 and
            0 <= self.CommunicationState <= 419340 and
            -90 <= self.Latitude <= 90 and
            -180 <= self.Longitude <= 180 and
            self.MessageID in [1, 2, 3] and
            0 <= self.NavigationalStatus <= 15 and
            -128 <= self.RateOfTurn <= 127 and
            0 <= self.RepeatIndicator <= 3 and
            0 <= self.Sog <= 102.2 and
            0 <= self.Spare <= 1 and
            0 <= self.SpecialManoeuvreIndicator <= 1 and
            0 <= self.Timestamp <= 59 and  # Validate this condition if Timestamp is a datetime
            1 <= self.MessageType <= 3 and
            (0 <= self.TrueHeading < 360 or self.TrueHeading == 511)
        )
        if not r:
            raise Exception("Invalid PositionReport")
        return r
            

@dataclass
class StandardClassBPositionReport:
    MessageType: int
    AssignedMode: bool
    ClassBBand: bool
    ClassBDisplay: bool
    ClassBDsc: bool
    ClassBMsg22: bool
    ClassBUnit: bool
    Cog: float
    CommunicationState: int
    CommunicationStateIsItdma: bool
    Latitude: float  # Renamed from Message.StandardClassBPositionReport.Latitude
    Longitude: float  # Renamed from Message.StandardClassBPositionReport.Longitude
    MessageID: int
    PositionAccuracy: bool
    Raim: bool
    RepeatIndicator: int
    Sog: float
    Spare1: int
    Spare2: int
    Timestamp: datetime
    TrueHeading: int
    UserID: int  # Renamed from Message.StandardClassBPositionReport.UserID
    Valid: bool
    MMSI: int
    MMSI_String: str  # Renamed from MetaData.MMSI_String
    ShipName: str
    MetaData_latitude: float  # Renamed from MetaData.latitude
    MetaData_longitude: float  # Renamed from MetaData.longitude
    TimeUtc: datetime
    Geom: Geometry
    ShipCommonDataID: uuid.UUID
    SubscribeMessageID: int

    def is_valid(self) -> bool:
        return (
            0 <= self.Cog < 360 or self.Cog == 3600 and
            0 <= self.CommunicationState <= 419340 and
            -90 <= self.Latitude <= 90 and
            -180 <= self.Longitude <= 180 and
            self.MessageID == 18 and  # Assuming MessageID must be exactly 18
            0 <= self.RepeatIndicator <= 3 and
            0 <= self.Sog <= 102.2 and
            (isinstance(self.Timestamp, datetime) and self.Timestamp.year >= 2020) and  # Check if Timestamp is a datetime object and year is reasonable
            1 <= self.MessageType <= 3 and
            (0 <= self.TrueHeading < 360 or self.TrueHeading == 511) and
            isinstance(self.UserID, int) and  # Ensure UserID is an integer
            isinstance(self.Valid, bool) and  # Ensure Valid is a boolean
            isinstance(self.MMSI, int) and  # Ensure MMSI is an integer
            isinstance(self.ShipName, str) and  # Ensure ShipName is a string
            (-90 <= self.MetaData_latitude <= 90) and  # Ensure MetaData_latitude is within valid latitude range
            (-180 <= self.MetaData_longitude <= 180) and  # Ensure MetaData_longitude is within valid longitude range
            isinstance(self.TimeUtc, datetime) and  # Check if TimeUtc is a datetime object
            isinstance(self.ShipCommonDataID, uuid.UUID) and  # Check if ShipCommonDataID is a UUID object
            (self.AssignedMode in [True, False]) and  # Ensure AssignedMode is a boolean
            (self.ClassBBand in [True, False]) and  # Ensure ClassBBand is a boolean
            (self.ClassBDisplay in [True, False]) and  # Ensure ClassBDisplay is a boolean
            (self.ClassBDsc in [True, False]) and  # Ensure ClassBDsc is a boolean
            (self.ClassBMsg22 in [True, False]) and  # Ensure ClassBMsg22 is a boolean
            (self.ClassBUnit in [True, False]) and  # Ensure ClassBUnit is a boolean
            (self.PositionAccuracy in [True, False]) and  # Ensure PositionAccuracy is a boolean
            (self.Raim in [True, False])  # Ensure Raim is a boolean
        )


@dataclass
class ShipStaticData:
    MessageType: int
    AisVersion: int
    CallSign: str
    Destination: str
    Dimension: Dimension
    Dte: bool
    Eta: Eta
    FixType: int
    ImoNumber: Optional[int]
    MaximumStaticDraught: float
    MessageID: int
    Name: str
    RepeatIndicator: int
    Spare: bool
    ShipType: int  # Assuming 'ShipType' corresponds to 'Type'
    UserID: int  # Renamed from 'Message.ShipStaticData.UserID'
    Valid: bool
    MMSI: int
    MMSI_String: str  # Assuming 'MetaData.MMSI_String' maps to this
    ShipName: str  # Assuming 'ShipName' is the same as 'Name'
    MetaData_latitude: float  # Assuming 'MetaData.latitude' maps to this
    MetaData_longitude: float  # Assuming 'MetaData.longitude' maps to this
    TimeUtc: datetime
    Geom: Geometry
    ShipCommonDataID: uuid.UUID
    SubscribeMessageID: int
    def is_valid(self) -> bool:
        return (
            self.AisVersion in [0, 1, 2, 3] and
            self.Dimension.is_valid() and
            self.FixType in [0, 1, 2, 3, 15] and  # Adjusted to include '15' based on your data
            (self.ImoNumber is None or 1000000 <= self.ImoNumber <= 9999999) and
            0 <= self.MaximumStaticDraught <= 25.5 and
            self.MessageID == 5 and
            len(self.Name.strip()) <= 20 and
            0 <= self.RepeatIndicator <= 3 and
            self.Spare is False and
            0 <= self.ShipType <= 99 and
            self.Valid is True and
            self.Eta.is_valid()
        )

    

@dataclass
class ReportA:
    Name: str
    Valid: bool
    def is_valid(self) -> bool:
        # Example validation for ReportA
        return len(self.Name) <= 20 and self.Valid is True

@dataclass
class ReportB:
    CallSign: Optional[str]
    Dimension: Optional[Dimension]
    FixType: int
    ShipType: int
    Spare: int
    VenderIDModel: int
    VenderIDSerial: int
    VendorIDName: str
    Valid: bool

    def is_valid(self) -> bool:
        # Example validation for ReportB
        dimension_valid = self.Dimension.is_valid() if self.Dimension else True
        return (
            (self.CallSign is None or len(self.CallSign) <= 7) and
            dimension_valid and
            0 <= self.FixType <= 3 and
            0 <= self.ShipType <= 99 and
            0 <= self.VenderIDModel <= 99 and
            self.Valid is True
        )

@dataclass
class StaticDataReport:
    MessageID: int
    PartNumber: bool
    RepeatIndicator: int
    ReportA: Optional[ReportA]
    ReportB: Optional[ReportB]
    Reserved: int
    UserID: int
    Valid: bool

    def is_valid(self) -> bool:
        return (
            self.MessageID == 24 and
            0 <= self.RepeatIndicator <= 3 and
            (self.ReportA is not None or self.ReportB is not None) and
            (self.ReportA.is_valid() if self.ReportA is not None else True) and
            (self.ReportB.is_valid() if self.ReportB is not None else True)
        )
