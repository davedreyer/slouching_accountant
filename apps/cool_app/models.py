from __future__ import unicode_literals

from django.db import models
from ..log_reg.models import User

class PokeManager(models.Manager):	
	def poke_query(self, id):

		response = {}
		
		user_info = []

		res = User.objects.exclude(id=id)

		for y in res:

			dict= {}

			dict['name'] = y.name
			dict['alias'] = y.alias
			dict['id'] = y.id
			dict['email'] = y.email

			count = Poke.objects.filter(pokee=y.id).count()

			dict['count'] = count

			user_info.append(dict)

		response['user_info'] = user_info	

		poker_id = []
		
		poker_query = Poke.objects.filter(pokee=id)

		for z in poker_query :

			poker_id.append(z.poker.id)

		poker_count = len(list(set(poker_id)))

		response['poker_count'] = poker_count

		return response

class Poke(models.Model):
	poker=models.ForeignKey(User, related_name="poker")
	pokee=models.ForeignKey(User, related_name="pokee")
	created_at = models.DateTimeField(auto_now_add = True)
	objects = PokeManager()