from django.contrib.auth.tokens import PasswordResetTokenGenerator


# class MyTokenGenerator(PasswordResetTokenGenerator):
#
#     def make_token(self, user):
#         pass

account_activation_token = PasswordResetTokenGenerator()
