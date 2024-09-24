import pandas as pd

from gen import recipe_gen
from classifier import model_pred
import json
import warnings
warnings.filterwarnings("ignore")

def convert(l):
    res = {}
    for i in range(0, len(l)):
        res[i+1] = l[i]
    
    return res

def generate_formulation(ingrdients, number_of_experiments, constraints):
    all_ingrdients = [
                      'I-003001_S-000102', 'I-003002_S-004001', 'I-003003_S-004002', 'I-003004_S-000102', 'I-003005_S-000102',
                      'I-003006_S-000102', 'I-003007_S-000102', 'I-003008_S-000102', 'I-003009_S-000102', 'I-003010_S-000102',
                      'I-003011_S-000102', 'I-003012_S-000102', 'I-003013_S-000102', 'I-003014_S-000102', 'I-003015_S-000102',
                      'I-003016_S-000102', 'I-003017_S-000102', 'I-003018_S-000102', 'I-003019_S-000102', 'I-003021_S-000102',
                      'I-003022_S-000102', 'I-003023_S-000102', 'I-003024_S-000102', 'I-003025_S-000102', 'I-003026_S-000102',
                      'I-003027_S-000102', 'I-003028_S-000102', 'I-003029_S-000102', 'I-003030_S-000102', 'I-003031_S-000102',
                      'I-003032_S-000102', 'I-003130_S-004003', 'I-003033_S-002001', 'I-003034_S-000102', 'I-003131_S-004007',
                      'I-003035_S-000102', 'I-003036_S-000102', 'I-003037_S-004004', 'I-003038_S-000102', 'I-003039_S-004005',
                      'I-003040_S-004006', 'I-003042_S-000102', 'I-003043_S-000102', 'I-003044_S-000102', 'I-003045_S-000102',
                      'I-003046_S-000102', 'I-003047_S-000102', 'I-003048_S-000102', 'I-003049_S-000102', 'I-003050_S-000102',
                      'I-003051_S-000102', 'I-003052_S-000102', 'I-003053_S-000102', 'I-003054_S-000102', 'I-003055_S-000102',
                      'I-003056_S-000102', 'I-003057_S-000102', 'I-003058_S-000102', 'I-001013_S-000102', 'I-003059_S-000102',
                      'I-003060_S-000102', 'I-003061_S-000102', 'I-003062_S-000102', 'I-003063_S-000102', 'I-003064_S-000102',
                      'I-003065_S-000102', 'I-003066_S-000102', 'I-003067_S-000102', 'I-003068_S-000102', 'I-003069_S-000102',
                      'I-003070_S-000102', 'I-003071_S-000102', 'I-003072_S-000102', 'I-003073_S-000102', 'I-003074_S-000102',
                      'I-003075_S-000102', 'I-003076_S-000102', 'I-003077_S-000102', 'I-003078_S-000102', 'I-003079_S-000102',
                      'I-003080_S-000102', 'I-003081_S-000102', 'I-003082_S-000102', 'I-003083_S-000102', 'I-003084_S-000102',
                      'I-003085_S-000102', 'I-003086_S-000102', 'I-003087_S-000102', 'I-003088_S-000102', 'I-003089_S-000102',
                      'I-003090_S-000102', 'I-003091_S-000102', 'I-003092_S-000102', 'I-003093_S-000102', 'I-003094_S-000102',
                      'I-003095_S-000102', 'I-003096_S-000102', 'I-003097_S-000102', 'I-003098_S-000102', 'I-003099_S-000102',
                      'I-003100_S-000102', 'I-003101_S-000102', 'I-003102_S-000102', 'I-003103_S-000102', 'I-003104_S-000102',
                      'I-003105_S-000102', 'I-003106_S-000102', 'I-003107_S-000102', 'I-003108_S-000102', 'I-003109_S-000102',
                      'I-003110_S-000102', 'I-003111_S-000102', 'I-003112_S-000102', 'I-003113_S-000102', 'I-003114_S-000102',
                      'I-003115_S-000102', 'I-003116_S-000102', 'I-001014_S-002011', 'I-003117_S-000102', 'I-003118_S-000102',
                      'I-003119_S-000102', 'I-003120_S-000102', 'I-000002_S-000102', 'I-003121_S-000102', 'I-003122_S-000102',
                      'I-003123_S-000102', 'I-003124_S-000102', 'I-003125_S-000102', 'I-003126_S-000102', 'I-003127_S-000102',
                      'I-003128_S-000102', 'I-003129_S-000102'
                      ]
    
    final_op = {}
    if set(ingrdients) > set(all_ingrdients):
        final_op["message"] = "This ingredient(s) has not been used for AI model training"
        final_op["status"] = False
        final_op["results"] = []
    
    else: 
        ingrdients_df = pd.DataFrame(all_ingrdients, columns=['ingredients'])

        # edit 2024-09-16
        # -------------------------------------------------------------------------------------------------------------------------------
        constraints_list = constraints.split(" & ")
        conditions = []
        for const in constraints_list:
            param = const.split(" ")[0]
            cond = const.split(" ")[1]
            if cond == "Range":
                value = [float(const.split(" ")[2].split("-")[0]), float(const.split(" ")[2].split("-")[1])]
            else:
                value = bool(const.split(" ")[2])
            conditions.append([param, cond, value])
        
        final_op_list = []

        for i in range(number_of_experiments):
            loop_cond = True
            loop_limit = 500
            iter = 0
            while(loop_cond):
                iter += 1
                reco = recipe_gen(
                            num_recommendations = 1, 
                            confidence_threshold = 0.9, 
                            constraints = constraints,
                            selected_cols = ingrdients
                            )
        # -------------------------------------------------------------------------------------------------------------------------------        
                for r in range(len(reco)):
                    temp_op = {}
                    temp_op["project"] = "Proteinbar"
                    temp_op["trial_name"] = "Exp-" + str(i+1)
                    temp_op["confidence_score"] = reco[r][1]
                    
                    op_series = reco[r][0]
                    op_df = pd.DataFrame({'ingredients': op_series.index, 'value': op_series.values})
                    merged_df = pd.merge(ingrdients_df, op_df, how = 'left', on = 'ingredients')
                    merged_df['value'] = merged_df['value'].fillna(0)
                    
                    op_ingredients_list = []
                    for index, row in merged_df.iterrows():
                        temp_dict = {}
                        temp_dict["ingredient_name"] = row['ingredients']
                        temp_dict["value"] = row['value']
                        op_ingredients_list.append(temp_dict)

                    temp_op["ingredients_selected"] = op_ingredients_list

                    temp_list = []
                    for x in merged_df.values:
                        temp_list.append(x[1])
                    temp_op["optimization_scores"] = model_pred(temp_list)

                    # edit 2024-09-01
                    # -------------------------------------------------------------------------------------------------------------------------------
                    if (
                        # (temp_op["optimization_scores"]["OP_000022"] == conditions[2][-1]) 

                        (temp_op["optimization_scores"]["OP_000007"] >= conditions[0][-1][0] and temp_op["optimization_scores"]["OP_000007"] <= conditions[0][-1][-1]) 
                        and (temp_op["optimization_scores"]["OP_000022"] == conditions[2][-1]) 
                        # and (temp_op["optimization_scores"]["OP_000012"] >= conditions[1][-1][0] and temp_op["optimization_scores"]["OP_000012"] <= conditions[1][-1][-1])
                        # and (temp_op["optimization_scores"]["OP_000023"] >= conditions[3][-1][0] and temp_op["optimization_scores"]["OP_000023"] <= conditions[3][-1][-1])
                        # and (temp_op["optimization_scores"]["OP_000006"] >= conditions[4][-1][0] and temp_op["optimization_scores"]["OP_000006"] <= conditions[4][-1][-1])
                        # and (temp_op["optimization_scores"]["OP_000024"] >= conditions[5][-1][0] and temp_op["optimization_scores"]["OP_000024"] <= conditions[5][-1][-1])
                        and (iter < loop_limit)
                        ) :
                        final_op_list.append(temp_op)
                        loop_cond = False
                    if iter == loop_limit:
                        loop_cond = False
  
        if len(final_op_list) == number_of_experiments:
            final_op["message"] = "Formulations successfully generated"
            final_op["status"] = True
            final_op["results"] = final_op_list
        else:
            final_op["message"] = "Formulation not generated"
            final_op["status"] = False
            final_op["results"] = []
        # -------------------------------------------------------------------------------------------------------------------------------
    
    final_op_json = json.dumps(final_op, indent=4)
    print(final_op_json)
    return final_op_json