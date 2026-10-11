try:
    import fastapi
    print(f"fastapi: {fastapi.__version__}")
except ImportError:
    print("fastapi: NOT INSTALLED")

try:
    import sqlalchemy
    print(f"sqlalchemy: {sqlalchemy.__version__}")
except ImportError:
    print("sqlalchemy: NOT INSTALLED")

try:
    import aiomysql
    print("aiomysql: OK")
except ImportError:
    print("aiomysql: NOT INSTALLED")

try:
    import pydantic
    print(f"pydantic: {pydantic.__version__}")
except ImportError:
    print("pydantic: NOT INSTALLED")
