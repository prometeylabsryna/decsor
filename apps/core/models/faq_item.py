"""FaqItem — question/answer entries for the F.A.Q. page."""
from django.db import models


class FaqItem(models.Model):
    question = models.CharField("Питання", max_length=255)
    answer = models.TextField("Відповідь")
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активне", default=True)

    class Meta:
        verbose_name = "Питання F.A.Q."
        verbose_name_plural = "F.A.Q. — Часті питання"
        ordering = ["order"]

    def __str__(self):
        return self.question
