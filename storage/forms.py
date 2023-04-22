from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "first_name", "last_name", "email", "username", "password1", "password2"
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True

        # remove autofocus from username
        self.fields['username'].widget.attrs.pop("autofocus", None)

        # add autofocus in first_name
        self.fields['first_name'].widget.attrs.update({"autofocus": True})
