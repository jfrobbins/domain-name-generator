from os import system as sys
from random import choice
import sys

class DomainGetter:
  
  def __init__(self, args):
    self.words = [i.strip().lower() for i in open('/usr/share/dict/words').readlines()]
    self.tlds = [i.split()[0].strip().lower() for i in open('tlds.txt').readlines()]
    words = []
    Length = 0
    if len(args) >= 1:
        for i in range(0, len(args)):
            a = args[i]
            #catch the length arg if it exsists, and remove those args
            if a.lower() == '-l' or a.lower() == '--len':
                Length = float(args.pop(i + 1))
                args.pop(i)
                break

        if Length > 0:
            #actually filter out by lengths
            self.words = [w for w in self.words if len(w) <= Length]

        if len(args) > 0:
            #if there are still args (non-len), do a search for the words:
            for w in self.words:
                for a in args:
                    if a in w:
                        words.append(w)
                        break
                        #add word to the list, and go to the next word
            self.words = words
#            self.words = [a for w in self.words for a in args if a in w]
#		this list comprehension didn't work correctly...
         
  def __iter__(self):
    while len(self.words) > 1:
      
      word = choice(self.words)
      self.words.remove(word)
      
      for tld in self.tlds:
        if word.endswith(tld):
          yield '%s.%s' % (word.rstrip(tld), tld)
        else:
          yield False


domains = DomainGetter(sys.argv[1:])

for domain in domains:
  if domain:
    print domain
