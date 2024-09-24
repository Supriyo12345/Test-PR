from combined import generate_formulation
import argparse
import json
import os

# This step is crucial to ensure that files are loaded correctly,
# as it sets the current working directory to the location of this script.
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main(input):    
    ingrdients = [item["ingredient_name"] for item in input["ingredients_selected"]]
    number_of_experiments = input["number_of_experiments"]
    constraints =   input["desired_optimization"][0]["optimization_name"] + " " + input["desired_optimization"][0]["operator"] + " " + str(input["desired_optimization"][0]["value"]) + " & " + \
                    input["desired_optimization"][1]["optimization_name"] + " " + input["desired_optimization"][1]["operator"] + " " + str(input["desired_optimization"][1]["value"]) + " & " + \
                    input["desired_optimization"][2]["optimization_name"] + " " + input["desired_optimization"][2]["operator"] + " " + str(input["desired_optimization"][2]["value"]) + " & " + \
                    input["desired_optimization"][3]["optimization_name"] + " " + input["desired_optimization"][3]["operator"] + " " + str(input["desired_optimization"][3]["value"]) + " & " + \
                    input["desired_optimization"][4]["optimization_name"] + " " + input["desired_optimization"][4]["operator"] + " " + str(input["desired_optimization"][4]["value"]) + " & " + \
                    input["desired_optimization"][5]["optimization_name"] + " " + input["desired_optimization"][5]["operator"] + " " + str(input["desired_optimization"][5]["value"]) 
    return generate_formulation(ingrdients, number_of_experiments, constraints)


# Sample usage
# python main.py --ingredients '["I-000004_S-000104", "I-000005_S-000104", "I-000014_S-000104", "I-000006_S-000104", "I-000007_S-000105", "I-000001_S-000101", "I-000008_S-000102", "I-000009_S-000107", "I-000010_S-000107", "I-000011_S-000108"]' --optimization_parameters '[{"code": "OP_000007", "value": "5-14", "operator": "Range"}, {"code": "OP_000001", "value": true, "operator": "Equal"}, {"code": "OP_000002", "value": "1-5", "operator": "Range"}, {"code": "OP_000003", "value": "1-5", "operator": "Range"}, {"code": "OP_000004", "value": "1-5", "operator": "Range"}, {"code": "OP_000005", "value": "1-5", "operator": "Range"}]' --number_of_experiments 10
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Execute the AI model with given parameters.")
    parser.add_argument('--ingredients', type=str,
                        required=True, help='List of ingredients')
    parser.add_argument('--optimization_parameters', type=str,
                        required=True, help='Optimization parameters')
    parser.add_argument('--number_of_experiments', type=int,
                        required=True, help='Number of experiments to run')

    args = parser.parse_args()

    ingredients = json.loads(args.ingredients)
    optimization_parameters = json.loads(args.optimization_parameters)
    number_of_experiments = args.number_of_experiments

    main(ingredients, optimization_parameters, number_of_experiments)

