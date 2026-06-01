import json

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class GlobalPrivacyControlValidator(BaseValidator):
    slug = "global-privacy-control"
    title = "Global Privacy Control (GPC)"
    category = "privacy"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/privacy/global-privacy-control/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/.well-known/gpc.json")

        if resource.status_code == 404:
            return self.skip_result("/.well-known/gpc.json not found (404).")

        if resource.status_code != 200:
            return self.fail_result(
                f"/.well-known/gpc.json returned status {resource.status_code}."
            )

        try:
            data = json.loads(resource.text)
        except (json.JSONDecodeError, ValueError):
            return self.fail_result(
                "/.well-known/gpc.json is not valid JSON."
            )

        if not isinstance(data, dict):
            return self.fail_result(
                "/.well-known/gpc.json does not contain a JSON object."
            )

        gpc_value = data.get("gpc")

        if gpc_value is True:
            return self.pass_result(
                "/.well-known/gpc.json found with \"gpc\": true."
            )

        return self.fail_result(
            f"/.well-known/gpc.json found but \"gpc\" is {gpc_value!r}, expected true.",
        )
