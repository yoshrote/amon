from time import time
from amon.api.models import LogsAPIModel, CommonAPIModel

class Log(object):

	def __init__(self):
		self.model = LogsAPIModel()
		self.common_model = CommonAPIModel()

	# Checks the tags in the database and adds them if they are new entries
	def check_tags(self, tags):

		if isinstance(tags, list):
			for el in tags:
				self.model.upsert_tag(el)
						
		elif isinstance(tags, str) or isinstance(tags, unicode):
			self.model.upsert_tag(tags)

	def __call__(self, *args, **kwargs):

		log_dict = args[0]

		try:
			tags = log_dict.get('tags')
		except: 
			tags = None
		
		message = log_dict.get('message', '')

		now = int(time())

		self.check_tags(tags)

		entry = {'time': now, 'message': message, 'tags': tags}
		
		# Add the data to a separate field, for easy searching 
		# TODO - support for dictionaries with more than 1 level
		if isinstance(message, dict):
			_searchable = ":".join(message.keys())
		elif isinstance(message, list):
			_searchable = ":".join(["%s" % el for el in message])
		else:
			_searchable = message
		
		entry['_searchable'] = _searchable

		self.model.save_log(entry)
		self.common_model.upsert_unread('logs')
