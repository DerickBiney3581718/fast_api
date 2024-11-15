from configparser import ConfigParser


def load_config(filename='env/database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in file {filename}')

    return config

def load_jwt_config(filename='env/database.ini', section='jwt'):
    parser = ConfigParser()
    parser.read(filename)

    config ={}
    if parser.has_section(section):
        params = parser.items(section)
        for p in params:
            config[p[0]] = p[1]
    else:
        raise Exception(f'Section {section} not found in file {filename}')
    return config


if __name__ == '__main__':
    config = load_config()
    print(config)
