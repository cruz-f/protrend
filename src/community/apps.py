from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class CommunityConfig(ModuleMixin, AppConfig):
    name = 'community'
    icon = '<i class="material-icons">dashboard</i>'
    default_auto_field = 'django.db.models.AutoField'

    @property
    def verbose_name(self):
        """Module name."""
        return 'ProTReND Community'
