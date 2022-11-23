from extensions import db, bcrypt



class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                        nullable=False)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    phone = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    is_superuser = db.Column(db.Enum("true", "false"), default="false")

    def __init__(self, first_name, last_name, phone, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

