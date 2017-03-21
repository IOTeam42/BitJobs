from django.views.generic import TemplateView


class RegisterView(TemplateView):
    template_name = "base/registration.html"

    def get_context_data(self, **kwargs):
        super(RegisterView).__init__(**kwargs)


class LoginView(TemplateView):
    template_name = "base/login.html"

    def get_context_data(self, **kwargs):
        super(LoginView).__init__(**kwargs)
