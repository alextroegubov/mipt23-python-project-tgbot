""" Admin module"""

from django.contrib import admin  # type: ignore
from .models import WordRecord, LessonRecord, User, GameRecord


@admin.register(WordRecord)
class WordRecordAdmin(admin.ModelAdmin):  # type: ignore
    """word record admin"""
    list_display = ('id', 'en_word', 'ru_translation', 'comment')


@admin.register(LessonRecord)
class LessonRecordAdmin(admin.ModelAdmin):  # type: ignore
    """lesson record admin"""
    list_display = ('id', 'user', 'duration', 'comment')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):  # type: ignore
    """user admin"""
    list_display = ('id', 'external_id', 'username', 'reg_at')


@admin.register(GameRecord)
class GameRecordAdmin(admin.ModelAdmin):  # type: ignore
    """game record admin"""
    list_display = ('id', 'user', 'date', 'n_questions', 'n_answers')
