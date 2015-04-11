import logging
from pinder.celery import app

from pinder.models import User, UserDistance

logger = logging.getLogger("tasks")


@app.task(name="task_generate_distance")
def task_generate_distance(user_id):
    u = User.objects.get(id=user_id)
    all_other_users = User.objects.all()

    logger.info("Populating distance for %s" % u)

    for user in all_other_users:
        if user == u:
            continue
        dist = UserDistance.set_distance(u, user)
        logger.info("Distance between %s and %s: %s kms" % (u, user, dist))
