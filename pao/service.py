from django.core.mail import send_mail


def send(user_mail):

    send_mail("Вы подписались на бусинную рыссылку",
    "Внимание! Если вам пришло данное письмо, значит вы получили автоматическое письмо от бусиного приложения",
    "servicensuem@gmail.com",
    [user_mail],
    fail_silently=False)

   