from django.db import models
from jsonfield import JSONField
from django_enumfield import enum


class Rank(enum.Enum):
    RANK_1 = 1
    RANK_2 = 1
    RANK_3 = 2


class Section(models.Model):
    name = models.CharField(max_length=30)

    @classmethod
    def create(cls, name, layout):
        cls.layout = layout
        sect = cls(name=name)
        return sect

    def save(self, **kwargs):
        super().save(self, kwargs)
        for row_num, row in enumerate(self.layout):
            for seq_num, (seat_rank, seat_num) in enumerate(row):
                Seat(rank=seat_rank,
                     seq_num=seq_num,
                     row_num=row_num,
                     seat_num=seat_num,
                     section=self).save()

    def get_layout(self):
        layout = []
        row_nums = self.seat_set.values("row_num").distinct()
        for row_dict in row_nums:
            layout.append(list(self.seat_set.all().filter(row_num=row_dict["row_num"])))
        return layout


class Seat(models.Model):
    class Meta:
        unique_together = (('seat_num', 'row_num', 'section'),)

    rank = enum.EnumField(Rank)
    seq_num = models.IntegerField()
    seat_num = models.IntegerField()
    row_num = models.IntegerField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE)


class Allocation(models.Model):
    class Meta:
        unique_together = (('name', 'section'),)

    name = models.CharField(max_length=30)
    allocation = JSONField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
