"""Auto-register all validators into the global registry."""

from website_spec_audit.registry import registry
from website_spec_audit.validators.accessibility import ALL_VALIDATORS as _accessibility
from website_spec_audit.validators.agent_readiness import ALL_VALIDATORS as _agent_readiness
from website_spec_audit.validators.foundations import ALL_VALIDATORS as _foundations
from website_spec_audit.validators.i18n import ALL_VALIDATORS as _i18n
from website_spec_audit.validators.performance import ALL_VALIDATORS as _performance
from website_spec_audit.validators.privacy import ALL_VALIDATORS as _privacy
from website_spec_audit.validators.resilience import ALL_VALIDATORS as _resilience
from website_spec_audit.validators.security import ALL_VALIDATORS as _security
from website_spec_audit.validators.seo import ALL_VALIDATORS as _seo
from website_spec_audit.validators.well_known import ALL_VALIDATORS as _well_known

_all_categories = [
    _foundations,
    _seo,
    _accessibility,
    _security,
    _well_known,
    _agent_readiness,
    _performance,
    _privacy,
    _resilience,
    _i18n,
]

for _category_validators in _all_categories:
    for _validator in _category_validators:
        registry.register(_validator)
