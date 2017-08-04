from app import app, models, database
database.create_tables([models.Entry, models.FTSEntry], safe=True)
app.run(debug = True)
