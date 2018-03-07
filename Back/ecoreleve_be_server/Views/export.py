from sqlalchemy import select, join, exists, func
import json
import pandas as pd
from ..Models import BaseExport, Project, Observation, Station, Base
from ..utils.generator import Generator
from ..renderers import CSVRenderer, PDFrenderer, GPXRenderer
from pyramid.response import Response
import io
from datetime import datetime
from ..Views import CustomView
from ..controllers.security import RootCore
from ..GenericObjets.SearchEngine import DynamicPropertiesQueryEngine, QueryEngine


ProcoleType = Observation.TypeClass

# class ObservationCollection(DynamicPropertiesQueryEngine):
#     pass
    
class ObservationCollection(DynamicPropertiesQueryEngine):

    def __init__(self, session, object_type=None, from_history=None):
        DynamicPropertiesQueryEngine.__init__(self, session=session, model=Observation, object_type=object_type, from_history=from_history)

    def _select_from(self):
        table_join = DynamicPropertiesQueryEngine._select_from(self)
        table_join = join(table_join, Station, Station.ID == Observation.FK_Station)

        station_columns = [
            Station.Name.label('Station_Name'),
            Station.LAT.label('Station_Latitude'),
            Station.LON.label('Station_Longitude'),
            Station.StationDate.label('Station_Date')
        ]
        self.selectable.extend(station_columns)
        return table_join
    
    def get_column_by_name(self, column_name):
        try :
            column = DynamicPropertiesQueryEngine.get_column_by_name(self, column_name)
        except:
            column = getattr(Station, column_name, None)
        return column


class CustomExportView(CustomView):

    def __init__(self, ref, parent):
        CustomView.__init__(self, ref, parent)
        try:
            self.session = self.request.registry.dbmakerExport
        except:
            ''' occures when DB export is not loaded, see development.ini :: loadDBExport '''
            pass


class ExportObservationProjectView(CustomExportView):

    item = None

    def __init__(self, ref, parent):
        CustomExportView.__init__(self, ref, parent)
        self.actions = {'getFields': self.getFields,
                        'getFilters': self.getFilters,
                        'count': self.count_,
                        'csv': self.export_csv,
                        'pdf': self.export_pdf,
                        'gpx': self.export_gpx,
                        'excel': self.export_excel,
                        'getFile': self.getFile
                        }
        self.type_obj = self.request.params.get('protocolType', None)
        self.CollectionEngine = ObservationCollection(session=self.session, object_type=self.type_obj)

    def retrieve(self):
        return self.search()

    def getFields(self):
        return self.generator.get_col()

    def getFilters(self):
        return self.generator.get_filters()

    def count_(self):
        data = self.request.params.mixed()
        if 'criteria' in data:
            criteria = json.loads(data['criteria'])
        else:
            criteria = {}
        count = self.generator.count_(criteria)
        return count

    def search(self):
        filters = [
            {'Column':'FK_Project','Operator':'=', 'Value':self.parent.id_},
        ]
        params = self.request.params.mixed()
        if 'criteria' in params:
            filters.extend(json.loads(params['criteria']))

        query = self.CollectionEngine.build_query(filters=filters)
        return self.session.execute(query).fetchall()

    def formatColumns(self, fileType, columns):
        queryColumns = []
        if fileType != 'gpx':
            for col in columns:
                queryColumns.append(self.table.c[col])
        else:
            splittedColumnLower = {c.name.lower().replace(
                '_', ''): c.name for c in self.table.c}
            queryColumns = [self.table.c[splittedColumnLower['lat']].label(
                'LAT'), self.table.c[splittedColumnLower['lon']].label('LON')]

            if 'stationname' in splittedColumnLower:
                queryColumns.append(self.table.c[splittedColumnLower[
                            'stationname']].label('SiteName'))
            elif 'name' in splittedColumnLower:
                queryColumns.append(self.table.c[splittedColumnLower[
                            'name']].label('SiteName'))
            elif 'sitename' in splittedColumnLower:
                queryColumns.append(self.table.c[splittedColumnLower[
                            'sitename']].label('SiteName'))
            if 'date' in splittedColumnLower:
                queryColumns.append(self.table.c[splittedColumnLower['date']].label('Date'))
        return queryColumns

    def getFile(self):
        params = self.request.params.mixed()
        # criteria = json.loads(params['criteria'])
        fileType = self.request.params.get('fileType', None)

        rows = self.search()
        protocol_name = self.session.query(ProcoleType).get(self.type_obj).Name
        project_name = self.session.query(Project).get(self.parent.id_).Name

        self.filename = project_name + '_'+ protocol_name + '_'
        self.request.response.content_disposition = 'attachment;filename=' + self.filename

        columns = rows[0].keys()
        value = {'header': columns, 'rows': rows}

        io_export = self.actions[fileType](value)
        return io_export

    # def getFile(self):
    #     try:
    #         criteria = json.loads(self.request.params.mixed()['criteria'])
    #         fileType = criteria['fileType']
    #         # columns selection
    #         columns = criteria['columns']

    #         queryColumns = self.formatColumns(fileType, columns)

    #         query = self.generator.getFullQuery(criteria['filters'], columnsList=queryColumns)
    #         rows = self.session.execute(query).fetchall()

    #         filename = self.viewName + '.' + fileType
    #         self.request.response.content_disposition = 'attachment;filename=' + filename
    #         value = {'header': columns, 'rows': rows}

    #         io_export = self.actions[fileType](value)
    #         return io_export

    #     except:
    #         raise

    def export_csv(self, value):
        csvRender = CSVRenderer()
        csv = csvRender(value, {'request': self.request})
        return Response(csv)

    def export_pdf(self, value):
        pdfRender = PDFrenderer()
        pdf = pdfRender(value, self.viewName, self.request)
        return Response(pdf)

    def export_gpx(self, value):
        gpxRender = GPXRenderer()
        gpx = gpxRender(value, self.request)
        return Response(gpx)

    def export_excel(self, value):
        df = pd.DataFrame(data=value['rows'], columns=value['header'])

        fout = io.BytesIO()
        writer = pd.ExcelWriter(fout)
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.save()
        file = fout.getvalue()

        dt = datetime.now().strftime('%d-%m-%Y')
        return Response(
            file,
            content_disposition="attachment; filename="
            + self.filename + dt + ".xlsx",
            content_type='application/vnd.openxmlformats-\
            officedocument.spreadsheetml.sheet')


class ExportProtocoleTypeView(CustomExportView):

    item = ExportObservationProjectView

    def __init__(self, ref, parent):
        CustomExportView.__init__(self, ref, parent)
        self.actions = {'getFields': self.getFields,
                        'getFilters': self.getFilters
        }

    def retrieve(self):
        query = select([ProcoleType])

        table_join = join(Station, Observation, Station.ID == Observation.FK_Station)
        subQuery = select([Observation]).select_from(table_join).where(Station.FK_Project==self.parent.id_)

        ## Observation.fk_table_type_name point to FK_ProtocoleType
        subQuery = subQuery.where(ProcoleType.ID== Observation.type_id)
        query = query.where(exists(subQuery))
        result = [dict(row) for row in self.session.execute(query).fetchall()]

        return result

    def getFilters(self):
        return None

    def getFields(self):
        # table = Base.metadata.tables['Observation']
        return None

    # def get_col_observation(self):
    #     for col in table.c:
    #         field_name=col.name
    #         field_label=col.name
    #         field_type=self.table.c[col.name].type
    #         if field_type in self.dictCell:
    #             cell_type=self.dictCell[field_type]
    #             cell_type='string'
                
    #         else:
    #             cell_type='string'

    #         final.append({'field':field_name,
    #             'headerName':field_label,
    #             'cell':cell_type,
    #             'editable':False})
    #         self.cols.append({'name':field_name,'type_grid':cell_type})


    #     cols = [{'field':field_name,
    #             'headerName':field_label,
    #             'cell':cell_type,
    #             'editable':False}
    #             ]
    #     return final


class ExportProjectView(CustomExportView):

    item = None

    def __init__(self, ref, parent):
        CustomExportView.__init__(self, ref, parent)
        self.add_child('protocols', ExportProtocoleTypeView)
        self.add_child('observations', ExportObservationProjectView)
        self.id_ = ref

    def retrieve(self):
        query = select([func.count(Station.ID)]).where(Station.FK_Project== self.id_)
        result = self.session.execute(query).scalar()
        return {'nb stations': result}

    def __getitem__(self, item):
        return self.get(item)


class ExportCollectionProjectView(CustomExportView):

    item = ExportProjectView
    def retrieve(self):
        query = select([Project]).order_by(Project.Name.asc())
        result = [dict(row) for row in self.session.execute(query).fetchall()]
        return result

class ExportCoreView(CustomExportView):

    item = None

    def __init__(self, ref, parent):
        CustomExportView.__init__(self, ref, parent)
        self.add_child('projects', ExportCollectionProjectView)

    def __getitem__(self, item):
        return self.get(item)

    def retrieve(self):
        return {'next items': 'views'
                }


RootCore.listChildren.append(('export', ExportCoreView))