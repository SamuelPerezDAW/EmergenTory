from django_rq import job


# Hacer esto cuando se tenga al menos la estructura del front
@job
def send_reset_password(user) -> None:
    pass
