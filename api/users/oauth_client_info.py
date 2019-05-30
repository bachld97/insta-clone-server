def read_auth_info():
    f = open('client.secret', 'r')
    lines = f.readlines()
    client_id = lines[0].strip()
    client_secret = lines[1].strip()
    f.close()
    return {
        'client_id': client_id,
        'client_secret': client_secret
    }
