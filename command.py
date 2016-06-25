class Command:
    message = ''
    parameters = []
    subonly = None

    def __init__(self, message, parameters, sub):
        self.message = message
        self.parameters = parameters
        self.subonly = sub == 'true'


def load_commands():
    commands = {}
    with open('commands.data', 'r') as f:
        for line in f:
            if line[0] != '#':
                line = line.split('|')
                commands[line[0]] = Command(line[1], line[2].split(" "), line[3])

    return commands
