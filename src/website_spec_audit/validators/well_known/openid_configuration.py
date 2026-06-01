import json

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class OpenidConfigurationValidator(BaseValidator):
    slug = "openid-configuration"
    title = "/.well-known/openid-configuration"
    category = "well-known"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/well-known/openid-configuration/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/.well-known/openid-configuration")

        if resource.status_code == 404:
            return self.skip_result(
                "/.well-known/openid-configuration not found (HTTP 404)."
            )

        if resource.status_code != 200:
            return self.fail_result(
                f"/.well-known/openid-configuration returned HTTP {resource.status_code}."
            )

        try:
            data = json.loads(resource.text)
        except (json.JSONDecodeError, ValueError):
            return self.fail_result(
                "/.well-known/openid-configuration is not valid JSON."
            )

        if not isinstance(data, dict) or "issuer" not in data:
            return self.fail_result(
                "/.well-known/openid-configuration JSON is missing the 'issuer' field."
            )

        return self.pass_result(
            f"/.well-known/openid-configuration is valid with issuer: {data['issuer']}."
        )
