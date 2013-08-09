from os import system as sys
from random import choice
import sys

class DomainGetter:
  
    def __init__(self, args):
        self.words = [i.strip().lower() for i in open('/usr/share/dict/words').readlines()]
        self.tlds = [i.split()[0].strip().lower() for i in open('tlds.txt').readlines()]
        words = []
        self.length = 0
        self.startsWith = None
        self.endsWith = None
        self.wordsOnly = False
        self.args = args
    
        if len(args) >= 1:
            #there are arguments
            args = self.getNonWordArgs()

            if self.length > 0:
                #actually filter out by lengths
                self.words = [w for w in self.words if len(w) <= self.length]

            if self.startsWith != None:
                self.words = [w for w in self.words if w[0:len(self.startsWith)] == self.startsWith]
                
            if self.endsWith != None:
                self.words = [w for w in self.words if w[0-len(self.endsWith):] == self.endsWith]            
                
            if len(args) > 0:
                print args
                #if there are still args (non-len), do a search for the words:
                for w in self.words:
                    for a in args:                        
                        if a in w:
                            words.append(w)
                            break
                            #add word to the list, and go to the next word
                self.words = words
                #self.words = [a for w in self.words for a in args if a in w]
                #this list comprehension didn't work correctly...
                del words

    def getNonWordArgs(self):
        args = self.args

        for a in args:
            print a
            #catch the length arg if it exists, and remove those args
            i = args.index(a)
            if a.lower() == '-l' or a.lower() == '--len':
                self.length = float(args.pop(i + 1))                

            #catch the length arg if it exists, and remove those args
            elif a.lower() == '-l' or a.lower() == '--len':
                self.length = float(args[i + 1])
                args.pop(i + 1)
        
            elif a.lower() == '--starts-with':
                self.startsWith = args[i + 1]
                args.pop(i + 1)

            elif a.lower() == '--ends-with':
                self.endsWith = args[i + 1]
                args.pop(i + 1)

            elif a.lower() == '--words-only':
                self.wordsOnly = True

        #clear the args out of the list:
        args = [a for a in args if not '--' in a]

        self.args = args
        return args
         
    def __iter__(self):
        while len(self.words) > 1:
            word = choice(self.words)
            self.words.remove(word)

            if self.wordsOnly == False:
                for tld in self.tlds:
                    if word.endswith(tld) and len(word.rstrip(tld)) >= 3:
                        yield '%s.%s' % (word.rstrip(tld), tld)
                    else:
                        yield False
            else:
                yield word    


###############################################

if __name__ == '__main__':
    domains = DomainGetter(sys.argv[1:])

    for domain in domains:
      if domain:
        print domain
