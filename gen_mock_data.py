# pylama:ignore=E402
from skygear.options import parse_args

if __name__ == '__main__':
    parse_args()

from uuid import uuid4
from datetime import datetime
from plugin.db_extensions.db_session import scoped_session
from plugin.models import (
    Celebrity,
    Country,
)

from plugin.models.queries import (
    CelebrityQuery,
    CelebrityFollowQuery,
    CountryQuery,
    UserQuery,
)


def create_celebrity(username, display_name, country):
    current_time = datetime.utcnow()
    return Celebrity(
        id=str(uuid4()),
        username=username,
        display_name=display_name,
        country=country,
        followers_count=0,
        _created_at=current_time,
        _updated_at=current_time,
    )


def generate_celecrities(session, countries):
    celebrities = [
        create_celebrity(
            'celebrity_' + str(i + 1),
            'International Celebrity ' + str(i + 1),
            None)
        for i in range(10)
    ]

    for country in countries:
        celebrities += [
            create_celebrity(
                (
                    country.name.lower().replace(' ', '_') +
                    '_celebrity_' +
                    str(i + 1)
                ),
                country.name + ' Celebrity ' + str(i + 1),
                country)
            for i in range(5)
        ]

    return celebrities


def create_country(name):
    current_time = datetime.utcnow()
    return Country(
        id=str(uuid4()),
        name=name,
        _created_at=current_time,
        _updated_at=current_time,
    )


def generate_countries(session):
    return [
        create_country('Hong Kong'),
        create_country('China'),
        create_country('United Kindom'),
        create_country('United State'),
        create_country('Japan'),
        create_country('Germany'),
        create_country('France'),
        create_country('Switzerland'),
    ]


if __name__ == '__main__':

    with scoped_session() as session:
        users = UserQuery(session).query.all()
        for user in users:
            user.country = None
            user.followers_count = 0
            user.following_count = 0
        session.add_all(users)

        CelebrityFollowQuery(session).query.delete()
        CelebrityQuery(session).query.delete()
        CountryQuery(session).query.delete()

    with scoped_session() as session:
        countries = generate_countries(session)
        celebrities = generate_celecrities(session, countries)
        session.add_all(countries + celebrities)
