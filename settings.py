import os

MONGO_URI = os.environ.get(
    'MONGODB_URI', 'mongodb://rahasya:1313@0.0.0.0:27017/hackit')


RESOURCE_METHODS = ['GET', 'POST', 'DELETE']


ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20
PAGINATION_LIMIT = 600
PAGINATION_DEFAULT = 600
#DEBUG = True



MONGO_QUERY_BLACKLIST = ['$where']

places = {

    'item_title': 'table',

    'schema': {
        'version': {
            'type': 'number'
        },
        "SrNo": {'type': 'number'},
        

    }
}


DOMAIN = {
    'places': places

}
