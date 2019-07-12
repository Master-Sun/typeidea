from rest_framework import serializers, pagination

from .models import Post, Category


# 列表页序列化数据，用法类似Form
class PostSerializer(serializers.ModelSerializer):
    # 外键需要如下配置
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
    )
    tag = serializers.SlugRelatedField(
        many=True,            # 多对多
        read_only=True,       # 定义外键是否可写
        slug_field='name',    # 定义外键展示对应主表中的字段
    )
    owner = serializers.SlugRelatedField(read_only=True, slug_field='username',)
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Post
        # id用来获取详情页
        fields = ['id', 'title', 'category', 'tag', 'owner', 'created_time']


# 定义详情页接口需要的Serializer类
# 此处继承自PostSerializer，只需在fields中增加content_html字段即可
class PostDetailSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'tag', 'owner', 'content_html', 'created_time']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'created_time')


# 获取某个分类下的文章列表，从资源的角度看，相当于分类的详情页数据
class CategoryDetailSerializer(CategorySerializer):
    # 将posts字段获取的内容映射到paginated_posts方法上
    # 即最终返回数据时，posts对应的数据从paginated_posts方法中获取
    posts = serializers.SerializerMethodField('paginated_posts')

    # http://127.0.0.1:8000/api/category/2/?page=3
    def paginated_posts(self, obj):
        posts = obj.post_set.filter(status=Post.STATUS_NORMAL)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(posts, self.context['request'])
        serializer = PostSerializer(page, many=True, context={'request': self.context['request']})
        return {
            'count': posts.count(),
            'results': serializer.data,
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link(),
        }

    class Meta:
        model = Category
        fields = ('id', 'name', 'created_time', 'posts')