import redis
#print(dir(redis))
r = redis.Redis(host = 'localhost', port = 6381, db = 0)

def set_info(key, info):
    ''''''

    r = redis.Redis(host = 'localhost', port = 6381, db = 0)
    r.set(key, info)
    res = [key.decode('utf-8') for key in r.keys()]
    if len(res) > 20:
        r.delete(res[-1])


def get_info(key):
    ''''''
    
    r = redis.Redis(host = 'localhost', port = 6381, db = 0)
    if r.get(key):
        value = r.get(key).decode('utf-8')
    else:
        return False
    r.delete(key)

    r.set(key, value)
    return value


def show_cache():
    ''''''

    r = redis.Redis(host = 'localhost', port = 6381, db = 0)
    res = [key.decode('utf-8') for key in r.keys()]
    return res
    
#set_info('show all tags', 'some tags')
#print(show_cache())
#r.delete('note_search(second)')
#print(get_info('3'))
#r.delete(1)
#r.set('2','4')
#print(r.get('2'))

#print(r.get(2))
#print(show_cache())
