from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class DataTablesValidator(BaseValidator):
    slug = "data-tables"
    title = "Accessible data tables"
    category = "accessibility"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/accessibility/data-tables/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        tables = doc.cssselect("table")

        if not tables:
            return self.pass_result("No <table> elements found.")

        details: list[str] = []
        issues = 0

        for i, table in enumerate(tables, 1):
            table_issues: list[str] = []

            # Check for caption
            captions = table.cssselect("caption")
            if not captions:
                table_issues.append("missing <caption>")

            # Check for th elements
            headers = table.cssselect("th")
            if not headers:
                table_issues.append("no <th> elements found")
            else:
                # Check if th elements have scope
                missing_scope = [
                    th for th in headers if not th.get("scope")
                ]
                if missing_scope:
                    table_issues.append(
                        f"{len(missing_scope)} <th> element(s) missing scope attribute"
                    )

            if table_issues:
                issues += 1
                details.append(f"Table {i}: {'; '.join(table_issues)}.")
            else:
                details.append(f"Table {i}: properly structured.")

        if issues:
            return self.warn_result(
                f"{issues} of {len(tables)} table(s) have accessibility issues.",
                details=details,
            )

        return self.pass_result(
            f"All {len(tables)} table(s) are properly structured."
        )
