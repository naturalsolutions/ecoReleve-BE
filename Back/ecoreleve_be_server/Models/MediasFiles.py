from sqlalchemy import Column, Integer, Sequence, String, DateTime, func, ForeignKey
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import relationship
from ..Models import Base


class MediasFiles(Base):

    __tablename__ = 'MediasFiles'
    Id = Column(Integer, Sequence('MediasFiles__id_seq'), primary_key=True)
    Path = Column(String(250), nullable=False, unique=True)
    Name = Column(String(250), nullable=False)
    Extension = Column(String(4), nullable=False)
    Date_Uploaded = Column(DateTime, server_default = func.now(), nullable=False)
    Creator = Column(Integer, nullable=False)
    FK_Observation = Column(Integer, ForeignKey('Observation.ID'), nullable=True)

    Observation = relationship("Observation")
    
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]

