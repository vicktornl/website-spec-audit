from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class HtmlLangValidator(BaseValidator):
    slug = "html-lang"
    title = "The lang attribute on <html>"
    category = "foundations"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/foundations/html-lang/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")
        lang = doc.get("lang", "").strip()

        if lang:
            return self.pass_result(f'<html> has lang="{lang}".')

        return self.fail_result("The <html> element is missing a lang attribute.")
