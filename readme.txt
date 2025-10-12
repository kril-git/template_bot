Для развертывания проекта на другой компютер нужно создать папки
filis
logs




pip freeze > requirements.txt



alembic revision --message="Initial" --autogenerate

alembic upgrade head

sqlalchemy.url = postgresql://postgres:postgres@192.168.100.53/sa -> alembric.ini

target_metadata = models.Base.metadata  -> env.pyc

# Удалить инлайн клавиатуру
await callback.message.edit_reply_markup(reply_markup=None)
await callback.message.delete_reply_markup()
