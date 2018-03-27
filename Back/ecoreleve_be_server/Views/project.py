from ..Models import (
    Project,
    ProjectList,
    Station
)
from sqlalchemy import select, desc, join, outerjoin
from collections import OrderedDict
from sqlalchemy.exc import IntegrityError
from ..controllers.security import context_permissions
from ..Views import DynamicObjectView, DynamicObjectCollectionView
from ..controllers.security import RootCore
from .station import StationsView
from pyramid.security import Allow


class ProjectStationsView(StationsView):

    def __init__(self, ref, parent):
        StationsView.__init__(self, ref, parent)
        self.__acl__ = parent.__acl__

    def handleCriteria(self, params):
        params = StationsView.handleCriteria(self, params)
        if 'criteria' not in params:
            params['criteria'] = []

        if not params.get('offset', None):
            params['offset'] = 0

        params = self.addProjectFilter(params)
        return params

    def formatParams(self, params, paging):
        return StationsView.formatParams(self, params, False)

    def addProjectFilter(self, params):
        criteria = [{'Column': 'FK_Project',
                     'Operator': '=',
                     'Value': self.parent.objectDB.ID
                     }]
        params['criteria'].extend(criteria)
        return params


class ProjectView(DynamicObjectView):

    model = Project
    children = [('stations', ProjectStationsView)]

    def __init__(self, ref, parent):
        DynamicObjectView.__init__(self, ref, parent)
        user_infos = self.request.authenticated_userid
        print('ini project ', user_infos, ' ref  : ', ref)
        if user_infos['app_roles']['ecoreleve'].lower() == 'client' and int(ref) in user_infos['project']:
            self.__acl__ = [(Allow, 'group:client', 'read')]
        else :
            print('not a client')
            self.__acl__ = context_permissions['project']


class ProjectsView(DynamicObjectCollectionView):

    Collection = ProjectList
    item = ProjectView
    children = [('{int}', ProjectView)]
    
    moduleFormName = 'ProjectForm'
    moduleGridName = 'ProjectGrid'

    def __init__(self, ref, parent):
        DynamicObjectCollectionView.__init__(self, ref, parent)
        self.__acl__ = context_permissions[ref]

    def handleCriteria(self, params):
        params = DynamicObjectCollectionView.handleCriteria(self, params)

        if self.request.authenticated_userid['app_roles']['ecoreleve'].lower() == 'client':
            params = self.addProjectFilter(params)
        return params

    def addProjectFilter(self, params):
        criteria = [{'Column': 'ID',
                    'Operator': 'IN',
                    'Value': ', '.join(str(x) for x in self.request.authenticated_userid['project'])
                    }]
        params['criteria'].extend(criteria)
        return params


RootCore.children.append(('projects', ProjectsView))
