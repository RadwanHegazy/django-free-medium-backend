from rest_framework import serializers
from uuid import uuid4
from globals.scrapper import ArabicFredium
from app import tasks

class URLSerializer (serializers.Serializer) : 
    link = serializers.URLField()
    email = serializers.EmailField()
    lang = serializers.ChoiceField(choices=(
        ('ar','ar'),
        ('en','en'),
    ))

    def validate(self, attrs):
        data = super().validate(attrs)

        self.link = data['link']
        self.lang = data['lang']
        self.email = data['email']

        if "@gmail.com" not in self.email : 
            raise serializers.ValidationError({'message':'invalid gmail'})

        return data
    

    def start (self) : 

        # start celery task
        tasks.StartTask.delay(email=self.email,link=self.link,lang=self.lang)

    