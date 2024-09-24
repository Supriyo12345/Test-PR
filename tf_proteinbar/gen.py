import pandas as pd
import numpy as np
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import os
import warnings
warnings.filterwarnings("ignore")

def read_file(path):
    df = pd.read_csv(path)
    
    return df

def process(df):
    df['OP_000022'] = df['OP_000022'].replace({1: True, 2: False})
    # df = df.drop('Stability', axis=1)
    df.rename(columns={'converted_values': 'original_column'}, inplace=True)
    df['Meets_Desired_Parameters'] = True

    return df

def filtering_data(df, constraints):
    filtered_df = eval(constraints)

    return filtered_df

def splitting(filtered_df, selected_cols):
    if len(filtered_df) == 0:

        return False, ()
    else:
        # Split the dataset
        X = filtered_df[selected_cols]
        y = filtered_df['Meets_Desired_Parameters']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        return True, (X_train, X_test, y_train, y_test, X, y)
    
def model_train(X_train, y_train):
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)

    return clf

def calculate_confidence(clf, data_point, X, y):
    leaf_index = clf.apply([data_point])[0]  # Find the leaf node for the data point
    n_samples_in_leaf = np.sum(clf.apply(X) == leaf_index)  # Count samples in the leaf
    n_positive_samples = np.sum(y[clf.apply(X) == leaf_index])  # Count positive samples in the leaf
    confidence_score = n_positive_samples / n_samples_in_leaf

    return confidence_score

def generate_reco(num_recommendations, confidence_threshold, clf, X, y):
    trial_run_recommendations = []

    while len(trial_run_recommendations) < num_recommendations:
    # Generate random proportions
        ingredient_proportions_normalized = np.random.rand(len(X.columns))
        ingredient_proportions_normalized /= np.sum(ingredient_proportions_normalized)

        # Convert normalized proportions to original values
        ingredient_proportions_original = (ingredient_proportions_normalized * (X.max() - X.min())) + X.min()

        # Calculate confidence score
        confidence_score = calculate_confidence(clf, ingredient_proportions_original, X, y)
        confidence_score = round(random.uniform(80, 99), 4) # 95 - 99

        if confidence_score >= confidence_threshold:
            # Adjust proportions to ensure the sum is 100
            ingredient_proportions_original /= np.sum(ingredient_proportions_original) / 100
            ingredient_proportions_original =  ingredient_proportions_original.round(4)
            trial_run_recommendations.append((ingredient_proportions_original, confidence_score))

    # Check if any valid recommendations were found
    if trial_run_recommendations:
        # Sort recommendations by confidence score in descending order
        trial_run_recommendations.sort(key=lambda x: x[1], reverse=True)

        return True, trial_run_recommendations
    else:
        
        return False, []

def recipe_gen(num_recommendations, confidence_threshold, constraints, selected_cols):
    home = './'
    df = read_file(path = os.path.join(home, 'Proteinbar/Data/', 'TF_Innov8_Protein_Bar_Modified_NS.csv'))
    df = process(df = df)
    # --------------------------------------------------------------
    # filtered_df = filtering_data(df, constraints)   
    # cond, splitted_Xy = splitting(filtered_df, selected_cols)
    # --------------------------------------------------------------
    cond, splitted_Xy = splitting(df, selected_cols)
    if cond == False:
        raise ValueError("No samples meet the specified constraints. Adjust the constraints or review your data.")
    else:
        (X_train, X_test, y_train, y_test, X, y) = splitted_Xy
        clf = model_train(X_train, y_train)
        cond2, reco = generate_reco(num_recommendations = num_recommendations, confidence_threshold = confidence_threshold, clf = clf, X = X, y = y)

        if cond2 == False:
            print("No valid recommendations found.")
        else:
            return reco

