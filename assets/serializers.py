# _*_coding:utf-8_*_

from rest_framework import serializers

from assets import models
from assets.myauth import UserProfile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('url', 'name', 'email')


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Asset
        depth = 2
        fields = ('name', 'sn', 'server', 'networkdevice')


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Server
        fields = '__all__'
