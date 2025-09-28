from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import Session, declarative_base, scoped_session

from config import DB_SETTINGS

Base = declarative_base()


class SessionFactory(Session):

    def __init__(self) -> None:
        super().__init__(autoflush=False)
        self.url = self._url
        self.bind = self._engine

    @property
    def _url(self) -> str:
        user = f'{DB_SETTINGS['db_user']}:{DB_SETTINGS['db_password']}'
        host = DB_SETTINGS['db_host']
        port = DB_SETTINGS['db_port']
        db_name = DB_SETTINGS['db_name']
        return f'postgresql://{user}@{host}:{port}/{db_name}'

    @property
    def _engine(self) -> Engine:
        return create_engine(self.url)


DBSession = scoped_session(SessionFactory)