from rest_framework import serializers
from .models import User, Novel, Chapter, Comment, RechargeRecord, Announcement

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'balance', 'created_at', 'is_active', 'role']

class NovelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Novel
        fields = '__all__'

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    replies = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_name', 'novel', 'content', 'created_at', 'replies']
    def get_replies(self, obj):
        # 递归获取所有回复
        return CommentSerializer(obj.replies.all().order_by('created_at'), many=True).data

class RechargeRecordSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = RechargeRecord
        fields = ['id', 'user', 'username', 'amount', 'bonus', 'recharge_time', 'status']

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__' 