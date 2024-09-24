import pickle
import os
import warnings
warnings.filterwarnings("ignore")

def rename_param(param):
    match param:
        case 'OP_000007':
            return 'OP_000007'
        case 'OP_000012':
            return 'OP_000012'
        case 'OP_000022':
            return 'OP_000022'
        case 'OP_000023':
            return 'OP_000023'
        case 'OP_000006':
            return 'OP_000006'
        case 'OP_000024':
            return 'OP_000024'
        
def read_model(path):
    with open(str(path), 'rb') as f:
        model = pickle.load(f)
    
    return model

def model_pred(temp_list):
    home = './'
    model = read_model(path = os.path.join(home, 'Proteinbar/Model/', 'parameter_classifier.pkl'))
    result = model.predict([temp_list])[0]

    res_ret = {}
    for value, parameter_name in zip(result, ['OP_000007','OP_000012','OP_000022','OP_000023','OP_000006','OP_000024']):
        if rename_param(parameter_name) == 'OP_000022':
            res_ret[rename_param(parameter_name)] = True if value == 1 else False # int(value)
        else:
            res_ret[rename_param(parameter_name)] = round(value, 4)
                
    return res_ret