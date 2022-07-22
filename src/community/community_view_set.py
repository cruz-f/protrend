from django.contrib.auth.mixins import LoginRequiredMixin
from material.frontend.views import ModelViewSet, CreateModelView, UpdateModelView

from community.models import OrganismCommunity, RegulatorCommunity, GeneCommunity, TFBSCommunity, EffectorCommunity
from community.permissions import CommunityPermissionsMixIn


INTERACTION_FIELDS = {'organism': OrganismCommunity,
                      'regulator': RegulatorCommunity,
                      'gene': GeneCommunity,
                      'tfbs': TFBSCommunity,
                      'effector': EffectorCommunity}


class CommunityCreateView(CreateModelView):

    def get_form(self, form_class=None):
        form = super(CommunityCreateView, self).get_form(form_class)
        for field, model in INTERACTION_FIELDS.items():
            if field in form.fields:
                form.fields[field].queryset = model.objects.filter(user=self.request.user)
        return form

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        obj = form.save(commit=False)
        obj.user = self.request.user

        # noinspection PyAttributeOutsideInit
        self.object = obj.save()
        return super().form_valid(form)


class CommunityUpdateView(UpdateModelView):

    def get_form(self, form_class=None):
        form = super(CommunityUpdateView, self).get_form(form_class)
        for field in INTERACTION_FIELDS:
            if field in form.fields:
                form.fields[field].queryset = self.model.objects.filter(user=self.request.user)
        return form

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
