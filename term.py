from cmd import Cmd
from time import sleep
import sys
import os
import readline
from random import random
#import simpleaudio as sa

class AutofictionTerm(Cmd):
    
    text = '''
    Hello, and uh, sorry about everything. But hey, everyone’s gotta go sometime, right? 
    Anyways, here’s the deal: Everyone is entitled to the whole "life flashing before your eyes" thing. 
    
    However, we have a bit of a pickle. 
    
    As you probably already know (considering that you’re here), we have quite a backlog of people waiting, and they love to reminisce and 
    remember and go through the catalogs, over and over and over. Some people want to stay here forever. 
    Unfortunately, we can’t really afford that right now. So, we’ve set up some chairs for you to experience sections of your life. 
    We ask that you only view a section. Spending too much time here, viewing different sections, tends to have, uh, undesirable aftereffects. Anyways, enjoy! 
    
    And uh, hurry up. 
    
    The clock’s ticking.
    '''
    start = False
    time = 150
    speed = 80
    progress = 0
    
    @staticmethod
    def do_exit(*args):
        return True
    
    def termprint(self):
        for l in self.text:
            sys.stdout.write(l)
            sys.stdout.flush()
            sleep(random()*10.0/self.speed)
        print('')
        
    def termloadbar(self):
        print('\r [{0}] {1}%'.format('#'*(self.progress//10), self.progress), end='')
    
    def termcountdown(self):
        #beep = sa.WaveObject.from_wave_file('resources/audio/beep.wav')
        print('\n\nTime remaining:')
        while self.time >= 0:
            mins, secs = divmod(self.time, 60)
            print('\r {:02d}:{:02d}'.format(mins, secs), end='')
            #beep.play()
            sleep(1.3)
            self.time -= 1
        print('\nTime\'s up.')
        
    def preloop(self):
        clear = lambda : os.system('tput reset')
        clear()
    
    def postloop(self):
        clear = lambda : os.system('tput reset')
        clear()

    def cmdloop(self, intro, prompt):
        self.preloop()
        self.old_completer = readline.get_completer
        readline.set_completer(self.complete)
        readline.parse_and_bind(self.completekey + ': complete')
        stop = None
        self.intro = intro
        self.prompt = prompt
        while not stop:
            try:
                while not self.start:
                    line = input(f'{self.intro}\n{self.prompt}')
                    self.start = True
                if(self.time > 0):
                    self.termprint()
                    while self.progress <= 100:
                        self.termloadbar()
                        self.progress += 1
                        sleep(0.05)
                    self.termcountdown()
                if self.cmdqueue:
                    line = self.cmdqueue.pop(0)
                #else:
                #    line = input(self.prompt)
            except EOFError:
                line = 'EOF'
            except KeyboardInterrupt:
                line = 'ctrl_c'
            line = self.precmd(line)
            stop = self.onecmd(line)
            stop = self.postcmd(stop, line)
            stop = True
        self.postloop()

    def onecmd(self, line):
        cmd, arg, line = self.parseline(line)
        if not line:
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line
        if line == 'EOF':
            self.lastcmd = ''
        if line == 'ctrl_c':
            print()
            return
        if cmd == '':
            return self.default(line)
        else:
            try:
                func = getattr(self, "do_" + cmd)
            except AttributeError:
                return self.default(line)
            return func(arg)

    def emptyline(self):
         pass

if __name__ == '__main__':
    terminal = AutofictionTerm()
    intro = 'Press enter to continue. (And hurry up.)'
    prompt = '~! '
    terminal.cmdloop(intro=intro, prompt=prompt)
