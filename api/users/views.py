from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

from . import oauth_client_info

import requests

from .serializers import CreateUserSerializer

client_info = oauth_client_info.read_auth_info()
CLIENT_ID = client_info['client_id']
CLIENT_SECRET = client_info['client_secret']

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    '''
    Registers user to the server. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''
    # Put the data from the request into the serializer
    serializer = CreateUserSerializer(data=request.data)
    # Validate the data
    if serializer.is_valid():
        # If it is valid, save the data (creates a user).
        serializer.save()
        # Then we get a token for the created user.
        # This could be done differentley
        r = requests.post('http://0.0.0.0:8000/o/token/',
            data={
                'grant_type': 'password',
                'username': request.data['username'],
                'password': request.data['password'],
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            },
        )
        return Response(r.json())
    return Response(serializer.errors)



@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    '''
    Gets tokens with username and password. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''
    username = request.data.get('username', request.query_params.get('username', None))
    password = request.data.get('password', request.query_params.get('password', None))
    
    if username is None or password is None:
        return Response(
            { 'error': 'username or password not found' }, 
            status=status.HTTP_400_BAD_REQUEST
        )

    r = requests.post(
    'http://0.0.0.0:8000/o/token/',
        data={
            'grant_type': 'password',
            'username': username,
            'password': password,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    
    response_data = {}
    token_data = r.json()
    if 'access_token' in token_data.keys(): # login success
        response_data = {
            'token_info': token_data,
            'user_info': { 'name': username },
            'user_not_found': False,
            'wrong_password': False,
        }
    else:
        response_data = _construct_error_response_(username=username)

    return Response(response_data)


def _construct_error_response_(username):
    wrong_password = User.objects.filter(username=username).exists()
    user_not_found = not wrong_password
    return {
        'user_not_found': user_not_found,
        'wrong_password': wrong_password
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    '''
    Registers user to the server. Input should be in the format:
    {"refresh_token": "<token>"}
    '''
    r = requests.post(
    'http://0.0.0.0:8000/o/token/',
        data={
            'grant_type': 'refresh_token',
            'refresh_token': request.data['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response(r.json())


@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request):
    '''
    Method to revoke tokens.
    {"token": "<token>"}
    '''
    r = requests.post(
        'http://0.0.0.0:8000/o/revoke_token/',
        data={
            'token': request.data['token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    # If it goes well return sucess message (would be empty otherwise)
    if r.status_code == requests.codes.ok:
        return Response({'message': 'token revoked'}, r.status_code)
    # Return the error if it goes badly
    return Response(r.json(), r.status_code)
