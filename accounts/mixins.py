from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class ApplicantRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_active and self.request.user.is_applicant


class CompanyRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_active and self.request.user.is_employer