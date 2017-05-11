import importlib
import glob

def create_loader(name):        
    def getModule():
        module = importlib.import_module("rules."+name)
        return module   
    
    return getModule

loaders = {}
for file in glob.glob("rules/*.py"):
    rule= file.replace("rules/", "").replace(".py", "")    
    loaders[rule] = create_loader(rule)
        
def get_rules(name):
    return loaders[name]().build_rules()