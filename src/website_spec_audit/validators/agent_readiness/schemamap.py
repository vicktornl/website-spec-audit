from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class SchemamapValidator(BaseValidator):
    slug = "schemamap"
    title = "Schemamap \u2014 discoverable JSON-LD endpoints per resource"
    category = "agent-readiness"
    status = TopicStatus.OPTIONAL
    spec_url = "https://specification.website/spec/agent-readiness/schemamap/"

    async def validate(self, context: AuditContext) -> CheckResult:
        resource = await context.fetch("/schemamap.xml")

        if resource.status_code == 404:
            return self.skip_result("/schemamap.xml not found (HTTP 404).")

        if resource.status_code != 200:
            return self.fail_result(
                f"/schemamap.xml returned HTTP {resource.status_code}."
            )

        text = resource.text.strip()
        if not text:
            return self.fail_result("/schemamap.xml is present but empty.")

        # Basic XML validity check
        try:
            from lxml import etree

            etree.fromstring(text.encode("utf-8"))
        except Exception as exc:
            return self.fail_result(
                f"/schemamap.xml is not valid XML: {exc}"
            )

        return self.pass_result("/schemamap.xml is present and valid XML.")
