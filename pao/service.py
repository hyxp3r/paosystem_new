from django.core.mail import send_mail


def send(user_mail):

    send_mail("Письмо через джангу",
    "Внимание! Письмо через джангу",
    "servicensuem@gmail.com",
    [user_mail],
    fail_silently=False)

   