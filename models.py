from google.appengine.ext import ndb

class User(ndb.Model):
	user_id = ndb.StringProperty()
	user_email = ndb.StringProperty()
	nickname = ndb.StringProperty()
	auth_domain = ndb.StringProperty()
	federated_identity = ndb.StringProperty()
	federated_provider = ndb.StringProperty()
	created = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def get_all(cls):
		return User.query()

