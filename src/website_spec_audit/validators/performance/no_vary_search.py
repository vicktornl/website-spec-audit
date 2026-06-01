from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class NoVarySearchValidator(BaseValidator):
    slug = "no-vary-search"
    title = "No-Vary-Search response header"
    category = "performance"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/performance/no-vary-search/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/")
        no_vary_search = resource.headers.get("no-vary-search")

        if not no_vary_search:
            return self.skip_result(
                "No-Vary-Search header not present. "
                "This is an emerging header and its absence is not a problem."
            )

        return self.pass_result(
            f"No-Vary-Search header is present: {no_vary_search}"
        )
