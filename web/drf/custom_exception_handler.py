from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status
import logging
from errors import FatalErr
from utils.response import Response
from django.db import DatabaseError

logger = logging.getLogger('ops.wings.drf')


class ServiceUnavailable(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = '服务器发生错误'


def exception_handler(exc, context):
    # 先调用DRF框架的默认异常处理函数
    response = drf_exception_handler(exc, context)
    if response is None:
        view = context['view']
        logger.info('[%s]: %s' % (view, type(exc)))
        # 定义常见的错误类型
        if isinstance(exc, DatabaseError):
            return Response(code=status.HTTP_507_INSUFFICIENT_STORAGE,
                            msg="数据库发现错误，请联系管理员")
        if isinstance(exc, FatalErr):
            return Response(code=FatalErr.code,
                            msg=FatalErr.msg)
        if isinstance(exc, Exception):
            return Response(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            msg="服务器发生错误，请联系管理员")

    return Response(msg='服务器发生错误，请联系管理员',
                    code=status.HTTP_500_INTERNAL_SERVER_ERROR)



