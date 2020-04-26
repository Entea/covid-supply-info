from django.contrib.auth.models import User, Group

from distributor.models import Hospital


def run(*args):
    for line in args:
        username, password = line.split(':')
        try:
            hospital = Hospital.objects.get(code=username)
            user = User.objects.create_user(username, password=password, is_superuser=False, is_staff=True)
            user.save()

            group = Group.objects.get(name='Hospital Managers')
            group.user_set.add(user)

            hospital.managers.add(user)
        except:
            print(f'Hospital with code {username} not found')
