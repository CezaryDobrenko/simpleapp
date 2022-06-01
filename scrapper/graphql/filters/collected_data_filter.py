from django_filters import CharFilter, FilterSet, OrderingFilter


class CollectedDataFilter(FilterSet):
    order_by = OrderingFilter(
        fields=("created_date", "modified_date"),
    )

    value = CharFilter(lookup_expr="icontains", field_name="value")
