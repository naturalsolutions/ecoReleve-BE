# from ..Models import Base, dbConfig
# from sqlalchemy import (
#     Column,
#     DateTime,
#     ForeignKey,
#     Integer,
#     Numeric,
#     String,
#     Unicode,
#     text,
#     Sequence,
#     orm,
#     func,
#     select,
#     bindparam,
#     UniqueConstraint,
#     event)
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.hybrid import hybrid_property
# # from ..GenericObjets.DataBaseObjects import ConfiguredDbObjectMapped, DbObject
# from ..GenericObjets.OrmModelsMixin import HasStaticProperties
# from ..Models import Base, dbConfig
# from urllib.parse import quote_plus

# sensor_schema = dbConfig['sensor_schema']
# dialect = dbConfig['cn.dialect']


# class Import(HasStaticProperties, Base):
#     __tablename__ = 'Import'
#     moduleGridName = 'ImportHistoryFilter'

#     # TempTable_GUID = Column(String(250), default=None)
#     # Status = Column(Integer)
#     # ObjectName = Column(String(250))
#     # ObjectType = Column(String(250))
#     # FK_ImportType = Column(Integer, ForeignKey(
#     #     'ImportType.ID'), nullable=False)

#     # __table_args__ = ({'schema': sensor_schema,
#     #                    'implicit_returning': False
#     #                    })
#     ID = Column(Integer, Sequence('Import__id_seq'), primary_key=True)
#     GPXrawDatas = relationship('GPX', back_populates='ImportedFile')
#     ArgosGPSRawDatas = relationship('ArgosGps', back_populates='ImportedFile')
#     ArgosEngRawDatas = relationship(
#         'ArgosEngineering', back_populates='ImportedFile')
#     RFIDrawDatas = relationship('Rfid', back_populates='ImportedFile')
#     GSMrawDatas = relationship('Gsm', back_populates='ImportedFile')
#     GSMengRawDatas = relationship(
#         'GsmEngineering', back_populates='ImportedFile')

#     @hybrid_property
#     def relatedDatas(self):
#         dictType = {
#             'GPX': self.GPXrawDatas,
#             'Argos': self.ArgosGPSRawDatas,
#             'GSM': self.GSMrawDatas,
#             'RFID': self.RFIDrawDatas
#         }
#         return dictType.get(self.ImportType)

#     __table_args__ = ({'schema': quote_plus('"ecoreleve_sensor".')+quote_plus('"public"'),
#                     'implicit_returning': False
#                     })

#     # @hybrid_property
#     # def maxDate(self):
#     #     return max(row.date for row in self.relatedDatas)

#     # @hybrid_property
#     # def minDate(self):
#     #     return min(row.date for row in self.relatedDatas)

#     # @hybrid_property
#     # def nbRow(self):
#     #     return len(self.relatedDatas)


# # class ImportType(Base):

# #     __tablename__ = 'ImportType'
# #     ID = Column(Integer, primary_key=True)
# #     Name = Column(String(250))

# #     __table_args__ = ({'schema': sensor_schema,
# #                         'implicit_returning': False
# #                        })
