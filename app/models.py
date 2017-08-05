from app import flask_db, database
import datetime


from playhouse.sqlite_ext import *

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