from __future__ import annotations

from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, event, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from orm.database import Base, async_session
from datetime import datetime


class Student(Base):
    __abstract__ = True

    vk_id: Mapped[int]
    full_name: Mapped[str]
    name: Mapped[str]


class AlmostCurator(Student):
    __tablename__ = "AlmostCurator"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_number: Mapped[str]
    birthday_date = Column(DateTime,)
    strikes_number: Mapped[int] = mapped_column(default=0)
    rating: Mapped[float] = mapped_column(default=10)
    inst_or_tg: Mapped[str]
    phone_number: Mapped[str]
    hw_completion: Mapped[bool] = mapped_column(default=True)
    meeting_attendance: Mapped[int] = mapped_column(default=0)
    competition_activity_rate: Mapped[float] = mapped_column(default=10)
    competition_responsibility_rate: Mapped[float] = mapped_column(default=10)
    competition_interactions_rate: Mapped[float] = mapped_column(default=10)
    competition_rules_rate: Mapped[float] = mapped_column(default=10)
    competition_additional_rate: Mapped[float] = mapped_column(default=10)
    belbin_role: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, default=None)

    def __str__(self):
        return f'👤ФИО: [https://vk.com/id{self.vk_id}|{self.full_name}]\n' \
               f'Группа: {self.group_number}\n\n' \
               f'🎂День рождения: {self.birthday_date.strftime("%d.%m.%Y")}\n' \
               f'📱Тг: {self.inst_or_tg}\n' \
               f'📞 Номер телефона: {self.phone_number}\n\n' \
               f'⚠️Количество предупреждений: {self.strikes_number}\n' \
               f'❗Количество пропусков: {self.meeting_attendance}\n'

    def __repr__(self):
        return f'👤ФИО: [https://vk.com/id{self.vk_id}|{self.full_name}]\n' \
               f'Группа: {self.group_number}\n\n' \
               f'🎂День рождения: {self.birthday_date.strftime("%d.%m.%Y")}\n' \
               f'📱Тг: {self.inst_or_tg}\n' \
               f'📞 Номер телефона: {self.phone_number}\n\n' \
               f'🧩Роль Белбина: {self.belbin_role or "—"}\n\n' \
               f'⚠️Количество страйков: {self.strikes_number}\n' \
               f'❗Количество пропусков: {self.meeting_attendance}\n' \
               f'Сделал дз: {"Да✔️" if self.hw_completion else "Нет❌"}\n\n' \
               f'Рейтинг: {self.rating}\n\n' \
               f'Компетенции:\n' \
               f'Активность: {self.competition_activity_rate}\n' \
               f'Ответственность: {self.competition_responsibility_rate}\n' \
               f'Взаимодействия: {self.competition_interactions_rate}\n' \
               f'Соблюдение правил: {self.competition_rules_rate}'


class Competition(Base):
    __abstract__ = True

    iras_rate: Mapped[str] = mapped_column(default='10')
    fedas_rate: Mapped[str] = mapped_column(default='10')
    sashas_rate: Mapped[str] = mapped_column(default='10')
    katyas_rate: Mapped[str] = mapped_column(default='10')
    alinas_rate: Mapped[str] = mapped_column(default='10')
    artems_rate: Mapped[str] = mapped_column(default='10')


class CompetitionActivity(Competition):
    __tablename__ = "CompetitionActivity"

    almost_curator_id: Mapped[int] = mapped_column(ForeignKey("AlmostCurator.id"), primary_key=True)

    ac = relationship(AlmostCurator, cascade='all,delete', backref='competition_activity')

    def __str__(self):
        return f'Оценка Ромы: {self.romki_rate}\n\n' \
               f'Оценка Хипа: {self.iras_rate}\n\n' \
               f'Оценка Вани: {self.katyas_rate}\n\n' \
               f'Оценка Насти: {self.sashas_rate}\n\n' \
               f'Оценка Вики: {self.artems_rate}\n\n' \
               f'Оценка Ани: {self.alinas_rate}'


class CompetitionResponsibility(Competition):
    __tablename__ = "CompetitionResponsibility"

    almost_curator_id: Mapped[int] = mapped_column(ForeignKey("AlmostCurator.id"), primary_key=True)

    ac = relationship(AlmostCurator, cascade='all,delete', backref='competition_responsibility')

    def __str__(self):
       return f'Оценка Ромы: {self.romas_rate}\n\n' \
               f'Оценка Хипа: {self.hips_rate}\n' \
               f'Оценка Вани: {self.ivans_rate}\n' \
               f'Оценка Вики: {self.vikas_rate}\n' \
               f'Оценка Ани: {self.anyas_rate}\n' \
               f'Оценка Насти: {self.nastyas_rate}'


class CompetitionInteractions(Competition):
    __tablename__ = "CompetitionInteractions"

    almost_curator_id: Mapped[int] = mapped_column(ForeignKey("AlmostCurator.id"), primary_key=True)

    ac = relationship(AlmostCurator, cascade='all,delete', backref='competition_interactions')

    def __str__(self):
        return f'Оценка Ромы: {self.romas_rate}\n\n' \
               f'Оценка Хипа: {self.hips_rate}\n' \
               f'Оценка Вани: {self.ivans_rate}\n' \
               f'Оценка Вики: {self.vikas_rate}\n' \
               f'Оценка Ани: {self.anyas_rate}\n' \
               f'Оценка Насти: {self.nastyas_rate}'


class CompetitionRules(Competition):
    __tablename__ = "CompetitionRules"

    almost_curator_id: Mapped[int] = mapped_column(ForeignKey("AlmostCurator.id"), primary_key=True)

    ac = relationship(AlmostCurator, cascade='all,delete', backref='competition_rules')

    def __str__(self):
        return f'Оценка Ромы: {self.romas_rate}\n\n' \
               f'Оценка Хипа: {self.hips_rate}\n' \
               f'Оценка Вани: {self.ivans_rate}\n' \
               f'Оценка Вики: {self.vikas_rate}\n' \
               f'Оценка Ани: {self.anyas_rate}\n' \
               f'Оценка Насти: {self.nastyas_rate}'


class CompetitionAdditional(Competition):
    __tablename__ = "CompetitionAdditional"

    almost_curator_id: Mapped[int] = mapped_column(ForeignKey("AlmostCurator.id"), primary_key=True)

    ac = relationship(AlmostCurator, cascade='all,delete', backref='competition_additional')

    def __str__(self):
        return f'Фидбек Ромы: {self.romas_rate}\n\n' \
               f'Фидбек Хипа: {self.hips_rate}\n' \
               f'Фидбек Вани: {self.ivans_rate}\n' \
               f'Фидбек Вики: {self.vikas_rate}\n' \
               f'Фидбек Ани: {self.anyas_rate}\n' \
               f'Фидбек Насти: {self.nastyas_rate}'


class Deadline(Base):
    __tablename__ = "Deadline"

    id: Mapped[int] = mapped_column(primary_key=True)
    time = Column(DateTime,)
    name: Mapped[str]
    birthday: Mapped[bool] = mapped_column(default=False)

    def __str__(self):
        return f'Название: {self.name}\n\n' \
               f'Срок: {self.time}'


class TeamSplit(Base):
    __tablename__ = "TeamSplit"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    num_teams: Mapped[int]

    members = relationship("TeamSplitMember", cascade="all,delete", back_populates="split")


class TeamSplitMember(Base):
    __tablename__ = "TeamSplitMember"

    id: Mapped[int] = mapped_column(primary_key=True)
    split_id: Mapped[int] = mapped_column(ForeignKey("TeamSplit.id", ondelete="CASCADE"))
    team_index: Mapped[int]
    almost_curator_id: Mapped[int] = mapped_column(ForeignKey("AlmostCurator.id", ondelete="CASCADE"))

    split = relationship("TeamSplit", back_populates="members")
    ac = relationship(AlmostCurator)
