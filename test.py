from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

# 创建基础模型
Base = declarative_base()

# 创建数据库引擎
engine = create_engine("mysql+pymysql://kenger:WKcqDgd8k5WgF2Xp2koj@127.0.0.1:3306/kenger_blog")
Session = sessionmaker(bind=engine)
session = Session()

# 用户模型
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(120), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

# 创建表
Base.metadata.create_all(engine)

# 添加用户
username = "testuser"
password = "11"
password_hash = generate_password_hash(password)
print(f"Password hash: {password_hash}")
new_user = User(username=username, password=password_hash)
session.add(new_user)
session.commit()

# 查询用户并验证密码
user = session.query(User).filter_by(username=username).first()
print(f"User found: {user}")
print("Password verification:", check_password_hash(user.password, password))

# 关闭会话
session.close()