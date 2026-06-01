import json

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class AssetlinksJsonValidator(BaseValidator):
    slug = "assetlinks-json"
    title = "/.well-known/assetlinks.json"
    category = "well-known"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/well-known/assetlinks-json/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/.well-known/assetlinks.json")

        if resource.status_code == 404:
            return self.skip_result(
                "/.well-known/assetlinks.json not found (HTTP 404)."
            )

        if resource.status_code != 200:
            return self.fail_result(
                f"/.well-known/assetlinks.json returned HTTP {resource.status_code}."
            )

        try:
            data = json.loads(resource.text)
        except (json.JSONDecodeError, ValueError):
            return self.fail_result(
                "/.well-known/assetlinks.json is not valid JSON."
            )

        if not isinstance(data, list):
            return self.fail_result(
                "/.well-known/assetlinks.json is valid JSON but not an array."
            )

        return self.pass_result(
            "/.well-known/assetlinks.json is present and a valid JSON array."
        )
