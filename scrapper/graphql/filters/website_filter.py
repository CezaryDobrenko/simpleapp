from django_filters import BooleanFilter, CharFilter, FilterSet, OrderingFilter


class WebsiteFilter(FilterSet):
    order_by = OrderingFilter(
        fields=("created_date", "modified_date"),
    )

    url = CharFilter(lookup_expr="icontains", field_name="url")
    description = CharFilter(lookup_expr="icontains", field_name="description")
    is_ready = BooleanFilter(method="is_ready_filter")

    def is_ready_filter(self, queryset, name, value: str):
        if value:
            return queryset.filter(is_ready=True)
        return queryset.filter(is_ready=False)
