from pyramid.view import view_config
from ..Models import (
    Observation,
    Station,
    # ProtocoleType,
    MediasFiles,
    FieldActivity_ProtocoleType,
    fieldActivity,
    ErrorAvailable,
    sendLog,
    dbConfig
)
import os
import base64
from sqlalchemy import select, and_, join
from traceback import print_exc
from ..Views import DynamicObjectView, DynamicObjectCollectionView
from ..controllers.security import RootCore
from pyramid.security import (
    Allow,
    Authenticated,
    ALL_PERMISSIONS)
import json
import geojson

class ObservationView(DynamicObjectView):

    model = Observation

    def __init__(self, ref, parent):
        DynamicObjectView.__init__(self, ref, parent)
        
    def __getitem__(self, ref):
        if ref in self.actions:
            self.retrieve = self.actions.get(ref)
            return self
        return self

    def update(self, json_body=None):
        if not json_body:
            data = self.request.json_body
        else:
            data = json_body

        curObs = self.objectDB
        listOfSubProtocols = []
        responseBody = {'id': curObs.ID}
        listOfDeletedFiles = []

        for items, value in data.items():
            if isinstance(value, list) and items != 'children':
                if items in ('images'):
                    for photo in value:                     
                        if 'status' in photo and photo['status'] == 'deleted':
                            fileDeleted= {}
                            fileDeleted['model'] = self.session.query(MediasFiles).filter(MediasFiles.Id == photo['id']).one()
                            fileDeleted['status'] =  self.session.query(MediasFiles).filter(MediasFiles.Id == photo['id']).delete()           
                            listOfDeletedFiles.append(fileDeleted)
                else:
                    listOfSubProtocols = value

        data['Observation_childrens'] = listOfSubProtocols
        curObs.values = data
        try:
            if curObs.Equipment is not None:
                curObs.Station = curObs.Station
            self.session.commit()
            for item in listOfDeletedFiles:
                if item['status'] == 1:
                    removedModel = item['model']
                    absUrl = os.path.abspath( os.path.join(dbConfig['mediasFiles']['path'],str(removedModel.FK_Observation),removedModel.Name))
                    try:
                        os.remove(absUrl)
                    except OSError as  e:  ## if failed, report it back to the user ##
                        print ("Error: %s - %s." % (e.filename, e.strerror))
                        raise

        except ErrorAvailable as e:
            self.session.rollback()
            self.request.response.status_code = 409
            responseBody['response'] = e.value

        return responseBody

    def delete(self):
        if self.objectDB:
            id_ = self.objectDB.ID
            DynamicObjectView.delete(self)
        else:
            id_ = None
        response = {'id': id_}
        return response


class ObservationsView(DynamicObjectCollectionView):

    Collection = None
    item = ObservationView
    children = [('{int}', ObservationView)]
    moduleFormName = 'ObservationForm'
    moduleGridName = 'ObservationFilter'

    def __init__(self, ref, parent):
        DynamicObjectCollectionView.__init__(self, ref, parent)
        self.POSTactions = {'batch': self.batch}
        self.parent = parent
        if 'objectType' in self.request.params:
            self.typeObj = int(self.request.params['objectType'])
        self.__acl__ = [
            (Allow, 'group:admin', ALL_PERMISSIONS),
            (Allow, 'group:superUser', ALL_PERMISSIONS),
            (Allow, 'group:user', ALL_PERMISSIONS)
        ]
        

    def __getitem__(self, ref):
        self.create = self.POSTactions.get(ref)
        return DynamicObjectCollectionView.__getitem__(self, ref)

    def retrieve(self):
        # if self.parent.__class__.__name__ == 'StationView':
        if True:
            if self.typeObj:
                return self.getObservationsWithType()
            else:
                return self.getProtocolsofStation()
        else:
            self.request.response.status_code = 520
            response = self.request.response
            response.text = 'A station ID is needed, try this url */stations/{id}/observations'
            return response

    def insert(self, json_body=None):
        if not json_body:
            json_body = self.request.json_body

        data = {}
        for items, value in json_body.items():
            if items in ('trace') :
                jsonTrace = None
                if value not in (None , ''):
                    jsonTrace = json.loads(value)
                data['geom'] = jsonTrace
            else:
                data[items] = value

        if data.get('type_name', None):
            data['type_name'] = data['type_name'].title()
        if 'station' in data and self.parent.__class__.__name__ != 'StationView':
            sta = Station()
            sta.session = self.session
            if 'type_id' not in data['station']:
                data['station']['type_id'] = 1

            sta.values = data['station']
            self.session.add(sta)
            self.session.flush()

        elif self.parent.__class__.__name__ == 'StationView':
            sta = self.parent.objectDB

        curObs = self.item.model(FK_Station=sta.ID)
        listOfSubProtocols = []
        listOfPhotos = []

        #ToDO get form to retrieve if subObs exists in schema
        # Because next lines are very bad
        for items, value in data.items():
            if isinstance(value, list) and items not in ('children'):
                if items in ('images'):
                    for photo in value:
                        curMedia = MediasFiles(
                            Path = photo['name'],
                            Name = photo['name'],
                            Extension = photo['name'].split(".")[-1],
                            Creator = self.request.authenticated_userid['iss']
                        )
                        listOfPhotos.append((curMedia,photo['base64Data']))
                        # pass
                else:
                    listOfSubProtocols = value

        data['Observation_childrens'] = listOfSubProtocols
        ###

        responseBody = {}

        try:
            curObs.values = data
            curObs.Station = sta
            self.session.add(curObs)
            self.session.commit()
            idObs = curObs.ID
            
            for item,base64File in listOfPhotos:
                item.Path = os.path.join(str(idObs),item.Path)
                item.FK_Observation = idObs
                try:
                    self.session.add(item)
                    self.session.commit()
                    if item.Id:
                        urlNewFile = os.path.join(dbConfig['mediasFiles']['path'],item.Path)
                        os.makedirs(os.path.dirname(urlNewFile), exist_ok=True)
                        with open(urlNewFile,"wb") as fh:
                            fh.write( base64.b64decode(base64File.replace('data:image/jpeg;base64,','')) )                            
                except Exception as e:
                    print("nop error ")
                    print(e)

                    raise 
            self.session.flush()
            responseBody['id'] = curObs.ID
            # self.session.rollback()
            # self.request.response.status_code = 409

        except Exception as e:
            self.session.rollback()
            self.request.response.status_code = 409
            responseBody['response'] = type(e)
            #sendLog(logLevel=1, domaine=3,msg_number=self.request.response.status_code)
        return responseBody

    def batch(self):
        rowData = self.request.json_body['rowData']
        responseBody = {'updatedObservations': [],
                        'createdObservations': []
                        }

        for row in rowData:
            if 'delete' in self.request.json_body:
                item = self.item(row['ID'], self)
                responseBody['updatedObservations'].append(item.delete())
                continue

            if 'ID' in row:
                item = self.item(row['ID'], self)
                responseBody['updatedObservations'].append(item.update(row))
            else:
                row['FK_ProtocoleType'] = self.request.json_body['FK_ProtocoleType']
                responseBody['createdObservations'].append(self.insert(row))

        return responseBody

    def getObservationsWithType(self):
        sta_id = self.parent.objectDB.ID
        listObs = list(self.session.query(Observation
                                          ).filter(Observation.type_id == self.typeObj
                                                   ).filter(Observation.FK_Station == sta_id))
        values = []
        for i in range(len(listObs)):
            curObs = listObs[i]
            # curObs.LoadNowValues()
            values.append(curObs.getDataWithSchema()['data'])

        return values

    def getProtocolsofStation(self):
        curSta = self.parent.objectDB
        sta_id = curSta.ID
        response = []

        try:
            if 'FormName' in self.request.params:
                # ON recupere les obs exixtante de la station 
                listObs = list(self.session.query(Observation).filter(
                    and_(Observation.FK_Station == sta_id, Observation.Parent_Observation == None)))
                listType = list(self.session.query(FieldActivity_ProtocoleType
                                                   ).filter(FieldActivity_ProtocoleType.FK_fieldActivity == curSta.fieldActivityId))
                
                listProto = {}
                if listObs:
                    for i in range(len(listObs)):
                        DisplayMode = 'edit'
                        curObs = listObs[i]
                        curObsType = curObs._type
                        typeID = curObsType.ID
                        if typeID in listProto:
                            listProto[typeID]['obs'].append(curObs.ID)
                        else:
                            typeName = curObsType.Label.replace('_', ' ')
                            if curObsType.Status == 10:
                                curObsForm = curObs.getForm(
                                    displayMode=DisplayMode)
                                curObsForm['grid'] = True
                            else:
                                curObsForm = {}
                                curObsForm['grid'] = False

                            listProto[typeID] = {
                                'Name': typeName,
                                'schema': curObsForm.get('schema', None),
                                'fieldsets': curObsForm.get('fieldsets', None),
                                'grid': curObsForm['grid'],
                                'obs': [curObs.ID]
                            }

                # ON complete la liste des obs avec les type de protocole requis pour la field activity
                if listType:
                    listVirginProto = list(
                        filter(lambda proto: proto.FK_ProtocoleType not in listProto, listType))

                    for i in range(len(listVirginProto)):
                        DisplayMode = 'edit'
                        typeID = listVirginProto[i].FK_ProtocoleType

                        curVirginObs = Observation(type_id=typeID)
                        curVirginObsType = curVirginObs._type
                        typeName = curVirginObsType.Label.replace('_', ' ')
                        protoStatus = curVirginObsType.obsolete

                        if protoStatus != 1:
                            if curVirginObsType.Status == 10:
                                curVirginObsForm = curVirginObs.getForm(
                                    displayMode=DisplayMode)
                                curVirginObsForm['grid'] = True
                            else:
                                curVirginObsForm = {}
                                curVirginObsForm['grid'] = False

                            listProto[typeID] = {
                                'Name': typeName,
                                'schema': curVirginObsForm.get('schema', None),
                                'fieldsets': curVirginObsForm.get('fieldsets', None),
                                'grid': curVirginObsForm['grid'],
                                'obs': []
                            }

                globalListProto = [{'ID': typeID,
                                    'Name': listProto[typeID]['Name'],
                                    # 'Label' : listProto[typeID]['Label'],
                                    'schema':listProto[typeID]['schema'],
                                    'fieldsets':listProto[typeID]['fieldsets'],
                                    'grid':listProto[typeID]['grid'],
                                    'obs':listProto[typeID]['obs']
                                    }
                                   for typeID in listProto.keys()
                                   ]

                response = sorted(globalListProto, key=lambda k: k['Name'])

        except Exception as e:
            print_exc()
            pass
        return response

    def getType(self):
        ProtocoleType = Observation.TypeClass
        if 'FieldActivityID' in self.request.params:
            fieldActivityID = self.request.params['FieldActivityID']
            join_table = join(ProtocoleType, FieldActivity_ProtocoleType,
                              ProtocoleType.ID == FieldActivity_ProtocoleType.FK_ProtocoleType)
            query = select([ProtocoleType.ID, ProtocoleType.Name]
                           ).where(and_(ProtocoleType.Status.in_([4, 8, 10]),
                                        FieldActivity_ProtocoleType.FK_fieldActivity == fieldActivityID)
                                   ).select_from(join_table)
        else:
            query = select([ProtocoleType.ID, ProtocoleType.Label]).where(
                ProtocoleType.Status.in_([4, 8, 10]))
        query = query.where(ProtocoleType.obsolete == False)
        result = self.session.execute(query).fetchall()
        res = []
        for row in result:
            elem = {}
            elem['ID'] = row['ID']
            elem['Name'] = row['Label'].replace('_', ' ')
            res.append(elem)
        res = sorted(res, key=lambda k: k['Name'])
        return res


RootCore.children.append(('protocols', ObservationsView))
