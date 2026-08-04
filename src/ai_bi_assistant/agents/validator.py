FORBIDDEN_KEYWORDS = {
    "DELETE",
    "DROP",
    "UPDATE",
    "INSERT",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "GRANT",
    "REVOKE",
}


def validate_sql(sql: str):
    """
    Allow only read-only SQL queries.
    """

    sql_upper = sql.upper()

    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in sql_upper:
            raise ValueError(
                f"Forbidden SQL detected: {keyword}"
            )

    if not (
        sql_upper.startswith("SELECT")
        or sql_upper.startswith("WITH")
    ):
        raise ValueError(
            "Only SELECT queries are allowed."
        )

    return True