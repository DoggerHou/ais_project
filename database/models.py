from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Инициализация базы данных
db = SQLAlchemy()


# Пользователь
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Набор данных SKU
class SkuDataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(120), default="Набор по умолчанию")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('datasets', lazy=True))


# Товары внутри набора
class SkuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('sku_dataset.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    demand = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False)

    dataset = db.relationship('SkuDataset', backref=db.backref('items', lazy=True))


# Результаты оптимизации
class ReplenishmentPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku_item_id = db.Column(db.Integer, db.ForeignKey('sku_item.id'), nullable=False)
    replenishment_times = db.Column(db.Integer, nullable=False)
    calculated_at = db.Column(db.DateTime, default=datetime.utcnow)

    sku_item = db.relationship('SkuItem', backref=db.backref('plans', lazy=True))

