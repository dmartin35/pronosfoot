"""
Site maintenance script
"""
from tools.djangodb import executeRawSqlQuery

def delete_expired_sessions():
    """
    delete sessions that expired at least one day ago
    """
    sql = """DELETE FROM `django_session` WHERE `expire_date` < DATE_SUB( CURDATE( ) , INTERVAL 0 DAY );"""
    executeRawSqlQuery(sql)

if __name__ == '__main__':
    delete_expired_sessions()