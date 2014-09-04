import random
def popularityBasedRandomApp():
   b = list(a.items())
   total = sum(w for c, w in b)
   r = random.uniform(0, total)
   upto = 0
   for c, w in b:
      if upto + w > r:
         return c
      upto += w
   assert False, "Shouldn't get here"


a = {}
a[1] = 2
a[3] = 4
print(popularityBasedRandomApp())