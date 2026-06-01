from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class HeadingHierarchyValidator(BaseValidator):
    slug = "heading-hierarchy"
    title = "Heading hierarchy"
    category = "seo"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/seo/heading-hierarchy/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")
        details: list[str] = []
        issues: list[str] = []

        headings: list[tuple[int, str]] = []
        for level in range(1, 7):
            for el in doc.iter(f"h{level}"):
                text = el.text_content().strip()[:80]
                headings.append((level, text))

        if not headings:
            return self.fail_result("No headings (h1-h6) found on the page.")

        # Collect headings in document order
        ordered: list[tuple[int, str]] = []
        for el in doc.iter():
            if el.tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
                level = int(el.tag[1])
                text = el.text_content().strip()[:80]
                ordered.append((level, text))

        # Check for exactly one h1
        h1_count = sum(1 for lvl, _ in ordered if lvl == 1)
        if h1_count == 0:
            issues.append("No <h1> element found.")
        elif h1_count > 1:
            issues.append(f"Multiple <h1> elements found ({h1_count}); there should be exactly one.")

        # Check for level skipping
        for i in range(1, len(ordered)):
            prev_level = ordered[i - 1][0]
            curr_level = ordered[i][0]
            if curr_level > prev_level + 1:
                issues.append(
                    f"Heading level skips from <h{prev_level}> to <h{curr_level}> "
                    f'(near "{ordered[i][1]}").'
                )

        for lvl, text in ordered[:10]:
            details.append(f"<h{lvl}>: {text}")

        if issues:
            return self.fail_result(
                "Heading hierarchy issues detected.",
                details=issues + details,
            )

        return self.pass_result(
            f"Heading hierarchy is correct ({len(ordered)} headings, single h1)."
        )
