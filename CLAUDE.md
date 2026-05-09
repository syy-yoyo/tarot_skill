# Project Guidance

## Avoid Case-Specific Constraint Sprawl

Optimize the tarot skill at the level of reusable consultation process, not one-off user examples.

When feedback comes from a concrete test case:

- Extract the general process issue first.
- Prefer constraints that improve all readings, such as intake, card-position-context interpretation order, plain language, third-party boundaries, and user agency.
- Do not add special spreads, special wording rules, or special handling for a narrow scenario unless the pattern clearly recurs across many readings.
- Remove or generalize constraints that name a specific scenario such as internships, interviews, CP fandom, paperwork, applications, or any other single test case.
- Keep the skill small enough that future behavior is shaped by principles rather than a pile of exceptions.

Good: "Use plain spoken Chinese instead of abstract consultant language."

Bad: "For internship questions, use this exact opening."
