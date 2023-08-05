"""
Table creation strings all kept here so that it can be easily managed.
"""


irs_table = """
    CREATE TABLE irs_table
        (
            date date, 
            maturity text, 
            irs text, 
            ininCdNm text, 
            scrsItmsKcd text,
        )
    """

irs_table_unique = """
    ALTER TABLE irs_table
    ADD CONSTRAINT irs_table_key UNIQUE(date);
    """
