from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class MetaDescriptionValidator(BaseValidator):
    slug = "meta-description"
    title = '<meta name="description">'
    category = "foundations"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/foundations/meta-description/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")
        meta = doc.cssselect('meta[name="description"]')

        if not meta:
            return self.fail_result("No <meta name=\"description\"> found.")

        content = meta[0].get("content", "").strip()
        if not content:
            return self.fail_result("Meta description has an empty content attribute.")

        if len(content) > 160:
            return self.warn_result(
                f"Meta description is {len(content)} characters; recommended max is 160.",
                details=[f'Content: "{content[:200]}..."'],
            )

        return self.pass_result("Meta description found.")
