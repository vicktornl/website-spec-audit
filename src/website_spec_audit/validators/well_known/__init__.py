from website_spec_audit.validators.well_known.api_catalog import ApiCatalogValidator
from website_spec_audit.validators.well_known.apple_app_site_association import (
    AppleAppSiteAssociationValidator,
)
from website_spec_audit.validators.well_known.assetlinks_json import (
    AssetlinksJsonValidator,
)
from website_spec_audit.validators.well_known.change_password import (
    ChangePasswordValidator,
)
from website_spec_audit.validators.well_known.nodeinfo import NodeinfoValidator
from website_spec_audit.validators.well_known.openid_configuration import (
    OpenidConfigurationValidator,
)
from website_spec_audit.validators.well_known.traffic_advice import (
    TrafficAdviceValidator,
)
from website_spec_audit.validators.well_known.webfinger import WebfingerValidator
from website_spec_audit.validators.well_known.well_known_overview import (
    WellKnownOverviewValidator,
)

ALL_VALIDATORS = [
    WellKnownOverviewValidator(),
    ChangePasswordValidator(),
    OpenidConfigurationValidator(),
    ApiCatalogValidator(),
    WebfingerValidator(),
    AppleAppSiteAssociationValidator(),
    AssetlinksJsonValidator(),
    NodeinfoValidator(),
    TrafficAdviceValidator(),
]
