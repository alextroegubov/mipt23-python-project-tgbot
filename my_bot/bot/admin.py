from django.contrib import admin  # type: ignore

# Register your models here.
from .models import WordRecord, LessonRecord, User, GameRecord


@admin.register(WordRecord)
class WordRecordAdmin(admin.ModelAdmin):  # type: ignore
    list_display = ('id', 'en_word', 'ru_translation', 'comment')


@admin.register(LessonRecord)
class LessonRecordAdmin(admin.ModelAdmin):  # type: ignore
    list_display = ('id', 'user', 'duration', 'comment')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):  # type: ignore
    list_display = ('id', 'external_id', 'username', 'reg_at')


@admin.register(GameRecord)
class GameRecordAdmin(admin.ModelAdmin):  # type: ignore
    list_display = ('id', 'user', 'date', 'n_questions', 'n_answers')
