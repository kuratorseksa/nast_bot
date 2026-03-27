from vkbottle import BuiltinStateDispenser, CtxStorage, KeyboardButtonColor, PhotoMessageUploader, DocMessagesUploader
from vkbottle.framework.labeler import BotLabeler
from orm.models import CompetitionRules, CompetitionInteractions, CompetitionAdditional, CompetitionResponsibility, \
    CompetitionActivity, AlmostCurator
from global_variables.token import api
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

state_dispenser = BuiltinStateDispenser()
labeler = BotLabeler()
ctx = CtxStorage()
deadline_scheduler = AsyncIOScheduler()
photo_uploader = PhotoMessageUploader(api)
doc_uploader = DocMessagesUploader(api)

user_accounting = set()

green = KeyboardButtonColor.POSITIVE
red = KeyboardButtonColor.NEGATIVE
blue = KeyboardButtonColor.PRIMARY

predsed_team_ids = [394608204, 520276059, 366048560, 466100052, 478135965, 348082199]


comp_dict = {'activity': [CompetitionActivity, 'competition_activity_rate'],
             'responsibility': [CompetitionResponsibility, 'competition_responsibility_rate'],
             'additional': [CompetitionAdditional, 'competition_additional_rate'],
             'interactions': [CompetitionInteractions, 'competition_interactions_rate'],
             'rules': [CompetitionRules, 'competition_rules_rate']
             }

top_tags_dict = {'По страйкам': 'strikes_number',
                 'По рейтингу': 'rating',
                 'По пропускам': 'meeting_attendance'
                 }

predsed_team_dict = {
    '394608204': 'romas_rate',
    '520276059': 'ivans_rate',
    '366048560': 'vikas_rate',
    '466100052': 'nastyas_rate',
    '478135965': 'hips_rate',
    '348082199': 'anyas_rate'
}
