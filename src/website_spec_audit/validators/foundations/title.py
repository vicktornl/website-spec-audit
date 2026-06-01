from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class TitleValidator(BaseValidator):
    slug = "title"
    title = "The <title> element"
    category = "foundations"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/foundations/title/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")
        titles = doc.cssselect("head title")

        if not titles:
            return self.fail_result("No <title> element found in <head>.")

        if len(titles) > 1:
            return self.warn_result(
                f"Found {len(titles)} <title> elements; there should be exactly one."
            )

        text = titles[0].text_content().strip()
        if not text:
            return self.fail_result("The <title> element is empty.")

        return self.pass_result(f"Title found: \"{text}\".")
