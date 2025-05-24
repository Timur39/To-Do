from sqladmin import ModelView
from src.db.models.user import UserModel
from src.db.models.task import TaskModel
from datetime import datetime, timezone


class UserAdmin(ModelView, model=UserModel):
    name_plural = "Пользователи"
    column_list = [UserModel.id, UserModel.username, UserModel.email]

    # Поиск и фильтрация
    column_searchable_list = [UserModel.username, UserModel.email]
    column_filters = [UserModel.roles]

    # Сортировка
    column_sortable_list = [UserModel.id]

    # Форма создания/редактирования
    form_excluded_columns = [UserModel.id]
    form_widget_args = {
        "email": {"placeholder": "user@example.com"},
        "role": {"choices": ["user", "admin"]},
    }

    # Кастомные действия
    async def on_model_delete(self, model, t):
        if model.roles == "admin":
            raise Exception("Cannot delete admin users!")


class TaskAdmin(ModelView, model=TaskModel):
    name_plural = "Задачи"
    export_max_rows = 1000
    can_export = True
    column_list = [
        TaskModel.id,
        TaskModel.title,
        TaskModel.description,
        TaskModel.priority,
        TaskModel.user_id,
        TaskModel.is_completed,
    ]
    column_searchable_list = [TaskModel.title, TaskModel.description]
    column_sortable_list = [TaskModel.id]
    form_excluded_columns = [TaskModel.id]
    form_args = {
        "created_at": {"default": datetime.now(timezone.utc)},
        "updated_at": {"default": datetime.now(timezone.utc)},
    }
