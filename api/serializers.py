# api/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Campaign, Donation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CampaignSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = [
            'id',
            'creator',
            'title',
            'description',
            'goal_amount',
            'raised_amount',
            'image',
            'created_at',
            'progress',
        ]

    def get_progress(self, obj):
        """Return progress percentage of campaign."""
        if obj.goal_amount > 0:
            return int((obj.raised_amount / obj.goal_amount) * 100)
        return 0


class DonationSerializer(serializers.ModelSerializer):
    donor = UserSerializer(read_only=True)

    class Meta:
        model = Donation
        fields = ['id', 'campaign', 'donor', 'amount', 'donated_at']
        read_only_fields = ['donor']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['donor'] = request.user
        return super().create(validated_data)
