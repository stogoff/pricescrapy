import pkgutil
import spiders
import configparser


def createConfig(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    p = spiders
    config.add_section("Shops")
    for importer, modname, ispkg in pkgutil.iter_modules(p.__path__):
        shop_name = modname.replace('_','-')
        config.set("Shops", shop_name, '0')


    with open(path, "w") as config_file:
        config.write(config_file)


if __name__ == "__main__":
    path = "shops.cfg"
    createConfig(path)


