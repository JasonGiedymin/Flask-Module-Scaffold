from flask import Module

def registerAssets(assets):
    pass

def getModule(fq_module_name, url_prefix=None, static_path=None, subdomain=None):
    module_name = getFinalName(fq_module_name)
    
    if url_prefix is not None:
        return Module(fq_module_name, module_name, url_prefix=url_prefix, static_path=static_path, subdomain=subdomain)
    else:
        return Module(fq_module_name, module_name, static_path=static_path, subdomain=subdomain)

def getFinalName(fq_name_string):
    return(fq_name_string.split('.')[len(fq_name_string.split('.')) - 1])

