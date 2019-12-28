from flask_sqlalchemy import SQLAlchemy

db2 = SQLAlchemy()

class Tx_history(db2.Model):
    __tablename__ = "txs"
    __bind_key__ = 'test1'

    id = db2.Column(db2.Integer, primary_key=True)
    address = db2.Column(db2.String(64))
    tx = db2.Column(db2.String(100))

    @property  # 실제로 함수지만, 접근할때 함수가 아닌 변수처럼 사용 가능 - property
    def serialize(self):
        return {
            'id': self.id,
            'address': self.address,
            'tx': self.tx,
        }


# class Transactions(db.Model):
#     __tablename__ = "tx_history"