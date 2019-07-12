import uuid


USER_KEY = 'uid'
TEN_YEARS = 60 * 60 * 25 * 365 * 10


class UserIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        uid = self.generate_uid(request)
        # 给request对象添加uid属性，也就是说request对象是在访问后创建的
        request.uid = uid
        response = self.get_response(request)
        # 给响应对象设置cookie，httponly：只能在服务端访问
        response.set_cookie(USER_KEY, uid, max_age=TEN_YEARS, httponly=True)
        return response

    # 先从cookie中取uid，取不到则生成一个
    def generate_uid(self, request):
        try:
            uid = request.COOKIES[USER_KEY]
        except KeyError:
            uid = uuid.uuid4().hex
        return uid