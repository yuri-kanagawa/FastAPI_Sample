user_create="""
| Request | |
| ---- | ----|
| name| AccountUserName |
| password| AccountUserPassword |
"""

user_login="""
| Request | |
| ---- | ----|
| name| AccountUserName |
| password| AccountUserPassword |
"""

user_login_token="""
| Request | |
| ---- | ----|
| token | access_token or refresh_token |
"""

user_logout="""
| Request | |
| ---- | ----|
| token | access_token or refresh_token |
"""

user_index = """
| Request | | |
| ---- | ----| ----|
| token | access_token or refresh_token |
| user_id | UserId |
| user_name | UserName |
| is_usage | UsageFlag | | 0: not_usage<br>1:is_usage|
"""

user_update = """
| Request | |
| ---- | ----|
| token | access_token or refresh_token |
| user_name | UserName |
| password | Password |
"""

user_update_usage = """
| Request | |
| ---- | ----|
| token | access_token or refresh_token |
"""