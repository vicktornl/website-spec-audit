import json

from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class PwaManifestValidator(BaseValidator):
    slug = "pwa-manifest"
    title = "Web app manifest"
    category = "resilience"
    status = TopicStatus.RECOMMENDED
    spec_url = "https://specification.website/spec/resilience/pwa-manifest/"

    REQUIRED_FIELDS = ["name", "icons", "start_url", "display"]

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        manifest_href = None
        for link in doc.iter("link"):
            rel = (link.get("rel") or "").lower()
            if "manifest" in rel:
                manifest_href = link.get("href")
                break

        if not manifest_href:
            return self.fail_result("No <link rel=\"manifest\"> found in the page.")

        # Fetch the manifest file
        try:
            manifest_resource = await context.fetch(manifest_href)
        except Exception as exc:
            return self.fail_result(
                f"Could not fetch manifest at {manifest_href}: {exc}."
            )

        if manifest_resource.status_code != 200:
            return self.fail_result(
                f"Manifest at {manifest_href} returned status {manifest_resource.status_code}."
            )

        try:
            data = json.loads(manifest_resource.text)
        except (json.JSONDecodeError, ValueError):
            return self.fail_result(
                f"Manifest at {manifest_href} is not valid JSON."
            )

        if not isinstance(data, dict):
            return self.fail_result("Manifest is not a JSON object.")

        missing_fields: list[str] = []
        for field in self.REQUIRED_FIELDS:
            if field not in data or not data[field]:
                missing_fields.append(field)

        if missing_fields:
            return self.warn_result(
                f"Manifest is missing recommended fields: {', '.join(missing_fields)}.",
                details=[
                    f"Found fields: {', '.join(sorted(data.keys()))}.",
                ],
            )

        return self.pass_result(
            "Web app manifest found with name, icons, start_url, and display."
        )
