from website_spec_audit.base import BaseValidator
from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, TopicStatus


class ImageOptimizationValidator(BaseValidator):
    slug = "image-optimization"
    title = "Image optimisation"
    category = "performance"
    status = TopicStatus.REQUIRED
    spec_url = "https://specification.website/spec/performance/image-optimization/"

    async def validate(self, context: AuditContext) -> CheckResult:
        doc = await context.fetch_html("/")

        images = list(doc.iter("img"))
        if not images:
            return self.pass_result("No <img> tags found on the page.")

        issues: list[str] = []
        missing_dimensions = 0
        missing_srcset = 0
        no_modern_format = 0

        for img in images:
            src = img.get("src", "")
            width = img.get("width")
            height = img.get("height")
            srcset = img.get("srcset")

            if not width or not height:
                missing_dimensions += 1

            if not srcset:
                missing_srcset += 1
            else:
                srcset_lower = srcset.lower()
                if "webp" not in srcset_lower and "avif" not in srcset_lower:
                    # Also check if this img is inside a <picture> with modern sources
                    parent = img.getparent()
                    has_modern_source = False
                    if parent is not None and parent.tag == "picture":
                        for source in parent.iter("source"):
                            source_type = (source.get("type") or "").lower()
                            source_srcset = (source.get("srcset") or "").lower()
                            if any(
                                fmt in source_type or fmt in source_srcset
                                for fmt in ("webp", "avif")
                            ):
                                has_modern_source = True
                                break
                    if not has_modern_source:
                        no_modern_format += 1

        if missing_dimensions:
            issues.append(
                f"{missing_dimensions} image(s) missing explicit width/height attributes."
            )
        if missing_srcset:
            issues.append(
                f"{missing_srcset} image(s) missing srcset attribute for responsive images."
            )
        if no_modern_format:
            issues.append(
                f"{no_modern_format} image(s) without modern format hints (webp/avif) in srcset or <picture>."
            )

        if not issues:
            return self.pass_result(
                f"All {len(images)} image(s) have dimensions, srcset, and modern format hints."
            )

        return self.warn_result(
            f"Found {len(images)} image(s) with optimisation opportunities.",
            details=issues,
        )
