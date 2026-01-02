import os
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    help = 'Sets up Google OAuth configuration from environment variables'

    def handle(self, *args, **options):
        client_id = os.getenv('GOOGLE_CLIENT_ID')
        client_secret = os.getenv('GOOGLE_CLIENT_SECRET')

        if not client_id or not client_secret:
            self.stdout.write(
                self.style.ERROR(
                    'GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set in environment variables'
                )
            )
            return

        # Get or create the Google social app
        social_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google',
                'client_id': client_id,
                'secret': client_secret,
            }
        )

        if not created:
            # Update existing app
            social_app.client_id = client_id
            social_app.secret = client_secret
            social_app.save()
            self.stdout.write(
                self.style.SUCCESS('Updated existing Google OAuth app')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Created new Google OAuth app')
            )

        # Add the app to the current site
        current_site = Site.objects.get_current()
        if current_site not in social_app.sites.all():
            social_app.sites.add(current_site)
            self.stdout.write(
                self.style.SUCCESS(f'Added Google OAuth app to site: {current_site.domain}')
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'Google OAuth setup complete!\n'
                f'Client ID: {client_id[:20]}...\n'
                f'Site: {current_site.domain}'
            )
        )