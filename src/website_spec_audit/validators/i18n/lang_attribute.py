from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class LangAttributeValidator(BaseValidator):
    slug = "lang-attribute"
    title = "lang attribute on inline content"
    category = "i18n"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/i18n/lang-attribute/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        html_elements = doc.xpath("//html")
        if not html_elements:
            return self.fail_result("No <html> element found in the document.")

        html_el = html_elements[0]
        lang = html_el.get("lang")

        if not lang:
            return self.fail_result(
                "The <html> element does not have a lang attribute.",
                details=[
                    "The lang attribute is required for accessibility and internationalisation.",
                ],
            )

        lang = lang.strip()
        if not lang:
            return self.fail_result(
                "The <html> lang attribute is empty.",
            )

        # Basic validation: should be a BCP 47 language tag
        if len(lang) < 2:
            return self.warn_result(
                f"The lang attribute value '{lang}' appears too short.",
            )

        return self.pass_result(
            f"The <html> element has lang=\"{lang}\".",
        )
