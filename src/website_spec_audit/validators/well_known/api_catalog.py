import json

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class ApiCatalogValidator(BaseValidator):
    slug = "api-catalog"
    title = "/.well-known/api-catalog"
    category = "well-known"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/well-known/api-catalog/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/.well-known/api-catalog")

        if resource.status_code == 404:
            return self.skip_result(
                "/.well-known/api-catalog not found (HTTP 404)."
            )

        if resource.status_code != 200:
            return self.fail_result(
                f"/.well-known/api-catalog returned HTTP {resource.status_code}."
            )

        try:
            json.loads(resource.text)
        except (json.JSONDecodeError, ValueError):
            return self.fail_result(
                "/.well-known/api-catalog is not valid JSON."
            )

        return self.pass_result("/.well-known/api-catalog is present and valid JSON.")
