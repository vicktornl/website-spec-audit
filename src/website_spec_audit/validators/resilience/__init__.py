from website_spec_audit.validators.resilience.error_pages import ErrorPagesValidator
from website_spec_audit.validators.resilience.maintenance_pages import MaintenancePagesValidator
from website_spec_audit.validators.resilience.monitoring_uptime import MonitoringUptimeValidator
from website_spec_audit.validators.resilience.offline_support import OfflineSupportValidator
from website_spec_audit.validators.resilience.pwa_manifest import PwaManifestValidator

ALL_VALIDATORS = [
    ErrorPagesValidator(),
    MaintenancePagesValidator(),
    OfflineSupportValidator(),
    PwaManifestValidator(),
    MonitoringUptimeValidator(),
]
