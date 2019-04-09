from skygear.options import options
from sqlalchemy import (
    Column,
    DateTime,
    JSON,
    Text,
    ForeignKey as _ForeignKey,
)
import os

if hasattr(options, 'appname'):
    schema_name = 'app_%s' % options.appname
else:
    schema_name = ''


class SkygearMixin(object):
    __table_args__ = {'schema': schema_name}
    id = Column('_id', Text, primary_key=True, nullable=False)
    _database_id = Column('_database_id', Text, primary_key=True, default='')
    _owner_id = Column('_owner_id', Text, primary_key=True, default='')
    _created_by = Column('_created_by', Text)
    _updated_by = Column('_updated_by', Text)
    _access = Column('_access', JSON, default=[])
    _created_at = Column('_created_at', DateTime, nullable=False)
    _updated_at = Column('_updated_at', DateTime, nullable=False)

    def get_asset_url(self, asset_id):
        if asset_id is not None:
            url = os.getenv('CLOUD_ASSET_PUBLIC_PREFIX') + '/'

            if not os.getenv('ASSET_STORE') == 'local':
                url += os.getenv('APP_NAME') + '/'

            return (url + asset_id).replace(' ', '%20')
        else:
            return None


def ForeignKey(key):
    if schema_name == '':
        return _ForeignKey(key)
    else:
        return _ForeignKey('{}.{}'.format(schema_name, key))
