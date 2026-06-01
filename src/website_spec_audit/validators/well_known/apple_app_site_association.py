import json

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class AppleAppSiteAssociationValidator(BaseValidator):
    slug = "apple-app-site-association"
    title = "/.well-known/apple-app-site-association"
    category = "well-known"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/well-known/apple-app-site-association/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/.well-known/apple-app-site-association")

        if resource.status_code == 404:
            return self.skip_result(
                "/.well-known/apple-app-site-association not found (HTTP 404)."
            )

        if resource.status_code != 200:
            return self.fail_result(
                f"/.well-known/apple-app-site-association returned HTTP {resource.status_code}."
            )

        try:
            json.loads(resource.text)
        except (json.JSONDecodeError, ValueError):
            return self.fail_result(
                "/.well-known/apple-app-site-association is not valid JSON."
            )

        return self.pass_result(
            "/.well-known/apple-app-site-association is present and valid JSON."
        )
