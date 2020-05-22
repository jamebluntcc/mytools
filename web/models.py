from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
Column = db.Column


filter_null = lambda x: x if x else '-'


class dbCRUD:

    __tablename__ = ''

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


class User(db.Model, dbCRUD):
    __tablename__ = 'user'
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(10), nullable=False)
    phone = Column(db.String(11))
    address = Column(db.String(45))
    create_time = Column(db.DateTime)


def generateDTcls(cls):
    class DT(cls):
        def __init__(self, **kwargs):
            self.draw = kwargs['draw']
            self.page = kwargs['page']
            self.length = kwargs['length']
            self.search_str = kwargs['search']
            self.order_str = kwargs['order']
            self.columns = self.to_list()

        def result(self, **kwargs):
            if kwargs:
                self.query = cls.query.filter_by(**kwargs)
            else:
                self.query = cls.query
            self.search()
            self.order()
            return self.pager()

        def to_list(self):
            '''
            rewrite this method to load new datatables
            :return:
            '''
            pass

        def search(self):
            if self.search_str:
                try:
                    col, pattern = self.search_str.split(':')
                    self.like(col, pattern)
                except:
                    pass

        def order(self):
            if self.order_str:
                order_type, index = self.order_str.split()
                col = self.columns[int(index)]
                if order_type == 'desc':
                    self.query = self.query.order_by((getattr(cls, col).desc()))
                else:
                    self.query = self.query.order_by(getattr(cls, col))

        def like(self, col, keyword):
            self.query = self.query.filter(getattr(cls, col).like('%{}%'.format(keyword)))

        @staticmethod
        def get_attr(obj, attr):
            return filter_null(getattr(obj, attr, '-'))

        def pager(self):
            pagination = self.paginate(page=self.page, per_page=self.length, error_out=True)
            recordsTotal = self.query.count()
            objs = pagination.items
            rs = []
            for obj in objs:
                rs.append({attr: self.get_attr(obj, attr) for attr in self.columns})
            res = {
                'draw': self.draw,
                'recordsTotal': recordsTotal,
                'recordsFiltered': recordsTotal,
                'data': rs
            }
            return res
    return DT