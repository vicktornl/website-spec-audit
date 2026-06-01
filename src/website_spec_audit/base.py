from abc import ABC, abstractmethod

from website_spec_audit.context import AuditContext
from website_spec_audit.models import CheckResult, CheckStatus, TopicMeta, TopicStatus


class BaseValidator(ABC):
    """Base class for all spec topic validators."""

    slug: str
    title: str
    category: str
    status: TopicStatus
    spec_url: str

    @property
    def meta(self) -> TopicMeta:
        return TopicMeta(
            slug=self.slug,
            title=self.title,
            category=self.category,
            status=self.status,
            spec_url=self.spec_url,
        )

    @abstractmethod
    async def validate(self, context: AuditContext) -> CheckResult:
        ...

    def pass_result(self, message: str = "pass") -> CheckResult:
        return CheckResult(topic=self.meta, check_status=CheckStatus.PASS, message=message)

    def fail_result(self, message: str, details: list[str] | None = None) -> CheckResult:
        return CheckResult(topic=self.meta, check_status=CheckStatus.FAIL, message=message, details=details or [])

    def warn_result(self, message: str, details: list[str] | None = None) -> CheckResult:
        return CheckResult(topic=self.meta, check_status=CheckStatus.WARN, message=message, details=details or [])

    def skip_result(self, message: str = "cannot be verified via HTTP alone") -> CheckResult:
        return CheckResult(topic=self.meta, check_status=CheckStatus.SKIP, message=message)
