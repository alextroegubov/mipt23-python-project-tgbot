from django.db import models  # type: ignore


class User(models.Model):  # type: ignore
    username = models.CharField(
        verbose_name='Никнейм',
        max_length=20
    )
    external_id = models.PositiveIntegerField(
        verbose_name='user ID in telegram',
        unique=True
    )
    reg_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    def __str__(self) -> str:
        return f'Пользователь {self.username}'


class WordRecord(models.Model):  # type: ignore
    user = models.ForeignKey(
        to='bot.User',
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
        default=0,
    )
    en_word = models.CharField(
        verbose_name='Слово (eng)',
        max_length=50
    )
    ru_translation = models.CharField(
        verbose_name='Перевод (ru)',
        max_length=100
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        default=''
    )
    added_at = models.DateTimeField(
        auto_now_add=True
    )


class LessonRecord(models.Model):  # type: ignore
    user = models.ForeignKey(
        to='bot.User',
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
        default=0
    )
    duration = models.IntegerField(
        verbose_name='Длительность'
    )
    date = models.DateTimeField(
        verbose_name='Дата занятия',
        auto_now_add=False
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        default='',
    )


class GameRecord(models.Model):  # type: ignore
    user = models.ForeignKey(
        to='bot.User',
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
        default=0
    )
    date = models.DateTimeField(
        verbose_name='Дата',
        auto_now_add=True
    )
    n_questions = models.PositiveIntegerField(
        verbose_name='Число вопросов',
    )

    n_answers = models.PositiveIntegerField(
        verbose_name='Число вопросов',
    )
