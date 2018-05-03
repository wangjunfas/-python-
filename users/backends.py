from .models import User


class EmailBackend(object):
    def authenticate(self, request, **credentials):
        # 先获取email
        email = credentials.get('email', credentials.get('username', ''))
        # 再根据email去取对象。如果能取到，则校验密码。如果取不到则报DoesNotExist的异常
        if email:
            # email存在则去取对象
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                pass
            else:
                # 取到了对象
                # 校验密码
                if user.check_password(credentials['password']):
                # 密码校验通过，则返回user对象
                    return user

    def get_user(self, user_id):
        # 这个函数是必须要有的。
        # 就是根据user_id去取user对象。
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
