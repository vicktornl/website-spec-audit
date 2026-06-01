from dataclasses import dataclass, field
from enum import Enum


class CheckStatus(Enum):
    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"
    SKIP = "skip"


class TopicStatus(Enum):
    REQUIRED = "required"
    RECOMMENDED = "recommended"
    OPTIONAL = "optional"
    AVOID = "avoid"


@dataclass(frozen=True)
class TopicMeta:
    slug: str
    title: str
    category: str
    status: TopicStatus
    spec_url: str


@dataclass
class CheckResult:
    topic: TopicMeta
    check_status: CheckStatus
    message: str
    details: list[str] = field(default_factory=list)


@dataclass
class CategoryResult:
    category: str
    results: list[CheckResult]

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.check_status == CheckStatus.PASS)

    @property
    def total(self) -> int:
        return len(self.results)


@dataclass
class AuditReport:
    url: str
    categories: list[CategoryResult]

    @property
    def total_passed(self) -> int:
        return sum(c.passed for c in self.categories)

    @property
    def total_checks(self) -> int:
        return sum(c.total for c in self.categories)
