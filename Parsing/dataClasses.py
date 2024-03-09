from dataclasses import dataclass
from typing import Optional, Union

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
class PositionReport:
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
    Timestamp: int
    TrueHeading: int
    UserID: int
    Valid: bool

    def is_valid(self) -> bool:
        return (
            0 <= self.Cog < 360 or self.Cog == 3600 and
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
            0 <= self.Timestamp <= 59 and
            (0 <= self.TrueHeading < 360 or self.TrueHeading == 511)
        )

@dataclass
class StandardClassBPositionReport:
    AssignedMode: bool
    ClassBBand: bool
    ClassBDisplay: bool
    ClassBDsc: bool
    ClassBMsg22: bool
    ClassBUnit: bool
    Cog: float
    CommunicationState: int
    CommunicationStateIsItdma: bool
    Latitude: float
    Longitude: float
    MessageID: int
    PositionAccuracy: bool
    Raim: bool
    RepeatIndicator: int
    Sog: float
    Spare1: int
    Spare2: int
    Timestamp: int
    TrueHeading: int
    UserID: int
    Valid: bool

    def is_valid(self) -> bool:
        return (
            0 <= self.Cog < 360 or self.Cog == 3600 and
            0 <= self.CommunicationState <= 419340 and
            -90 <= self.Latitude <= 90 and
            -180 <= self.Longitude <= 180 and
            self.MessageID == 18 and
            0 <= self.RepeatIndicator <= 3 and
            0 <= self.Sog <= 102.2 and
            0 <= self.Timestamp <= 59 and
            (0 <= self.TrueHeading < 360 or self.TrueHeading == 511)
        )


@dataclass
class ShipStaticData:
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
    Type: int
    UserID: int
    Valid: bool

    def is_valid(self) -> bool:
        return (
            self.AisVersion in [0, 1, 2, 3] and
            len(self.CallSign.strip()) <= 7 and
            len(self.Destination.strip()) <= 20 and
            self.Dimension.is_valid() and
            self.FixType in [0, 1, 2, 3] and
            (self.ImoNumber is None or 1000000 <= self.ImoNumber <= 9999999) and
            0 <= self.MaximumStaticDraught <= 25.5 and
            self.MessageID == 5 and
            len(self.Name.strip()) <= 20 and
            0 <= self.RepeatIndicator <= 3 and
            self.Spare is False and
            0 <= self.Type <= 99 and
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
