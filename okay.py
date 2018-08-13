from moviepolls.models import Choice, Movie

for i,movie in enumerate(Movie.objects.all()):
    m = Movie.objects.get(pk=i+1)
    m.choice_set.create(choice_text='Meh', votes=0)
    m.choice_set.create(choice_text='Supermegafoxyawesomehot', votes=0)
    m.choice_set.create(choice_text='Terrible', votes=0)
