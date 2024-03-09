from . import *
from . import Base

class SPGlobalShipDetails(Base):
    __tablename__ = 'spglobalshipdetails'
    SPGlobalShipDetailsID = Column(Integer, primary_key=True, autoincrement=True)
    ImoNumber = Column(Integer)
    ShipName = Column(String(255))
    MMSI = Column(Integer)
    Displacement = Column(Integer)
    BreadthExtreme = Column(Float)
    BreadthMoulded = Column(Float)
    LengthBP = Column(Float)
    LengthRegistered = Column(Float)
    TotalKWMainEng = Column(Float)
    
    idx_spglobalshipdetails_imo_number = Index('idx_spglobalshipdetails_imo_number', ImoNumber)
    idx_spglobalshipdetails_mmsi = Index('idx_spglobalshipdetails_mmsi', MMSI)
