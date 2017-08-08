from app import flask_db, database
import datetime


from playhouse.sqlite_ext import *


class User(flask_db.Model):
    ''' the user model specifies its fields (or columns) declaratively, like django'''
    username = CharField(unique=True)
    password = CharField()
    email = CharField()
    join_date = DateTimeField()

    class Meta:
        order_by = ('username',)



class Relationship(flask_db.Model):
    ''' this model contains two foreign keys to user -- it essentially allows us to
        model a "many-to-many" relationship between users.  by querying and joining
        on different columns we can expose who a user is "related to" and who is
        "related to" a given user 
    '''
    from_user = ForeignKeyField(User, related_name='relationships')
    to_user = ForeignKeyField(User, related_name='related_to')

    # class Meta:
    #     indexes = (
    #         # Specify a unique multi-column index on from/to-user.
    #         (('from_user', 'to_user'), True),
    #     )

class Message(flask_db.Model):
    ''' a dead simple one-to-many relationship: one user has 0..n messages, exposed by
        the foreign key.  because we didn't specify, a users messages will be accessible
        as a special attribute, User.message_set
    '''
    user = ForeignKeyField(User)
    content = TextField()
    pub_date = DateTimeField()

    # class Meta:
    #     order_by = ('-pub_date',)

class Entry(flask_db.Model):
    title = CharField()
    slug = CharField(unique=True)
    content = TextField()
    published = BooleanField(index=True)
    timestamp = DateTimeField(default=datetime.datetime.now, index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = re.sub('[^\w]+', '-', self.title.lower())
        ret = super(Entry, self).save(*args, **kwargs)

        # Store search content.
        self.update_search_index()
        return ret

    def update_search_index(self):
        try:
            fts_entry = FTSEntry.get(FTSEntry.entry_id == self.id)
        except FTSEntry.DoesNotExist:
            fts_entry = FTSEntry(entry_id=self.id)
            force_insert = True
        else:
            force_insert = False
        fts_entry.content = '\n'.join((self.title, self.content))
        fts_entry.save(force_insert=force_insert)
    
    @classmethod
    def public(cls):
        return Entry.select().where(Entry.published == True)

    @classmethod
    def search(cls, query):
        words = [word.strip() for word in query.split() if word.strip()]
        if not words:
            # Return empty query.
            return Entry.select().where(Entry.id == 0)
        else:
            search = ' '.join(words)

        return (FTSEntry
                .select(
                    FTSEntry,
                    Entry,
                    FTSEntry.rank().alias('score'))
                .join(Entry, on=(FTSEntry.entry_id == Entry.id).alias('entry'))
                .where(
                    (Entry.published == True) &
                    (FTSEntry.match(search)))
                .order_by(SQL('score').desc()))



class FTSEntry(FTSModel):
    entry_id = IntegerField()
    content = TextField()

    class Meta:
        database = database