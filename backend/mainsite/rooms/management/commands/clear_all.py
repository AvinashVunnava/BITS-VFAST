from django.core.management.base import BaseCommand
from rooms.models import NormalRoom


class Command(BaseCommand):
    help = 'This is for creating rooms'

    def add_arguments(self, parser):
        parser.add_argument('no_of_rooms', type=int)

    def handle(self, *args, **kwargs):
        NormalRoom.objects.all().delete()

        self.stdout.write("Rooms DELETED")

