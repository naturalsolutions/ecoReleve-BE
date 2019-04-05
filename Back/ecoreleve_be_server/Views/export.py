from sqlalchemy import select, join, exists, func, and_, text, or_, outerjoin
from sqlalchemy.types import TIMESTAMP
import json
import pandas as pd
from ..Models import BaseExport, Project, Observation, Station, ModuleForms, FrontModules, Base, User, Client, Project
from ..utils.generator import Generator
from ..renderers import CSVRenderer, PDFrenderer, GPXRenderer
from pyramid.response import Response
import io
from datetime import datetime
from ..Views import CustomView
from ..controllers.security import RootCore
from ..GenericObjets.SearchEngine import Query_engine
from traceback import print_exc
import uuid
from geoalchemy2.shape import to_shape

ProcoleType = Observation.TypeClass

# class ObservationCollection(DynamicPropertiesQueryEngine):
#     pass

@Query_engine(Observation)
class ObservationCollection():

     def extend_from(self, _from):
        station_columns = [
            Station.Name,
            Station.LAT,
            Station.LON,
            Station.StationDate,
            Station.creator,
            Station.ELE
            ]
        observation_columns = [
            Observation.ID.label('observation_id'),
            Observation.trace
        ]

        project_columns = [
            Project.Name.label('Projet')
        ]

        self.selectable.extend(station_columns)



        join_table = outerjoin(_from, Station,Observation.FK_Station == Station.ID)
        join_table = outerjoin( join_table, User, Station.creator == User.id) 
        join_table = outerjoin(join_table, Project, Station.FK_Project == Project.ID)
        join_table = outerjoin(join_table, Client, Project.FK_Client == Client.ID)
        self.fk_join_list.append(Station.__table__)
        self.selectable.extend(station_columns)
        self.selectable.extend(observation_columns)
        self.selectable.extend(project_columns)
        
        # self.selectable.extend([User.Lastname,
        #                         User.Firstname,
        #                         Client.Name.label('ClientName')])

        # join_table = outerjoin(_from, )
        return join_table


@Query_engine(Observation)
class SinpObservationCollection():

     def extend_from(self, _from):
        station_columns = [
            # Station.Name,
            Station.LAT,
            Station.LON,
            Station.StationDate,
            Station.creator
            ]
        observation_columns = [
            Observation.ID.label('observation_id')
        ]
        Taxref = Base.metadata.tables['TAXREF']
        # taxref_id_column = self.get_column_by_name('taxref_id')
        # join_table = outerjoin(_from, Taxref, taxref_id_column == Taxref.c['CD_NOM'])
        join_table = outerjoin(_from, Station, Observation.FK_Station == Station.ID)
        join_table = outerjoin(join_table, User, Station.creator == User.id)
        join_table = outerjoin(join_table, Project, Station.FK_Project == Project.ID)
        join_table = outerjoin(join_table, Client, Project.FK_Client == Client.ID)
        self.fk_join_list.append(Station.__table__)
        self.selectable.extend(station_columns)
        self.selectable.extend(observation_columns)
        self.selectable.extend([User.Lastname,
                                User.Firstname,
                                Client.Name.label('ClientName')])
        print(self.selectable)
        return join_table


class CustomExportView(CustomView):

    chidlren = []

    def __init__(self, ref, parent):
        CustomView.__init__(self, ref, parent)
        try:
            self.session = self.request.registry.dbmakerExport
        except:
            ''' occures when DB export is not loaded, see development.ini :: loadDBExport '''
            pass


class ExportObservationProjectView(CustomExportView):

    item = None
    moduleFormName = 'ObservationForm'
    chidlren = []

    def __init__(self, ref, parent):
        CustomExportView.__init__(self, ref, parent)
        self.actions = {'getFields': self.getFields,
                        'getFilters': self.getFilters,
                        'count': self.count_,
                        'csv': self.export_csv,
                        'pdf': self.export_pdf,
                        'gpx': self.export_gpx,
                        'excel': self.export_excel,
                        'getFile': self.getFile,
                        'sinp': self.export_sinp
                        }
        self.type_obj = self.request.params.get('protocolType', None)
        if not self.type_obj:
            self.type_obj = self.request.params.get('typeObj', self.request.params.get('objectType',None))
        self.CollectionEngine = ObservationCollection(session=self.session, object_type=self.type_obj)

    def format_result(self,result):
        response = []
        for row in result:
            tempdict = {}
            listKeys = list(row.keys())
            # listKeysOrdered.sort()
            listKeysSorted = sorted(listKeys, key=lambda s: s.lower())
            # for col, value in row.items().sort():
            for item in listKeysSorted:
                if isinstance(row._keymap[item][1][0].type,TIMESTAMP):
                    tempdict[item] = row[item].strftime('%H:%M:%S')
                if item == 'trace' and row[item] is not None:
                    tempdict[item] = to_shape(row[item]).to_wkt()
                else:
                    tempdict[item] = row[item]
            response.append(tempdict)
        return listKeysSorted,response


    def retrieve(self):
        if self.request.params.get('geo', None):
            return self.get_geoJSON(geoJson_properties=['taxon'])
        result = self.search()
        _ , response = self.format_result(result)

        return response

    def get_geoJSON(self,geoJson_properties = None) :
        result=[]
        total=None
        countResult = self.count_()

        exceed = None
        geoJson=[]

        if countResult <= 100000 :
            exceed = True
            return {'type':'FeatureCollection', 'features': geoJson,'exceed': exceed, 'total':countResult}
            try :
                data=self.search()
            except :
                print_exc()
            for row in data:
                properties = {}
                if geoJson_properties != None :
                    for col in geoJson_properties :
                        properties[col] = row[col]
                if row['LAT'] and row['LON']:
                    geoJson.append({'type':'Feature',
                                    'properties':properties,
                                    'geometry':
                                        {'type':'Point',
                                        'coordinates':[row['LAT'],row['LON']]
                                        }
                                    })
        else :
            exceed = True
        return {'type':'FeatureCollection', 'features': geoJson,'exceed': exceed, 'total':countResult}

    def count_(self):
        data = self.request.params.mixed()
        filters = [
            {'Column':'Station@FK_Project','Operator':'=', 'Value':self.parent.id_},
        ]
        if 'criteria' in data:
            filters.extend(json.loads(data['criteria']))

        count = self.CollectionEngine._count(filters=filters)
        return count

    def search(self, selectable=[]):
        filters = [
            {'Column':'Station@FK_Project','Operator':'=', 'Value':self.parent.id_},
        ]
        params = self.request.params.mixed()
        if 'criteria' in params:
            filters.extend(json.loads(params['criteria']))

        if len(selectable) == 0:
            selectable = self.getFieldsWithPrefix()

        query = self.CollectionEngine.build_query(filters=filters, selectable=selectable)
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
        criteria = json.loads(params['criteria'])
        fileType = self.request.params.get('fileType', None)
        columns = json.loads(params['columns'])
        
        columns = self.getFieldsWithPrefix()
        columnsSorted = sorted(columns, key=lambda s: s.lower())
        result = self.search(selectable = columnsSorted)

        columnsSorted,rows = self.format_result(result)
        protocol_name = self.session.query(ProcoleType).get(self.type_obj).Name
        project_name = self.session.query(Project).get(self.parent.id_).Name

        self.filename = project_name + '_'+ protocol_name + '_'
        self.request.response.content_disposition = 'attachment;filename=' + self.filename

        value = {'header': columnsSorted, 'rows': rows}

        io_export = self.actions[fileType](value)
        return io_export

    def getConf(self, moduleName=None):
        if not moduleName:
            moduleName = self.moduleFormName
        frontModule = self.session.query(FrontModules
                                  ).filter(FrontModules.Name == moduleName
                                           ).first()
        return frontModule

    def getForm(self):
        project_fields = self.session.query(ModuleForms
                                    ).filter(ModuleForms.Module_ID == self.getConf('ProjectForm').ID
                                    ).filter(ModuleForms.Name.in_(['Name'])).all()

        observation_fields = self.session.query(ModuleForms
                                    ).filter(
            and_(ModuleForms.Module_ID == self.getConf().ID,
                 or_(ModuleForms.TypeObj == self.type_obj, ModuleForms.TypeObj == None))).order_by(ModuleForms.FormOrder).all()

        station_fields = self.session.query(ModuleForms
                                    ).filter(ModuleForms.Module_ID == self.getConf('StationForm').ID
                                    ).filter(or_(ModuleForms.TypeObj == 1, ModuleForms.TypeObj == None)
                                    # ).filter(ModuleForms.TypeObj.in_(['1', None])
                                    ).filter(~ModuleForms.Name.in_(['ID', 'FK_Project'])
                                    ).order_by(ModuleForms.FormOrder).all()

        all_fields = [field for field in station_fields]
        for field in observation_fields:
            all_fields.append(field)

        return all_fields

    def getFields(self):
        all_fields = self.getForm()
        column_fields = []

        for field in all_fields:
            column = {
                'field': field.Name,
                'headerName': field.Label,
                'editable': False,
                'cell': 'string',
            }
            column_fields.append(column)
        return column_fields
    
    def getFieldsWithPrefix(self):
        all_fields = self.getForm()
        column_fields = []

        prefix= ['','','Station@']
        for field in all_fields:
            colAlliased = getattr(field,'Name')
            # if getattr(field,'Module_ID') == 2:
            #     colAlliased = prefix[2]+colAlliased
            column_fields.append(colAlliased)
        return column_fields

    def getFilters(self):
        all_fields = self.getForm()
        filters = []
        for field in all_fields:
            filters.append(self.GenerateFilter(field))

        return filters

    def GenerateFilter(self, field):
        ''' return filter field to build Filter '''
        prefix = ''
        if field.Module_ID == 2:
            prefix = 'Station@'
        if field.Module_ID == 5:
            prefix = 'Project@'
        filter_ = {
            'name': prefix+field.Name,
            'type': field.InputType,
            'label': field.Label,
            'title': field.Label,
            'editable': True,
            'validators': [],
            'options': [],
        }

        try:
            filter_['options'] = json.loads(field.Options)
        except:
            filter_['options'] = field.Options

        if field.InputType == 'Select' and field.Options is not None and 'select' in field.Options.lower():
            result = self.session.execute(text(field.Options)).fetchall()
            filter_['options'] = [
                {'label': row['label'], 'val':row['val']} for row in result]

        if field.InputType == 'Checkboxes':
            filter_['options'] = [
                {'label': 'True', 'val': 1}, {'label': 'False', 'val': 0}]

        if (field.InputType == 'TaxRefEditor'):
            if( field.Options is not None and field.Options != ''):
                option = json.loads(field.Options)
                filter_['options'] = filter_['options']
                filter_['options']['iconFont'] = 'reneco reneco-autocomplete'
            elif( field.Options is None or field.Options == '' ) :
                typeObj_dbView = {
                    1:'oiseau',
                    3:'reptile',
                    4:'mammal',
                    5:'chiroptera',
                    6:'flore',
                    7:'insecte'
                }
                try:
                    valObj = int(self.type_obj)
                except:
                    valObj = None
                dbViewStr = typeObj_dbView.get(valObj)
                if dbViewStr :
                    filter_['options'] = { 
                        "type" : "vernaculaire",
                        "taxaList" : dbViewStr,
                        "vernaStrict" : True
                    }

        return filter_

    def export_csv(self, value):
        # df = pd.DataFrame(data=value['rows'], columns=value['header'])
        df = pd.DataFrame.from_records(value['rows'],
                                       columns=value['header'],
                                       coerce_float=True)

        # fout = io.BytesIO()
        # writer = pd.ExcelWriter(fout)
        # df.to_excel(writer, sheet_name='Sheet1', index=False)
        # writer.save()
        # file = fout.getvalue()
        fout = io.StringIO()
        file = df.to_csv(sep=';',index=False)
        dt = datetime.now().strftime('%d-%m-%Y')
        return Response(
            file,
            content_disposition="attachment; filename="
            + self.filename + dt + ".csv",
            content_type='text/csv')
    

    def export_pdf(self, value):
        pdfRender = PDFrenderer()
        pdf = pdfRender(value, self.viewName, self.request)
        return Response(pdf)

    def export_gpx(self, value):
        gpxRender = GPXRenderer()
        gpx = gpxRender(value, self.request)
        return Response(gpx)

    def export_excel(self, value):
        # df = pd.DataFrame(data=value['rows'], columns=value['header'])
        df = pd.DataFrame.from_records(value['rows'],
                                       columns=value['header'],
                                       coerce_float=True)

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

    def export_sinp(self, value):
        params = self.request.params.mixed()
        # rows = self.search()
        filters = [
            {'Column':'Station@FK_Project','Operator':'=', 'Value':self.parent.id_},
        ]

        CollectionEngine = SinpObservationCollection(session=self.session, object_type=self.type_obj)
        query = CollectionEngine.build_query(selectable=['taxref_id', 'type_inventaire', 'taxon','nom_vernaculaire'], filters=filters)
        
        protocol_name = self.session.query(ProcoleType).get(self.type_obj).Name
        project_name = self.session.query(Project).get(self.parent.id_).Name
        dataframe = pd.read_sql(query, self.session.get_bind())
        required_columns = [
            'statObs', #default value = "Pr"
            'nomCite', #nom complet taxon 
            'cdNom',
            'cdRef',
            # 'datedet', #date de determination definitive du taxon
            'dateDebut',
            'dateFin',
            'dSPublique', #default value = "Pr" (privé)
            'orgGestDat', # normallement nom bureau d'étude, correspond à l'organisme qui gére et détient la donnée d'origine et qui en a la responsabilité ??? client de l'etude ?? 
            'statSource', #type d'observation => terrain , default value = "Te"
            'WKT', #Point, polygon ...
            'natObjGeo', #default value = "St", si polygon => "In"
            'obsNomOrg', #nom de l'organisme ayant effectué l'observation
            'obsId', #nom de l'observateur, s'il ne veut pas etre renseigné mettre "ANONYME", format : NOM Prenom
            'permId' #identifiant permanent de notre coté de l'app (id de l'observation)
        ]

        recommanded_columns = [
            # 'ocMethDet', ## correspondra au type d'inventaire fourni par le bureau d'étude
        ]

        point_wkt = 'POINT({LONG} {LAT})'
        out_dataframe = pd.DataFrame(columns=required_columns.extend(recommanded_columns))

        out_dataframe['dateDebut'] = dataframe['StationDate'].apply(lambda x: x.strftime("%d/%m/%Y"))
        out_dataframe['dateFin'] = dataframe['StationDate'].apply(lambda x: x.strftime("%d/%m/%Y"))
        out_dataframe['dSPublique'] = 'Pr'
        out_dataframe['natObjGeo'] = 'St'
        out_dataframe['nomCite'] = dataframe['nom_vernaculaire'].dropna().apply(lambda x : x) #dataframe['taxon'].dropna().apply(lambda x : x)
        out_dataframe['obsId'] = dataframe[['Lastname','Firstname']].apply(lambda r: self.without_accent(r[0],True) + self.without_accent(r[1],title=True) or 'Inconnu', axis=1)
        out_dataframe['obsNomOrg'] = self.without_accent('INCONNU')
        out_dataframe['orgGestDat'] = dataframe['ClientName'].apply(lambda x: self.without_accent(x) or 'Inconnu')
        out_dataframe['WKT'] = dataframe[['LON', 'LAT']].apply(lambda r : point_wkt.format(LONG=r[0], LAT=r[1]), axis=1)
        out_dataframe['statObs'] = 'Pr'
        out_dataframe['statSource'] = 'Te'
        out_dataframe['cdNom'] = dataframe['taxref_id'].apply(lambda x: int(x) if x == x else "") #.fillna(0.0).astype(int) #.apply(lambda x : None if x==0 else int(x) )
        out_dataframe['permId'] = [ uuid.uuid4() for _ in range(len(out_dataframe.index)) ]
        out_dataframe['idOrigine'] = dataframe['observation_id'].apply(lambda x: x)
        out_dataframe['ocMethDet'] = dataframe['type_inventaire'].apply(lambda x: self.without_accent(x))
        # out_dataframe['cdRef'] = dataframe['taxref_id']

        return out_dataframe.to_csv(index=False, sep=';',encoding='utf-8')

    def without_accent(self, text, upper=False, title=False):
        import unicodedata
        if  text is not None :
            text = unicodedata.normalize('NFD', text)
            text = text.encode('ascii', 'ignore')
            text = text.decode("utf-8")
            if upper:
                text = str(text).upper()
            if title:
                text = str(' '+text).title()
            return str(text)
        else:
            return ''


class ExportProtocoleTypeView(CustomExportView):

    item = ExportObservationProjectView
    children = [('{int}', ExportObservationProjectView)]
    
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
    children = [('protocols', ExportProtocoleTypeView), ('observations', ExportObservationProjectView)]
    
    def __init__(self, ref, parent):
        CustomExportView.__init__(self, ref, parent)
        self.id_ = ref

    def retrieve(self):
        query = select([func.count(Station.ID)]).where(Station.FK_Project== self.id_)
        result = self.session.execute(query).scalar()
        return {'nb stations': result}


class ExportCollectionProjectView(CustomExportView):

    item = ExportProjectView
    children = [('{int}', ExportProjectView)]
    
    def retrieve(self):
        query = select([Project]).order_by(Project.Name.asc())
        result = [dict(row) for row in self.session.execute(query).fetchall()]
        return result

class ExportCoreView(CustomExportView):

    item = None
    children = [('projects', ExportCollectionProjectView)]
    def __init__(self, ref, parent):
        CustomExportView.__init__(self, ref, parent)

    def retrieve(self):
        return {'next items': 'views'
                }


RootCore.children.append(('export', ExportCoreView))
