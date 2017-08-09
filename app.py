from app import app, models, database



def create_tables():
		# database.connect()
		database.create_tables([models.User, models.Entry, models.FTSEntry], safe=True)
if __name__ == '__main__':

	create_tables()
	app.run(debug = True)
