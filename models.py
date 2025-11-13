from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    item = db.Column(db.String(255))  # 👈 add here
    amount = db.Column(db.Numeric(10,2), nullable=False)
    category = db.Column(db.String(100), default='Other')
    expense_date = db.Column(db.Date, nullable=False)
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'amount': float(self.amount),
            'category': self.category,
            'expense_date': self.expense_date.isoformat(),
            'note': self.note,
        }

