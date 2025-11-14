# from datetime import timedelta

# beat_schedule = {
#     'send-reminder-every-evening': {
#         'task': 'send_daily_reminders',
#         'schedule': timedelta(hours=0, minutes=0, seconds=10),
#         'options': {'expires': 3600}
#     },
# }

broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/1'
timezone = "Asia/Kolkata"
broker_connection_retry_on_startup = True