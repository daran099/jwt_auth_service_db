from db.base import Base
from db.session import engine
import models

Base.metadata.create_all(engine)
