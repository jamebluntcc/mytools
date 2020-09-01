# coding: utf-8
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from wings.drf import filters
from wings.drf import render
from wings.drf.filters_helper import DynamicCalendarMonth


class ResourceMixin:
    def filter_input_elements_data(self):
        inputs = []
        if getattr(self, 'search_fields', None):
            inputs.append({
                'key': 'search',
                'name': getattr(self, 'search_label', 'search'),
                'method': 'input'
            })
        if getattr(self, 'filter_class'):
            for k, v in self.filter_class.base_filters.items():
                item = {}
                if isinstance(v, filters.ApiSearchFilter):
                    if not v.display:
                        continue
                    if not v.sub:
                        item['method'] = 'api_search'
                    else:
                        item['method'] = 'relate'
                        item['sub'] = v.sub
                    item['info'] = {
                        'url': v.url,
                        'search_key': v.search_key,
                        'otherKeys': v.other_keys,
                        'join': v.sep
                    }
                    item['multiple'] = v.multiple

                elif isinstance(v, filters.ChoiceFilter) or isinstance(v, filters.BooleanFilter):
                    if not v.display:
                        continue
                    item['info'] = v.choice
                    item['multiple'] = v.multiple
                    if v.default or v.default is not None:
                        item['default'] = []
                        if not isinstance(v.default, list):
                            item['default'].append({'key': v.default, 'label': dict(v.choice).get(v.default)})
                        else:
                            for x in v.default:
                                item['default'].append({'key': x, 'label': dict(v.choice).get(x)})

                    if not v.sub:
                        item['method'] = 'dropdown'
                    else:
                        item['method'] = 'relate'
                        item['sub'] = v.sub
                elif isinstance(v, filters.CharFilter):
                    if not v.display:
                        continue
                    item['method'] = 'input' if not v.format else 'date'
                    if v.default:
                        item['default'] = v.default
                    if v.placeholder:
                        item['placeholder'] = v.placeholder
                elif isinstance(v, filters.NumberFilter):
                    if not v.display:
                        continue
                    item['method'] = 'input'
                    if v.default:
                        item['default'] = v.default
                elif isinstance(v, filters.DateFromToRangeFilter):
                    if not v.display:
                        continue
                    item['method'] = 'date_range'
                    item['format'] = v.format
                    if isinstance(v.default, DynamicCalendarMonth):
                        item['default'] = v.default.default()
                    elif v.default:
                        item['default'] = v.default
                elif isinstance(v, filters.DateTimeFromToRangeFilter):
                    if not v.display:
                        continue
                    item['method'] = 'date_range'
                    item['format'] = v.format
                    if v.default:
                        item['default'] = v.default
                elif isinstance(v, filters.RangeFilter):
                    if not v.display:
                        continue
                    item['method'] = 'number_range'
                    if v.addon_after:
                        item['addonAfter'] = v.addon_after
                elif isinstance(v, filters.DateStringFilter):
                    if not v.display:
                        continue
                    item['method'] = 'date'
                    item['format'] = v.format
                    item['default'] = v.default
                if item:
                    item['key'] = k
                    item['name'] = v.field.label or v.field.help_text or k
                    inputs.append(item)
        return inputs

    @swagger_auto_schema(auto_schema=None)
    @action(methods=['get'], detail=False)
    def filter_input_elements(self, request):
        return Response(self.filter_input_elements_data())

    def get_enums(self, request):
        return {}

    @swagger_auto_schema(auto_schema=None)
    @action(methods=['get'], detail=False)
    def enums(self, request):
        data = self.get_enums(request)
        return Response(data)


class BaseViewSet(ResourceMixin, GenericViewSet):
    aggregator_type = None
    renderer_classes = [render.CustomJSONRender, render.ReadOnlyBrowsableAPIRenderer]

    def get_serializer_class(self):
        if self.action == 'list' and getattr(self, 'list_serializer_class', None):
            return self.list_serializer_class

        if self.action == 'create' and getattr(self, 'create_serializer_class', None):
            return self.create_serializer_class

        if self.action in ['partial_update', 'update']:
            if getattr(self, 'update_serializer_class', None):
                return self.update_serializer_class
            if getattr(self, 'create_serializer_class', None):
                return self.create_serializer_class

        return super().get_serializer_class()


class ModelViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   BaseViewSet):

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if hasattr(instance, 'is_active'):
            instance.is_active = False
            instance.save()
        else:
            self.perform_destroy(instance)
        return Response()


__all__ = ('BaseViewSet', 'ModelViewSet')
