class SuperuserOrPublisherQuerysetMixin:

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.request.user

        if user.is_superuser:
            return queryset
        return queryset.filter(publishers=user)
