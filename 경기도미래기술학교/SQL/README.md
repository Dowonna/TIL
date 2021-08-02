2021-08-02. 원래 수업은 2021-07-20 부터 실시되었으나, 늦게나마 TIL 작성을 시작하였습니다. 양해 바랍니다.  

---

## 1. SQL Alchemy란 무엇이며, 왜 필요한가?

### [📚 Object Relational Tutorial (1.x API)](https://docs.sqlalchemy.org/en/14/orm/tutorial.html#object-relational-tutorial-1-x-api)

### Python에서 사용가능한 ORM(Object-relational mapping).

- `ORM`은 객체(Object)와 관계(Relational)를 연결해주는 역할을 한다.

![SQL Alchemy ORM](https://tekshinobi.com/wp-content/uploads/2020/04/box-diag-sqla.jpg)

- 장점
    - 객체 지향적인 코드로 비즈니스 로직에 집중가능함
    - 재사용 및 유지보수가 용이함
    - DBMS(DataBase Management System)에 대한 종속성이 줄어듬

- 단점
    - ORM 만으로 서비스를 구현하기 어려움
    - 프로시저가 많은 시스템에서는 장점을 가지기 어려움

- 설치방법
    - 아나콘다 프롬프트
    ```powershell
    $ conda install sqlalchemy
    ```
    - pip install
    ```powershell
    $ pip install sqlalchemy
    ```

## 2. SQL Alchemy 기초

### 엔진 생성

### [📚 Engine Configuration](https://docs.sqlalchemy.org/en/14/core/engines.html#engine-configuration)

- 사용방법

    - **MySQL**
    ```python
    engine = create_engine('mysql+pymysql://root:1234@localhost:3306/pythondb')
    ```
    아니면
    ```python
    engine = create_engine('mysql+mysqldb://root:1234@localhost:3306/pythondb)
    ```

    - **Oracle**
    ```python
    engine = create_engine('oracle+cx_oracle://scott:tiger@localhost:1521/xe')
    ```

    - **SQLite**
    ```python
    engine = create_engine('sqlite:///foo.db)
    ```
    아니면
    ```python
    engine = create_engine('sqlite:///:memory:')
    ``` 

### 테이블 생성 및 엔진 등록

```python
# 자주 사용하는 모듈 Import
import sqlalchemy as 

from sqlalchemy import create_engine
from sqlalchemy import and_, or_
from sqlalchemy import ForeignKey
from sqlalchemy import Column, DateTime, Integer, String, Float

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import relationship

# 클래스 선언
"""
class 클래스명(Base):
    __tablename__ = 'DB에_등록된_테이블명_입력'
    col1 = Column(Type, primary_key=True)
    col2 = Column(Type, ...)

    def __init__(self, col1=None, col2=None):
        self.col1 = col1
        self.col2 = col2

Base.metadata.create_all(bind=engine)
"""
class User(Base):
    __tablename__ = 'users'  # DB에 등록된 테이블 로딩
    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)
    email = Column(String(30), unique=True)
    
    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

# Base를 상속받는 클래스들을 모두 테이블로 생성함
Base.metadata.create_all(bind=engine)
```

- 데이터 제어를 위한 Session 객체 생성
```python
db_session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))  ### autoflush=False | 버퍼가 가득 차면 예외발생 후 작업을 중지시키고 Error 반환
```

- 데이터 입력 후 세션 추가
```python
user1 = User('Lee Minjae', 'dipleinelven@naver.com')
user2 = User('Kamil Lee', 'parousia0918@gmail.com')

# Pending 상태로 저장함
db_session.add(user1)
db_session.add(user2)

# Pending 상태를 Persist 상태로 저장함
db_session.commit()

# DB 접속 종료
db_session.close()
```

- 특정 테이블의 모든 데이터 조회
```python
user_list = db_session.query(User).all()

for user in user_list:
    print(user.id, user.name, user.email)

"""
1 Lee Minjae dipleinelven@naver.com
2 Kamil Lee parousia0918@gmail.com
"""
```

- 특정 테이블의 특정 row 데이터 조회
```python
user = db_session.query(User).filter(User.name == 'Kamil Lee').one()
user.email

"""
'parousia0918@gmail.com'
"""
```

- 특정 테이블의 특정 row 데이터 조회(.like / .notlike)
```python
user = db_session.query(User).filter(User.name.like('Lee%')).one()  ### 'Lee~' 로 시작하는 컬럼값(User.name) 조회
user.email

"""
'dipleinelven@naver.com'
"""
```

- 특정 테이블의 특정 row 데이터 변경
```python
user = db_session.query(User).filter(User.id == 1)
user.name = 'Kamil Dowonna'

db_session.commit()

"""
'Kamil Dowonna'
"""
```

- 특정 테이블의 특정 row 데이터 삭제
```python
user = db_session.query(User).filter(User.id == 1).one()
db_session.delete(user)

db_session.commit()

"""

"""
```

- 여러 테이블 간 JOIN() 사용법
```python
class Dept(Base):
    __tablename__ = 'dept'
    deptno = Column(Integer, primary_key=True)
    dname = Column(String(14))
    loc = Column(String(13))
    emp = relationship("Emp", back_populates="dept")

class Emp(Base):
    __tablename__ = 'emp'
    empno = Column(Integer, primary_key=True)
    ename = Column(String(10))
    job = Column(String(9))
    deptno = Column(Integer, ForeignKey(Dept.deptno, ondelete='cascade'))
    dept = relationship('Dept', foreign_keys='Emp.deptno', lazy='joined')

    def __repr__(self):
        return '%s, %s, %s' % (self.empno, self.ename, self.job)

db_session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))
```

```python
e1 = db_session.query(Emp.ename == 'SMITH').one()
e1

"""
SMITH
"""
```

```python
# 'SMITH'의 부서명 및 부서위치 찾기(JOIN())
"""
SELECT dept.DNAME, dept.LOC
	FROM emp
	JOIN dept ON
		emp.DEPTNO = dept.DEPTNO
	WHERE emp.ENAME = 'SMITH';
"""
e1.dept.dname, e1.dept.loc

"""
{'RESEARCH', 'DALLAS'}
"""
```

```python
# 1. loc == 'DALLAS' 부서 정보 조회
# 2. 'DALLAS'에 근무하는 사원들 조회
d1 = db_session.query(Dept).filter(Dept.loc == 'DALLAS').one()
d1.loc, d1.dname

"""
{'DALLAS', 'RESEARCH'}
"""
```

- 역조회 JOIN() 사용법

```python
"""
SELECT emp.ENAME
	FROM emp
	JOIN dept ON
		emp.DEPTNO = dept.DEPTNO
	WHERE dept.LOC = 'DALLAS';
"""
d1.emp

"""
[SMITH, JONES, SCOTT, ADAMS, FORD]
"""
```