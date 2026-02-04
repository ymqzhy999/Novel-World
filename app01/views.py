from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Novel, Chapter, Comment, SearchHistory, RechargeRecord, PurchaseRecord, Bookshelf, Announcement
from .serializers import UserSerializer, NovelSerializer, ChapterSerializer, CommentSerializer, RechargeRecordSerializer, AnnouncementSerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.permissions import AllowAny, IsAdminUser
from decimal import Decimal
from rest_framework.parsers import JSONParser
from django.db.models import Sum, Count
from django.db import models
import redis
import json

# Redis 连接配置
# 请根据您的实际 Redis 服务器地址和端口进行修改
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Create your views here.

class UserInfoView(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        if user_id:
            user = User.objects.get(id=user_id)
        else:
            user = User.objects.first()
        return Response(UserSerializer(user).data)

class NovelListView(APIView):
    def get(self, request):
        # 尝试从 Redis 缓存中获取数据
        cache_key = 'novel_list_cache'
        cached_data = redis_client.get(cache_key)

        if cached_data:
            print("从 Redis 缓存中获取小说列表")
            return Response(json.loads(cached_data))

        # 如果缓存中没有，则从数据库中获取
        novels = Novel.objects.all().order_by('-created_at')
        serializer = NovelSerializer(novels, many=True)
        data = serializer.data

        # 将数据存入 Redis 缓存，设置过期时间为 60 秒
        redis_client.setex(cache_key, 60, json.dumps(data))
        print("将小说列表存入 Redis 缓存")
        return Response(data)

class ChapterListView(APIView):
    def get(self, request, novel_id):
        chapters = Chapter.objects.filter(novel_id=novel_id).order_by('id')
        return Response(ChapterSerializer(chapters, many=True).data)

class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username)
            if not user.is_active:
                return Response({'success': False, 'msg': '账号已被封禁'}, status=status.HTTP_403_FORBIDDEN)
            if user.password == password:
                return Response({'success': True, 'user': {
                    'id': user.id, 'username': user.username, 'email': user.email, 'balance': user.balance,
                    'is_admin': user.is_admin, 'role': user.role
                }})
            else:
                return Response({'success': False, 'msg': '密码错误'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'success': False, 'msg': '用户不存在'}, status=status.HTTP_400_BAD_REQUEST)

class UserRegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            return Response({'success': False, 'msg': '用户名已存在'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'success': False, 'msg': '邮箱已注册'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(username=username, email=email, password=password)
        return Response({'success': True, 'user': {
            'id': user.id, 'username': user.username, 'email': user.email, 'balance': user.balance
        }})

class CommentListCreateView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, novel_id):
        comments = Comment.objects.filter(novel_id=novel_id, parent=None).order_by('-created_at')
        # 只返回一级评论，前端可递归渲染回复
        return Response(CommentSerializer(comments, many=True).data)
    def post(self, request, novel_id):
        user_id = request.data.get('user_id')
        content = request.data.get('content')
        parent_id = request.data.get('parent')
        if not user_id or not content:
            return Response({'success': False, 'msg': '参数不完整'}, status=400)
        comment = Comment.objects.create(
            user_id=user_id,
            novel_id=novel_id,
            content=content,
            parent_id=parent_id if parent_id else None
        )
        return Response({'success': True, 'comment': CommentSerializer(comment).data})

class UserCommentsView(APIView):
    def get(self, request, user_id):
        comments = Comment.objects.filter(user_id=user_id).order_by('-created_at')
        result = []
        for c in comments:
            try:
                novel = Novel.objects.get(id=c.novel_id)
                novel_title = novel.title
            except:
                novel_title = '未知小说'
            result.append({
                'id': c.id,
                'novel_title': novel_title,
                'content': c.content,
                'created_at': c.created_at
            })
        return Response(result)

class AddHistoryView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        keyword = request.data.get('keyword')  # 存小说id
        if not user_id or not keyword:
            return Response({'success': False, 'msg': '参数不完整'}, status=400)
        SearchHistory.objects.create(user_id=user_id, keyword=keyword)
        return Response({'success': True})

class UserHistoryView(APIView):
    def get(self, request, user_id):
        history = SearchHistory.objects.filter(user_id=user_id).order_by('-search_time')
        result = []
        for h in history:
            try:
                novel = Novel.objects.get(id=h.keyword)
                novel_title = novel.title
                novel_id = novel.id
            except:
                novel_title = h.keyword
                novel_id = h.keyword
            result.append({
                'id': h.id,
                'novel_id': novel_id,
                'novel_title': novel_title,
                'search_time': h.search_time
            })
        return Response(result)


class RechargeView(APIView):
    # 1. 加上权限控制，必须登录才能访问
    # (需要在 settings.py 配置 REST_FRAMEWORK 的 DEFAULT_PERMISSION_CLASSES，或者这里显式加)
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        # 🛡️ 修复 Bug 2：不再信前端传的 user_id，而是从当前登录用户取
        # 注意：这需要你配置好了 JWT 或 Session 认证，request.user 才有值
        # 如果你暂时没配认证，先保留 request.data.get('user_id') 但要清楚这是隐患
        user = request.user

        # 如果还没配认证，暂时用原来的，但逻辑上要明白这是错的
        if not user or user.is_anonymous:
            # 为了兼容你现在的代码，暂时还从 data 取，但生产环境绝对不行！
            user_id = request.data.get('user_id')
            user = User.objects.get(id=user_id)

        try:
            amount_str = request.data.get('amount')
            amount = Decimal(str(amount_str))

            # 🛡️ 修复 Bug 1：必须是正数
            if amount <= 0:
                return Response({'success': False, 'msg': '充值金额必须大于0'}, status=400)

            # 🛡️ 修复 Bug 3：Bonus 由后端说了算，完全忽略前端传的 bonus
            bonus = Decimal('0')
            if amount >= 5000:
                bonus = Decimal('1000')
            elif amount >= 2000:
                bonus = Decimal('350')
            elif amount >= 1000:
                bonus = Decimal('150')
            elif amount >= 500:
                bonus = Decimal('60')
            elif amount >= 300:
                bonus = Decimal('30')

            # 创建记录 (注意：这里不再接收 request.data.get('bonus'))
            RechargeRecord.objects.create(user=user, amount=amount, bonus=bonus)

            return Response({'success': True, 'msg': '充值申请已提交，实际赠送以系统计算为准'})

        except Exception as e:
            return Response({'success': False, 'msg': str(e)}, status=400)

class RechargeApproveView(APIView):
    # 这里建议用更完善的权限校验，暂用IsAdminUser或自定义
    def post(self, request):
        recharge_id = request.data.get('recharge_id')
        approve = request.data.get('approve')
        try:
            record = RechargeRecord.objects.get(id=recharge_id)
            if record.status != 'pending':
                return Response({'success': False, 'msg': '该记录已审核'})
            if approve:
                record.status = 'approved'
                record.user.balance += record.amount + record.bonus
                record.user.save()
            else:
                record.status = 'rejected'
            record.save()
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'msg': str(e)}, status=400)

class UnlockChapterView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        chapter_id = request.data.get('chapter_id')
        try:
            user = User.objects.get(id=user_id)
            chapter = Chapter.objects.get(id=chapter_id)
            # 检查是否已购买
            if PurchaseRecord.objects.filter(user=user, chapter=chapter).exists():
                return Response({'success': True, 'msg': '已解锁', 'balance': user.balance})
            # 检查余额
            if user.balance < Decimal('10'):
                return Response({'success': False, 'msg': '余额不足'})
            # 扣费并记录
            user.balance -= Decimal('10')
            user.save()
            PurchaseRecord.objects.create(user=user, chapter=chapter, price=Decimal('10'))
            return Response({'success': True, 'msg': '解锁成功', 'balance': user.balance})
        except Exception as e:
            return Response({'success': False, 'msg': str(e)}, status=400)

class RechargeRecordListView(APIView):
    def get(self, request):
        records = RechargeRecord.objects.all().order_by('-recharge_time')
        return Response(RechargeRecordSerializer(records, many=True).data)

class NovelManageView(APIView):
    parser_classes = [JSONParser]
    def get(self, request):
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        novels = Novel.objects.all().order_by('-created_at')
        total = novels.count()
        start = (page - 1) * page_size
        end = start + page_size
        data = NovelSerializer(novels[start:end], many=True).data
        return Response({'total': total, 'results': data})
    def post(self, request):
        data = request.data
        novel = Novel.objects.create(
            title=data.get('title'),
            author=data.get('author'),
            description=data.get('description',''),
            cover_url=data.get('cover_url',''),
            category=data.get('category',''),
            content=data.get('content','')
        )
        return Response(NovelSerializer(novel).data)
    def put(self, request):
        data = request.data
        novel = Novel.objects.get(id=data.get('id'))
        for field in ['title','author','description','cover_url','category','content']:
            if field in data:
                setattr(novel, field, data[field])
        novel.save()
        return Response(NovelSerializer(novel).data)
    def delete(self, request):
        novel_id = request.data.get('id')
        try:
            novel = Novel.objects.get(id=novel_id)
            novel.delete()
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'msg': str(e)}, status=400)

class UserManageView(APIView):
    parser_classes = [JSONParser]
    def get(self, request):
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        users = User.objects.filter(role='user').order_by('-created_at')
        total = users.count()
        start = (page - 1) * page_size
        end = start + page_size
        data = UserSerializer(users[start:end], many=True).data
        return Response({'total': total, 'results': data})
    def put(self, request):
        user = User.objects.get(id=request.data.get('id'))
        if 'is_admin' in request.data:
            user.is_admin = request.data['is_admin']
        if 'role' in request.data:
            user.role = request.data['role']
        if 'disabled' in request.data:
            user.is_active = not request.data['disabled']
        user.save()
        return Response(UserSerializer(user).data)
    def delete(self, request):
        user_id = request.data.get('id')
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({'success': True})
        except Exception as e:
            return Response({'success': False, 'msg': str(e)}, status=400)

class BookshelfAddView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        novel_id = request.data.get('novel_id')
        if not user_id or not novel_id:
            return Response({'success': False, 'msg': '参数不完整'}, status=400)
        if Bookshelf.objects.filter(user_id=user_id, novel_id=novel_id).exists():
            return Response({'success': True, 'msg': '已收藏'})
        Bookshelf.objects.create(user_id=user_id, novel_id=novel_id)
        return Response({'success': True})

class BookshelfRemoveView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        novel_id = request.data.get('novel_id')
        Bookshelf.objects.filter(user_id=user_id, novel_id=novel_id).delete()
        return Response({'success': True})

class BookshelfCheckView(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        novel_id = request.GET.get('novel_id')
        collected = Bookshelf.objects.filter(user_id=user_id, novel_id=novel_id).exists()
        return Response({'collected': collected})

class BookshelfListView(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response([], status=200)
        bookshelf = Bookshelf.objects.filter(user_id=user_id)
        novels = []
        for item in bookshelf:
            novel = item.novel
            novels.append({
                'id': novel.id,
                'novel_id': novel.id,
                'title': novel.title,
                'author': novel.author,
                'cover_url': novel.cover_url,
                # 可扩展更多字段
            })
        return Response(novels)

class UserRechargeMessagesView(APIView):
    def get(self, request, user_id):
        records = RechargeRecord.objects.filter(user_id=user_id).order_by('-recharge_time')
        result = []
        for r in records:
            if r.status == 'pending':
                msg = f"您于{r.recharge_time:%Y-%m-%d %H:%M}提交了充值{r.amount}书币，正在审核中。"
            elif r.status == 'approved':
                msg = f"您于{r.recharge_time:%Y-%m-%d %H:%M}充值{r.amount}书币已通过审核，到账{r.amount + r.bonus}书币。"
            elif r.status == 'rejected':
                msg = f"您于{r.recharge_time:%Y-%m-%d %H:%M}充值{r.amount}书币被拒绝。"
            else:
                msg = f"您于{r.recharge_time:%Y-%m-%d %H:%M}充值{r.amount}书币，状态：{r.status}"
            result.append({
                'id': r.id,
                'title': '充值通知',
                'content': msg,
                'created_at': r.recharge_time,
                'status': r.status
            })
        return Response(result)

class UserCommentReplyMessagesView(APIView):
    def get(self, request, user_id):
        replies = Comment.objects.filter(parent__user_id=user_id).order_by('-created_at')
        result = []
        for r in replies:
            result.append({
                'id': r.id,
                'title': '评论回复',
                'content': f'您的评论收到了回复："{r.content}"',
                'created_at': r.created_at,
                'novel_id': r.novel_id,
            })
        return Response(result)

class AnnouncementManageView(APIView):
    parser_classes = [JSONParser]

    def get(self, request):
        # 只有管理员可以查看所有公告
        # if not request.user.is_staff: # 如果你使用了Django的认证系统，可以用这个判断
        #     return Response({'msg': '无权限'}, status=status.HTTP_403_FORBIDDEN)

        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        announcements = Announcement.objects.all().order_by('-published_at')
        total = announcements.count()
        start = (page - 1) * page_size
        end = start + page_size
        data = AnnouncementSerializer(announcements[start:end], many=True).data
        return Response({'total': total, 'results': data})

    def post(self, request):
        # 只有管理员可以发布公告
        # if not request.user.is_staff: # 如果你使用了Django的认证系统，可以用这个判断
        #     return Response({'msg': '无权限'}, status=status.HTTP_403_FORBIDDEN)

        serializer = AnnouncementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        # 只有管理员可以修改公告
        # if not request.user.is_staff: # 如果你使用了Django的认证系统，可以用这个判断
        #     return Response({'msg': '无权限'}, status=status.HTTP_403_FORBIDDEN)

        try:
            announcement = Announcement.objects.get(id=request.data.get('id'))
        except Announcement.DoesNotExist:
            return Response({'msg': '公告不存在'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AnnouncementSerializer(announcement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # 只有管理员可以删除公告
        # if not request.user.is_staff: # 如果你使用了Django的认证系统，可以用这个判断
        #     return Response({'msg': '无权限'}, status=status.HTTP_403_FORBIDDEN)

        try:
            announcement = Announcement.objects.get(id=request.data.get('id'))
        except Announcement.DoesNotExist:
            return Response({'msg': '公告不存在'}, status=status.HTTP_404_NOT_FOUND)
        announcement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AnnouncementListView(APIView):
    def get(self, request):
        # 用户只查看已发布的公告
        announcements = Announcement.objects.filter(is_published=True).order_by('-published_at')
        serializer = AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data)

class RechargeStatsView(APIView):
    def get(self, request):
        total_recharge = RechargeRecord.objects.filter(status='approved').aggregate(Sum('amount'))['amount__sum'] or 0
        
        # 充值用户数量
        recharge_users_count = RechargeRecord.objects.filter(status='approved').values('user').distinct().count()

        # 各用户充值金额排行（Top 10）
        top_recharge_users = User.objects.filter(id__in=RechargeRecord.objects.values('user')).annotate(
            total_approved_recharge=Sum('rechargerecord__amount', filter=models.Q(rechargerecord__status='approved'))
        ).order_by('-total_approved_recharge')[:10]

        top_recharge_users_data = []
        for user in top_recharge_users:
            if user.total_approved_recharge is not None:
                top_recharge_users_data.append({
                    'username': user.username,
                    'total_recharge': user.total_approved_recharge
                })

        return Response({
            'total_recharge_amount': total_recharge,
            'recharge_users_count': recharge_users_count,
            'top_recharge_users': top_recharge_users_data,
        })

class NovelCollectionStatsView(APIView):
    def get(self, request):
        # 小说总收藏数
        total_collections = Bookshelf.objects.count()

        # 各小说收藏数排行（Top 10）
        top_collected_novels = Novel.objects.annotate(collection_count=Count('bookshelf'))\
                                         .order_by('-collection_count')[:10]
        
        top_collected_novels_data = []
        for novel in top_collected_novels:
            top_collected_novels_data.append({
                'title': novel.title,
                'collection_count': novel.collection_count
            })

        return Response({
            'total_collections': total_collections,
            'top_collected_novels': top_collected_novels_data,
        })
