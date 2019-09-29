from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from typing import Union, Dict, List, TypeVar


class SingletonEngines:
    def __init__(self, con_defs: Union[Dict[str, str], None]) -> None:
        self._con_defs: Dict[str, str] = con_defs or {}
        self._engines: Dict[str, Union[None, Engine]] = {}

    @property
    def definitions(self) -> Dict[str, str]:
        return self._con_defs

    @definitions.setter
    def definitions(self, defs: Dict[str, str]) -> None:
        self._con_defs = defs

    def load(self, force=False) -> None:
        for name, uri in self._con_defs.items():
            if name not in self._engines or force:
                self._engines[name] = self._create_engine(uri)

    def get(self, name: str) -> Union[str, Engine]:
        if name in self._engines:
            return self._engines.get(name)
        self._engines[name] = self._create_engine(self._get_engine_def(name))
        return self._engines.get(name)

    def set(self, name: str, engine: Engine) -> None:
        self._engines['name'] = engine

    def _create_engine(self, con_def: Union[None, str] = None
                       ) -> Union[None, Engine]:
        return create_engine(con_def) if con_def else None

    def _get_engine_def(self, name: str) -> Union[str, None]:
        return self._con_defs.get(name)


engines = None


def init_engines(con_defs: Union[Dict[str, str], None] = None) -> None:
    global engines
    engines = SingletonEngines(con_defs)


def get_engines(con_defs: Union[Dict[str, str], None] = None) -> SingletonEngines:
    global engines
    if engines is None:
        init_engines(con_defs)
    return engines


if __name__ == '__main__':
    definitions = {
        'test': 'mysql+mysqldb://{user}:{passwd}@{host}/test'.format(user='root', passwd='mysql', host='mysql')
    }
    engines = get_engines(definitions)
    engines.load()
    e = engines.get('test')
    conn = e.raw_connection()
    cursor = conn.cursor()
    while True:
        try:
            sql = input('input sql:\n')
        except KeyboardInterrupt:
            break
        cursor.execute(sql)

        res = cursor.fetchall()
        print(list(res))
    print('closing...')
    cursor.close()
    conn.close()
