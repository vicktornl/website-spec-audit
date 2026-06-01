from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class DocumentLanguageValidator(BaseValidator):
    slug = "document-language"
    title = "Document and parts language"
    category = "accessibility"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/accessibility/document-language/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")
        lang = doc.get("lang", "").strip()

        if not lang:
            return self.fail_result(
                "The <html> element is missing a lang attribute."
            )

        # Check that lang value looks valid (BCP 47: at least a 2-3 letter primary tag)
        primary = lang.split("-")[0]
        if not (2 <= len(primary) <= 3 and primary.isalpha()):
            return self.warn_result(
                f'The lang attribute value "{lang}" does not appear to be a valid BCP 47 tag.'
            )

        return self.pass_result(f'Document language is set to "{lang}".')
