from pyramid.security import NO_PERMISSION_REQUIRED, remember
from pyramid.view import view_config
from sqlalchemy import select
from ..Models import User, groupfinder, Project_User
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.response import Response
import json


@view_config(
    route_name='core/user',
    permission=NO_PERMISSION_REQUIRED,
    renderer='json'
)
def users(request):
    """Return the list of all the users with their ids.
    """
    pass
    session = request.dbsession
    query = select([
        User.id.label('PK_id'),
        User.Login.label('fullname')
    ]).order_by(User.Lastname, User.Firstname)
    return [dict(row) for row in session.execute(query).fetchall()]


@view_config(
    route_name='core/currentUser',
    renderer='json'
)
def current_user(request, user_id=None):
    """Return the list of all the users with their ids.
    """
    user_infos = request.authenticated_userid
    role = groupfinder(user_id, request)[0].replace('group:', '')
    policy = request.registry.queryUtility(IAuthenticationPolicy)
    # claims = policy.decode_jwt(request, token, verify=True)

    body = {'login': user_infos['login'],
            'fullname': user_infos['fullname'],
            'role': role,
            'lng': user_infos['userlanguage'],
            }

    if 'project' not in user_infos and role == 'client':
        claims = user_infos

        query = select([Project_User.FK_Project]).where(Project_User.FK_User == request.authenticated_userid['iss'])
        result = request.dbsession.execute(query).fetchall()
        print(result)
        projects_id = [row for row in result]
        claims['project'] = projects_id
        body['project'] = projects_id
        jwt = make_jwt(request, claims)
        response = Response(body=json.dumps(body), content_type='text/plain')
        remember(response, jwt)
        return response
    
    if 'project' in user_infos :
        body['project'] = user_infos['project']

    return body

def make_jwt(request, claims):
    policy = request.registry.queryUtility(IAuthenticationPolicy)
    return policy.encode_jwt(request, claims)

@view_config(
    route_name='users/id',
    renderer='json'
)
def getUser(request):
    pass
    user_id = int(request.matchdict['id'])
    return current_user(request, user_id=user_id)
