import skygear

from ...models.queries import CountryQuery
from ...serializers import CountrySchema
from ...db_extensions.db_session import scoped_session


@skygear.handler('base-info/countries',
                 method=['GET'],
                 user_required=False)
def get_country_list(request):
    response = []

    with scoped_session() as session:
        country_record_list = CountryQuery(session).get_all()
        response = CountrySchema(many=True).dump(country_record_list).data

    return response
