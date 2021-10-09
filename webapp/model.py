from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Swagger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    edit_date = db.Column(db.DateTime, nullable=False)
    create_date = db.Column(db.DateTime, nullable=False)
    swagger = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return '<Swagger {} {}>',format(self.title, self.author)
