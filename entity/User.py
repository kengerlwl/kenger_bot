from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer, String

# 创建SQLAlchemy引擎和session管理
engine = create_engine("mysql://kenger:WKcqDgd8k5WgF2Xp2koj@127.0.0.1:3306/kenger_blog")  # 这里替换为你的数据库连接URL
db_session = scoped_session(sessionmaker(autoflush=False, bind=engine))

# 定义基础模型
from sqlalchemy.orm import sessionmaker, declarative_base

# 定义基础模型
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(120), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"