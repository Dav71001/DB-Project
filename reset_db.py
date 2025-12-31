from app.database import engine, Base
from app.models import apartment_models

print("Удаление старых таблиц...")
Base.metadata.drop_all(bind=engine)
print("Создание новых таблиц...")
Base.metadata.create_all(bind=engine)
print("Готово! База данных синхронизирована с моделями.")
