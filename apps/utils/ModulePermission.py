# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission, SAFE_METHODS

class ModulePermission(BasePermission):
    '''
    ModulePermission, 检查一个用户是否有对应某些module的权限

    APIView需要实现module_perms属性:
        type: list
        example: ['information.information', 'school.school']

    权限说明:
        1. is_superuser有超级权限
        2. 权限列表请在api.models.Permission的class Meta中添加(请不要用数据库直接添加)
        3. 只要用户有module_perms的一条符合结果即认为有权限, 所以module_perms是or的意思
    '''

    authenticated_users_only = True


    #获取api模块中的权限
    def has_perms(self, user, perms):
        user_perms = user.get_all_permissions()
        print (user_perms)
        for perm in perms:
            if perm in user_perms:
                return True
        return False


    #获取当前应用的perm
    def get_module_perms(self, view):
        return ['users.{}'.format(perm) for perm in view.module_perms]

    def has_permission(self, request, view):
        '''
        is_superuser用户有上帝权限，测试的时候注意账号
        '''
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        # # is_superuser用户有上帝权限
        if request.user.is_superuser:
            return True



        assert view.module_perms or not isinstance(view.module_perms, list), (
            u"view需要override module属性，例如['information.information', 'school.school']"
        )

        if getattr(view, '_ignore_model_permissions', False):

            return True

        if hasattr(view, 'get_queryset'):
            queryset = view.get_queryset()
        else:
            queryset = getattr(view, 'queryset', None)

        assert queryset is not None, (
            'Cannot apply DjangoModelPermissions on a view that '
            'does not set `.queryset` or have a `.get_queryset()` method.'
        )

        return (
            request.user and
            (request.user.is_authenticated() or not self.authenticated_users_only) and
            self.has_perms(request.user, self.get_module_perms(view))
        )


class ModulePermissionOrReadOnly(ModulePermission):
    """
    The request is authenticated with ModulePermission, or is a read-only request.
    """

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or super(ModulePermissionOrReadOnly, self).has_permission(request, view))