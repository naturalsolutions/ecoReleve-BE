from ..Models import (
    Client,
    MonitoredSite,
    Base,
    ClientList
)
from sqlalchemy import select, desc, join, outerjoin
from collections import OrderedDict
from sqlalchemy.exc import IntegrityError
from ..controllers.security import context_permissions
from ..Views import DynamicObjectView, DynamicObjectCollectionView
from ..Views.project import ProjectsView
from ..controllers.security import RootCore


class ClientView(DynamicObjectView):

    model = Client
    children = [('projects', ProjectsView)]

    def __init__(self, ref, parent):
        DynamicObjectView.__init__(self, ref, parent)
        self.__acl__ = context_permissions['clients']
        # self.add_child('projects', ProjectsView)
        # self.actions = {'projects': self.getStations}

    def __getitem__(self, ref):
        if ref in self.actions:
            self.retrieve = self.actions.get(ref)
            return self
        return self.get(ref)


class ClientsView(DynamicObjectCollectionView):

    Collection = ClientList
    item = ClientView
    children = [('{int}', ClientView)]
    
    moduleFormName = 'ClientForm'
    moduleGridName = 'ClientGrid'

    def __init__(self, ref, parent):
        DynamicObjectCollectionView.__init__(self, ref, parent)
        self.__acl__ = context_permissions[ref]


RootCore.children.append(('clients', ClientsView))
