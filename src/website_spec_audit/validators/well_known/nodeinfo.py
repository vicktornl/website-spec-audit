import json

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class NodeinfoValidator(BaseValidator):
    slug = "nodeinfo"
    title = "/.well-known/nodeinfo"
    category = "well-known"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/well-known/nodeinfo/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/.well-known/nodeinfo")

        if resource.status_code == 404:
            return self.skip_result(
                "/.well-known/nodeinfo not found (HTTP 404)."
            )

        if resource.status_code != 200:
            return self.fail_result(
                f"/.well-known/nodeinfo returned HTTP {resource.status_code}."
            )

        try:
            data = json.loads(resource.text)
        except (json.JSONDecodeError, ValueError):
            return self.fail_result(
                "/.well-known/nodeinfo is not valid JSON."
            )

        if not isinstance(data, dict) or "links" not in data:
            return self.fail_result(
                "/.well-known/nodeinfo JSON is missing the 'links' field."
            )

        if not isinstance(data["links"], list):
            return self.fail_result(
                "/.well-known/nodeinfo 'links' field is not an array."
            )

        return self.pass_result(
            f"/.well-known/nodeinfo is valid with {len(data['links'])} link(s)."
        )
