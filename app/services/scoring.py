SEVERITY_DEDUCTIONS = {
    "ERROR": 15,
    "WARNING": 5,
    "INFO": 1,
}


def calculate_score(violations: list) -> int:
    score = 100

    for violation in violations:
        score -= SEVERITY_DEDUCTIONS.get(
            violation.severity,
            0,
        )

    return max(0, score)