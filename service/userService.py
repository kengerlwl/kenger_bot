from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from entity.User import db_session, User  # 从models.py中导入session和User模型
import threading
from Config import Config

class DatabaseUtils:
    _db_engine = None
    _local = threading.local()

    @classmethod
    def get_db_engine(cls):
        if cls._db_engine is None:
            cls._db_engine = create_engine(Config().SQLALCHEMY_DATABASE_URI)  # 这里替换为你的数据库连接URL
        return cls._db_engine

    @classmethod
    def get_session(cls):
        if not hasattr(cls._local, 'session'):
            Session = sessionmaker(bind=cls.get_db_engine())
            cls._local.session = Session()
        return cls._local.session

class UserService:
    @staticmethod
    def register_user(username, password):
        session = DatabaseUtils.get_session()
        
        # 检查是否已存在该用户
        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            return False, "Username already exists"
        
        # 创建新用户
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        session.add(new_user)
        session.commit()
        return True, "User registered successfully"

    @staticmethod
    def authenticate_user(username, password):
        session = DatabaseUtils.get_session()
        # print("session", session)    

        # 查找用户
        user = session.query(User).filter_by(username=username).first()
        # print("user", user)
        if user and check_password_hash(user.password, password):
            return True, user
        return False, "Invalid credentials"