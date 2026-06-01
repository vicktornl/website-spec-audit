from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class LocalisedMetadataValidator(BaseValidator):
    slug = "localised-metadata"
    title = "Localised page metadata"
    category = "i18n"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/i18n/localised-metadata/"

    async def validate(self, context: AuditContext) -> CheckResult:
        return self.skip_result("requires comparison across language versions")
