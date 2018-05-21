from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=False):
        data = form.cleaned_data
        # user.username = data['username']
        user.email = data['email']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.gender = data['gender']
        user.date_of_birth = data['date_of_birth']
        user.avatar = data['avatar']
        user.university = data['university']
        user.job = data['job']
        user.country = data['country']
        user.twitter = data['twitter']
        user.facebook = data['facebook']
        user.instagram = data['instagram']
        user.bio = data['bio']
        if 'password1' in data:
            user.set_password(data['password1'])
        else:
            user.set_unusable_password()
        # self.populate_username(request, user)
        if commit:
            user.save()
        return user
