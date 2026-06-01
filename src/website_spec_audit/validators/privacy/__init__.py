from website_spec_audit.validators.privacy.analytics_privacy import AnalyticsPrivacyValidator
from website_spec_audit.validators.privacy.cookie_consent import CookieConsentValidator
from website_spec_audit.validators.privacy.data_minimization import DataMinimizationValidator
from website_spec_audit.validators.privacy.global_privacy_control import GlobalPrivacyControlValidator
from website_spec_audit.validators.privacy.privacy_policy import PrivacyPolicyValidator
from website_spec_audit.validators.privacy.third_party_scripts import ThirdPartyScriptsValidator

ALL_VALIDATORS = [
    PrivacyPolicyValidator(),
    CookieConsentValidator(),
    GlobalPrivacyControlValidator(),
    ThirdPartyScriptsValidator(),
    AnalyticsPrivacyValidator(),
    DataMinimizationValidator(),
]
