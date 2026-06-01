from website_spec_audit.validators.security.caa_records import CaaRecordsValidator
from website_spec_audit.validators.security.content_security_policy import (
    ContentSecurityPolicyValidator,
)
from website_spec_audit.validators.security.cookie_attributes import (
    CookieAttributesValidator,
)
from website_spec_audit.validators.security.dnssec import DnssecValidator
from website_spec_audit.validators.security.frame_ancestors import (
    FrameAncestorsValidator,
)
from website_spec_audit.validators.security.hsts import HstsValidator
from website_spec_audit.validators.security.https_tls import HttpsTlsValidator
from website_spec_audit.validators.security.permissions_policy import (
    PermissionsPolicyValidator,
)
from website_spec_audit.validators.security.referrer_policy import (
    ReferrerPolicyValidator,
)
from website_spec_audit.validators.security.security_txt import SecurityTxtValidator
from website_spec_audit.validators.security.subresource_integrity import (
    SubresourceIntegrityValidator,
)
from website_spec_audit.validators.security.x_content_type_options import (
    XContentTypeOptionsValidator,
)

ALL_VALIDATORS = [
    HttpsTlsValidator(),
    HstsValidator(),
    ContentSecurityPolicyValidator(),
    SecurityTxtValidator(),
    XContentTypeOptionsValidator(),
    FrameAncestorsValidator(),
    ReferrerPolicyValidator(),
    PermissionsPolicyValidator(),
    SubresourceIntegrityValidator(),
    CookieAttributesValidator(),
    CaaRecordsValidator(),
    DnssecValidator(),
]
