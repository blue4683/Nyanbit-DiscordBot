# 에러 처리

## Discord

```bash
discord.errors.HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body
In 1.options.1: Required options must be placed before non-required options
```

- 필수로 입력되어야 하는 인자는 그렇지 않은 인자보다 먼저 정의되어야한다는 오류이다.
- 문제의 원인은 다음 코드에서 발견할 수 있었다.

```python
async def give(ctx, member: Optional[discord.Member], cnt: int):
```

- `cnt`를 `member` 앞으로 정의해주니 문제는 해결되었다. 하지만 `member`가 필수로 입력되어야 하는 인자이기 때문에 확인해볼 필요가 있었다.
- `Optional`이라는 클래스가 옵션을 선택하게 만들어주는 용도인줄 알았으나 직접 확인해보니 다음과 같은 설명이 있었다.

```python
@_SpecialForm
def Optional(self, parameters):
    """Optional type.

    Optional[X] is equivalent to Union[X, None].
    """
    arg = _type_check(parameters, f"{self} requires a single type.")
    return Union[arg, type(None)]
```

- `Optional[X]`는 `Union[X, None]`과 같다 == `Optional`은 `None`을 허용한다 == 입력이 필요없는 인자다.
- `Optional`을 제거해도 슬래시 명령어에서 똑같이 멤버를 선택해서 입력할 수 있었다.
- 수정한 코드는 다음과 같다.

```python
async def give(ctx, member: discord.Member, cnt: int):
```

---

- 슬래시 명령어 `args`의 `description`을 설정하고 싶어서 다음과 같이 작성했다.

```python
@bot.hybrid_command(name="유저추가", description="등록되지 않은 유저를 추가합니다.")
@app_commands.describe(
    member='등록할 유저를 선택해주세요.',
)
async def add(ctx, member: discord.Member):
```

- 명령어의 설명까지는 바뀌었으나 `args`의 설명은 반영되지 않았다.
- `app_commands.describe`의 설명을 보니 `Union[str, locale_str]`를 인자로 받고 있는데 여기서 `str`은 변수 이름을(여기서는 `member`), `locale_str`은 `description`을 의미한다.
- `locale_str`의 설명을 보면 다음과 같다.

```
Marks a string as ready for translation.

This is done lazily and is not actually translated until :meth:`CommandTree.sync` is called.

The sync method then ultimately defers the responsibility of translating to the :class:`Translator`
instance used by the :class:`CommandTree`. For more information on the translation flow, see the
:class:`Translator` documentation.
```

- 요약하자면, 문자열을 나타내는데 `lazy`하게 수행하고, 실제로 `CommandTree.sync`가 호출되지 않으면 번역되지 않는다고 되어있다.
- 해결을 위해 깃허브 Repo의 Q&A를 살펴보다 다음과 같은 함수로 동기화를 시킬 수 있음을 확인할 수 있었다.

```python
@bot.command()
@commands.is_owner()  # Prevent other people from using the command
async def sync_tree(ctx: commands.Context) -> None:
    """Sync app commands to Discord."""
    await ctx.bot.tree.sync()
    await ctx.send('Application commands synchronized!')
```

- 디스코드 채팅에서 `/sync_tree`을 입력하면 동기화가 된다.
- 동기화 후에 디스코드 앱을 재시작하면 제대로 반영됨을 확인할 수 있었다.

## DB

### Pymysql

```bash
TypeError: %d format: a real number is required, not str
```

- 오류가 발생한 쿼리문은 다음과 같다.

```python
sql = '''
INSERT INTO userinfo (user_id, user_name) VALUES (%s, %s);
INSERT INTO nyanbit (user_id, nyanbit_cnt) VALUES (%s, %d);
'''
```

- SQL에서의 `%s`는 파이썬의 문자열 포맷터가 아닌 `placeholder` 역할을 한다.
- 쿼리문에서는 정수 또는 실수를 넣기 위해 `%d, %f`를 사용하는 것이 아닌 `%s`로 통일해서 사용한다.
- 바꾼 쿼리문은 다음과 같다.

```python
sql = '''
INSERT INTO userinfo (user_id, user_name) VALUES (%s, %s);
INSERT INTO nyanbit (user_id, nyanbit_cnt) VALUES (%s, %s);
'''
```

---

```bash
1064, "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'sql문'"
```

- 여러 개의 쿼리문을 동시에 처리하고 싶어 다음과 같이 쿼리문을 정의했다.

```python
sql = '''
INSERT INTO userinfo (user_id, user_name) VALUES (%s, %s);
INSERT INTO nyanbit (user_id, nyanbit_cnt) VALUES (%s, %s);
'''
```

- Pymysql 모듈은 다음과 같이 선언했다.

```python
self.conn = pymysql.connect(
    host=self.host, user=self.user, password=self.password,
    db=self.db, port=self.port, charset=self.charset)
```

- 문제는 이렇게 선언한 모듈은 기본적으로 멀티쿼리를 지원하지 않는다.
- 멀티쿼리를 지원하는 옵션을 활성화시키기 위해 `pymysql.connect`의 client_flag 파라미터에 다음을 추가해준다.

```python
from pymysql.constants import CLIENT

CLIENT.MULTI_STATEMENTS
```

- 추가해준 선언문은 다음과 같다.

```python
self.conn = pymysql.connect(
    host=self.host, user=self.user, password=self.password,
    db=self.db, port=self.port, charset=self.charset, client_flag=CLIENT.MULTI_STATEMENTS)
```
