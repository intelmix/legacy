from peewee import *
from yeksatr.backend.helpers.setting import Setting

database = Setting.database
class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class UserGroup(BaseModel):
    title = CharField(max_length=50)

    class Meta:
        db_table = 'tbl_user_group'

class User(BaseModel):
    birthdate = DateTimeField(null=True)
    email = CharField(max_length=75)
    familly = CharField(max_length=70, null=True)
    fk_group = ForeignKeyField(db_column='fk_group_id', null=True, rel_model=UserGroup, to_field='id')
    gender = IntegerField(null=True)
    job = CharField(max_length=120, null=True)
    mobile_number = CharField(max_length=15, null=True)
    name = CharField(max_length=50, null=True)
    password = CharField(max_length=45)
    register_date = DateTimeField()
    username = CharField(max_length=80)
    reset_password_key = CharField(max_length=32)
    reset_password_request_date = DateTimeField(null=True)
    
    class Meta:
        db_table = 'tbl_user'

class Bulletin(BaseModel):
    fk_user = ForeignKeyField(db_column='fk_user_id', null=True, rel_model=User, to_field='id')
    recipient_email = CharField(max_length=50, null=True)
    title = CharField(max_length=50)

    class Meta:
        db_table = 'tbl_bulletin'

class Source(BaseModel):
    icon = CharField(max_length=45)
    title = CharField(max_length=45)
    url = CharField(max_length=45)

    class Meta:
        db_table = 'tbl_source'

class BulletinFilter1(BaseModel):
    date1 = IntegerField()
    date2 = IntegerField()
    date_op = IntegerField()
    fk_bulletin = ForeignKeyField(db_column='fk_bulletin_id', rel_model=Bulletin, to_field='id')
    fk_source = ForeignKeyField(db_column='fk_source_id', rel_model=Source, to_field='id')
    query_text = CharField(max_length=100)

    class Meta:
        db_table = 'tbl_bulletin_filter1'

class BulletinSchedule(BaseModel):
    day_of_month = IntegerField()
    day_of_week = IntegerField()
    fk_bulletin = ForeignKeyField(db_column='fk_bulletin', rel_model=Bulletin, to_field='id')
    hour = IntegerField()
    minute = IntegerField()
    occurence = IntegerField()

    class Meta:
        db_table = 'tbl_bulletin_schedule'

class Category(BaseModel):
    title = CharField(max_length=50)

    class Meta:
        db_table = 'tbl_category'

class CrawlLog(BaseModel):
    crawl_date = DateTimeField()
    news_count = IntegerField()

    class Meta:
        db_table = 'tbl_crawl_log'

class Feed(BaseModel):
    fk_source = ForeignKeyField(db_column='fk_source_id', rel_model=Source, to_field='id')
    title = CharField(max_length=45)
    url = CharField(max_length=45)

    class Meta:
        db_table = 'tbl_feed'

class News(BaseModel):
    extracted = IntegerField(null=True)
    fetch_date = DateTimeField()
    fk_feed = ForeignKeyField(db_column='fk_feed_id', rel_model=Feed, to_field='id')
    publish_date = DateTimeField()
    title = CharField(max_length=4000)
    url = CharField(max_length=2000)
    url_hash = CharField(max_length=45)

    class Meta:
        db_table = 'tbl_news'

class NewsContent(BaseModel):
    fk_news = ForeignKeyField(db_column='fk_news_id', rel_model=News, to_field='id')
    html_content = TextField()
    text_content = TextField()

    class Meta:
        db_table = 'tbl_news_content'

class SourceCategory(BaseModel):
    fk_category = ForeignKeyField(db_column='fk_category_id', rel_model=Category, to_field='id')
    fk_source = ForeignKeyField(db_column='fk_source_id', rel_model=Source, to_field='id')

    class Meta:
        db_table = 'tbl_source_category'

class SourceTag(BaseModel):
    fk_source = ForeignKeyField(db_column='fk_source_id', rel_model=Source, to_field='id')
    tag_class = CharField(max_length=450, null=True)
    tag = CharField(db_column='tag_id', max_length=450, null=True)
    tag_name = CharField(max_length=45, null=True)

    class Meta:
        db_table = 'tbl_source_tag'

class UserNews(BaseModel):
    edit_date = DateTimeField()
    fk_news = ForeignKeyField(db_column='fk_news_id', rel_model=Source, to_field='id')
    fk_user = ForeignKeyField(db_column='fk_user_id', rel_model=User, to_field='id')
    is_flagged = IntegerField()
    is_starred = IntegerField()
    news_content = TextField()
    publish_date = DateTimeField()
    tags = TextField()
    title = CharField(max_length=50)

    class Meta:
        db_table = 'tbl_user_news'

class UserVerify(BaseModel):
    fk_user = ForeignKeyField(db_column='fk_user_id', rel_model=User, to_field='id')
    verification_code = CharField(max_length=100)
    verification_type = IntegerField()

    class Meta:
        db_table = 'tbl_user_verify'


class Feedback(BaseModel):
    fk_user = ForeignKeyField(db_column='fk_user_id', rel_model=User, to_field='id')
    contents = TextField()
    submit_date = DateTimeField()

    class Meta:
        db_table = 'tbl_feedback'
