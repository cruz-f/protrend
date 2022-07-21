from django.contrib.auth.mixins import LoginRequiredMixin
from material.frontend.views import ModelViewSet, CreateModelView, UpdateModelView

from community.permissions import CommunityPermissionsMixIn


class CommunityCreateView(CreateModelView):

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        obj = form.save(commit=False)
        obj.user = self.request.user

        # noinspection PyAttributeOutsideInit
        self.object = obj.save()
        return super().form_valid(form)


class CommunityUpdateView(UpdateModelView):

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        obj = form.save(commit=False)
        obj.user = self.request.user

        # noinspection PyAttributeOutsideInit
        self.object = obj.save()
        return super().form_valid(form)


class CommunityViewSet(LoginRequiredMixin, CommunityPermissionsMixIn, ModelViewSet):
    create_view_class = CommunityCreateView
    update_view_class = CommunityUpdateView
