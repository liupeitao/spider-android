success_sql = """ INSERT INTO mq.mq_task_job (taskuid,app,state,"group","progress") VALUES (%s,%s,'成功',%s,%s) RETURNING id;"""
faild_sql = """ INSERT INTO mq.mq_task_job (taskuid,app,state,"group","progress") VALUES (%s,%s,'失败',%s,%s) RETURNING id;"""
