from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = "users"

    # id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(100))
    mnemonic = db.Column(db.String(200))

    # id = db.Column(db.Integer, primary_key=True)
    # password = db.Column(db.String(64))
    # account = db.Column()
    # userid = db.Column(db.String(32))
    # username = db.Column(db.String(8))

    @property  # 실제로 함수지만, 접근할때 함수가 아닌 변수처럼 사용 가능 - property
    def serialize(self):
        return {
            'id': self.id,
            'address': self.address,
            'password': self.password,
            'mnemonic': self.mnemonic
        }
