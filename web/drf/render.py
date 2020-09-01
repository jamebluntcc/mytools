# coding:utf-8

from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer


class CustomJSONRender(JSONRenderer):
    """
    自定义Render，返回格式
    {
        'code': 0,
        'msg': '成功',
        'data': {...}
    }
    可以自定义code和msg
    """

    def format_error_msg(self, data):
        if not data:
            return ''
        if isinstance(data, list):
            return self.format_error_msg(data[0])
        if isinstance(data, dict):
            return self.format_error_msg(list(data.values()))
        return str(data)

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            response = renderer_context.get('response')
            response._origin_status_code = response.status_code
            response.status_code = 200
            # 返回结构符合标准
            if isinstance(data, dict) and all([i in data for i in ['code', 'msg']]):
                if 'data' not in data:
                    data['data'] = None
                return super().render(data, accepted_media_type, renderer_context)
            # 有异常
            if response.exception:
                msg = self.format_error_msg(data) or '未知错误信息'
                return super().render({
                    'msg': msg,
                    'code': response._origin_status_code,
                    'data': data
                }, accepted_media_type, renderer_context)
            # 无异常
            return super().render({
                'msg': '操作成功',
                'code': 0,
                'data': data
            }, accepted_media_type, renderer_context)


class ReadOnlyBrowsableAPIRenderer(BrowsableAPIRenderer):
    def show_form_for_method(self, view, method, request, obj):
        return False

    def get_filter_form(self, data, view, request):
        return
