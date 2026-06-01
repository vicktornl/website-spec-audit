from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class EmptyLinksButtonsValidator(BaseValidator):
    slug = "empty-links-buttons"
    title = "Empty links and buttons"
    category = "accessibility"
    status = TopicStatus.AVOID
    spec_url = "https://specification.website/spec/accessibility/empty-links-buttons/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        elements = doc.cssselect("a, button")

        if not elements:
            return self.pass_result("No links or buttons found.")

        empty: list[str] = []
        for el in elements:
            # Check for visible text content
            text = (el.text_content() or "").strip()
            if text:
                continue

            # Check for aria-label or aria-labelledby
            if el.get("aria-label") or el.get("aria-labelledby"):
                continue

            # Check for title attribute
            if el.get("title"):
                continue

            # Check for child img with alt text
            child_imgs = el.cssselect("img[alt]")
            has_alt = any(
                (img.get("alt") or "").strip() for img in child_imgs
            )
            if has_alt:
                continue

            # Check for child svg with role or aria-label
            child_svgs = el.cssselect("svg")
            has_svg_label = any(
                svg.get("aria-label") or svg.get("role") == "img"
                for svg in child_svgs
            )
            if has_svg_label:
                continue

            tag = el.tag
            href = el.get("href", "")
            desc = f"<{tag}"
            if href:
                desc += f' href="{href}"'
            desc += "> has no accessible name."
            empty.append(desc)

        if empty:
            return self.fail_result(
                f"{len(empty)} empty link(s) or button(s) found.",
                details=empty,
            )

        return self.pass_result(
            f"All {len(elements)} link(s) and button(s) have accessible names."
        )
