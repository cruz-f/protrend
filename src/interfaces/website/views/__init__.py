from .about import about
from .authentication import SignInView, LogoutView, sign_up, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView, activate
from .index import (IndexView, fake_view)
from .search import search
from .paginate_regulators import regulators_page
from .organism import (OrganismsView, OrganismView)
from .gene import GeneView
from .regulator import (RegulatorsView, RegulatorView)
from .utils import download_fasta
