class BaseQuery:
    def __init__(self, session):
        self.session = session
        self.query = self.session.query(self.model())

    def model(self):
        raise NotImplemented

    def filter_by_id(self, id):
        self.query = self.query.filter(self.model().id == id)
        return self

    def paginate(self, page, page_size):
        return self.offset((page - 1) * page_size).limit(page_size)

    def limit(self, size):
        self.query = self.query.limit(size)
        return self

    def offset(self, size):
        self.query = self.query.offset(size)
        return self

    def order_by(self, column, is_desc=False):
        if is_desc:
            self.query = self.query.order_by(column.desc())
        else:
            self.query = self.query.order_by(column)

        return self

    def all(self):
        return self.query.all()

    def one(self):
        return self.query.one()

    def first(self):
        return self.query.first()

    def count(self):
        return self.query.count()
