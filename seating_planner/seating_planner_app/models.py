from django.db import models
from jsonfield import JSONField
from django_enumfield import enum


class Rank(enum.Enum):
    RANK_1 = 1
    RANK_2 = 1
    RANK_3 = 2


class Extra(enum.Enum):
    NONE = 1
    AISLE = 2
    FRONT_ROW = 3
    HIGH_SEAT = 4


class Section(models.Model):
    name = models.CharField(max_length=30, unique=True)

    @classmethod
    def create(cls, name, layout):
        cls.layout_template = layout
        sect = cls(name=name)
        return sect

    def save(self, **kwargs):
        super().save(self, kwargs)
        for row_num, row in enumerate(self.layout_template):
            for seq_num, tuple in enumerate(row):
                if len(tuple) == 2:
                    seat_rank, seat_num = tuple
                    extra = Extra.NONE
                else:
                    seat_rank, seat_num, extra = tuple

                Seat(rank=seat_rank,
                     extra=extra,
                     seq_num=seq_num,
                     row_num=row_num,
                     seat_num=seat_num,
                     section=self).save()

    @property
    def layout(self):
        layout = []
        row_nums = self.seat_set.values("row_num").distinct()
        for row_dict in row_nums:
            layout.append(list(self.seat_set.order_by("seq_num").filter(row_num=row_dict["row_num"])))
        return layout


class Seat(models.Model):
    class Meta:
        unique_together = (('seat_num', 'row_num', 'section'),)

    rank = enum.EnumField(Rank)
    extra = enum.EnumField(Extra)
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
