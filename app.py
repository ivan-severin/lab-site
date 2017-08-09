from app import app, models, database


if __name__ == '__main__':
	database.create_tables([models.Entry, models.FTSEntry], safe=True)
	app.run(debug = True)
