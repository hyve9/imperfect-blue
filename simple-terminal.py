from cmd import Cmd
from time import sleep
import readline

class AutofictionTerm(Cmd):

    name = None
    memories = None
    current_memory = None
    
    @staticmethod
    def do_exit(*args):
        return True
        
    def do_memories(self, *args):
        if not self.memories:
            print('Name missing. I don\'t know who you are. Do you?')
        else:
            print('Loading memories...')
            sleep(1)
            print('Memories found:')
            for i in range(len(self.memories)):
                print(f'{i}: {self.memories[i]}')
            selection = None
            while selection not in [str(x) for x in range(len(self.memories))]:
                selection = input(f'Please select a memory from the list above from 0 to {len(self.memories) - 1}: ')
            self.current_memory = self.memories[int(selection)]
            print(f'Loading memory {self.current_memory}...')
            print('(here some crazy VR stuff would happen...)')
            sleep(1)
    
    def do_whoami(self, *args):
        print(f'You are {self.name}, silly!')
    
    def do_rename(self, *args):
        if not args[0]:
            print('Please provide an alternative name, like \'rename Alice\'.')
        else:
            self.name = args[0]
            print(f'Ok, you are now {self.name}')
            
    def help_memories(self, *args):
        print('memories: Prints a list of available memories and allows you to select one.')
    
    def help_whoami(self, *args):
        print('whoami: Prints who you are (or at least who you said you were).')
    
    def help_rename(self, *args):
        print('rename: Allows you to rename yourself. Takes one argument, like \'rename Alice\'.')

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
                while not self.name:
                    self.name = input(f'{self.intro}\n{self.prompt}')
                    if self.name:
                        print(f'Welcome, {self.name}! You can type \'help\' to get a list of available commands.')
                        self.memories = [f'/home/{self.name}/memory_0', f'/home/{self.name}/memory_1', f'/home/{self.name}/memory_2', f'/home/{self.name}/memory_3']
                if self.cmdqueue:
                    line = self.cmdqueue.pop(0)
                else:
                    line = input(self.prompt)
            except EOFError:
                line = 'EOF'
            except KeyboardInterrupt:
                line = 'ctrl_c'
            line = self.precmd(line)
            stop = self.onecmd(line)
            stop = self.postcmd(stop, line)
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
    intro = 'Welcome to the afterlife. Please tell me your name.'
    prompt = '~! '
    terminal.cmdloop(intro=intro, prompt=prompt)
