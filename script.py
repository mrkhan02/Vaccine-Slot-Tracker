import  os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'covid.settings')
django.setup()
from app.models import Query

l=Query.objects.all()
for i in l:
    print(i.name)