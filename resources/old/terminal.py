from cmd import Cmd

class AutofictionTerm(Cmd):

    name = None
    
    @staticmethod
    def do_exit(*args):
        return True
        
    def do_foo(*args):
        for i in range(1, len(args)):
            print(args[i])
        
    def do_bar(*args):
        print('bars')
    
    def do_whoami(self, *args):
        print(f'You are {self.name}, silly!')
    
    def do_rename(self, *args):
        if not args[0]:
            print('Please provide an alternative name, like \'rename Alice\'.')
        else:
            self.name = args[0]
            print(f'Ok, you are now {self.name}')

    def cmdloop(self, intro=None):

        self.preloop()
        if self.use_rawinput and self.completekey:
            try:
                import readline

                self.old_completer = readline.get_completer()
                readline.set_completer(self.complete)
                readline.parse_and_bind(self.completekey + ': complete')
            except ImportError:
                pass
        try:
            if intro is not None:
                self.intro = intro
            if self.intro:
                self.stdout.write(str(self.intro) + "\n")
            stop = None
            while not self.name:
                if self.cmdqueue:
                    self.name = self.cmdqueue.pop(0)
                else:
                    if self.use_rawinput:
                        try:
                            self.name = input(self.prompt)
                        except EOFError:
                            pass
                        except KeyboardInterrupt:
                            self.stdout.write('Try again.\n')
                    else:
                        self.stdout.write(self.prompt)
                        self.stdout.flush()
                        self.name = self.stdin.readline()
                        if not len(line):
                            self.name = 'nobody'
                        else:
                            self.name = line.rstrip("\r\n")
            self.stdout.write(f'Welcome, {self.name}!\n')
            while not stop:
                if self.cmdqueue:
                    line = self.cmdqueue.pop(0)
                else:
                    if self.use_rawinput:
                        try:
                            line = input(self.prompt)
                        except EOFError:
                            line = "EOF"
                        except KeyboardInterrupt:
                            line = "ctrl_c"
                    else:
                        self.stdout.write(self.prompt)
                        self.stdout.flush()
                        line = self.stdin.readline()
                        if not len(line):
                            line = "EOF"
                        else:
                            line = line.rstrip("\r\n")
                line = self.precmd(line)
                stop = self.onecmd(line)
                stop = self.postcmd(stop, line)
            self.postloop()
        finally:
            if self.use_rawinput and self.completekey:
                try:
                    import readline

                    readline.set_completer(self.old_completer)
                except ImportError:
                    pass

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
            self.stdout.write("\n")
            return
        if cmd == '':
            return self.default(line)
        else:
            try:
                func = getattr(self, "do_" + cmd)
            except AttributeError:
                return self.default(line)
            return func(arg)


p = AutofictionTerm()
intro = ''' 
Welcome to the afterlife. Please tell me your name.
'''
p.cmdloop(intro=intro)
