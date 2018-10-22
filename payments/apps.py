from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    name = 'payments'
    verbose_name = 'Payments'

    def ready(self):
        #import signal handlers
        import payments.signals
