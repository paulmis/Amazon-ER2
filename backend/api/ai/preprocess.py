import pandas as pd
import numpy as np
import os
# hash
import hashlib
import warnings
warnings.filterwarnings("ignore")

def get_preprocessed_dataset(min_reviews = 10, exclude_5_star = True, min_review_length = 20, max_review_length = 5000):
    """Returns a preprocessed dataset of Amazon reviews. The dataset is cached in data/preprocessed_dataset_{hash}.csv"""
    # hash of the parameters
    hash = str(hashlib.sha256(str(min_reviews).encode("utf-8") + str(exclude_5_star).encode("utf-8") + str(min_review_length).encode("utf-8") + str(max_review_length).encode("utf-8")).hexdigest())
    
    # We check if the dataset is present in dataset/preprocessed_dataset_{hash}.csv
    if os.path.isfile("data/preprocessed_dataset_" + hash + ".csv"):
        return pd.read_csv("data/preprocessed_dataset_" + hash + ".csv")
    
    reviews_df = pd.read_csv("data/Amazon_Unlocked_Mobile.csv")
    
    # Reviews only of products with more than 10 reviews
    reviews_df = reviews_df.groupby("Product Name").filter(lambda x: len(x) > min_reviews)
    # We also ignore reviews with 5 stars
    if exclude_5_star:
        reviews_df = reviews_df[reviews_df["Rating"] != 5]
    # The review must be more than > 20 characters
    reviews_df = reviews_df[reviews_df["Reviews"].str.len() > min_review_length]
    reviews_df = reviews_df[reviews_df["Reviews"].str.len() < max_review_length]

    products = reviews_df["Product Name"].unique()
    
    preprocessed_dataset = process_product_reviews(reviews_df, products)
    
    # Save the preprocessed dataset
    preprocessed_dataset.to_csv("data/preprocessed_dataset_" + hash + ".csv", index=False)
    
    return preprocessed_dataset
    
#############################################################################################################
# Helpers
############################################################################################################# 

def get_number_of_reviews_to_sample(actual_reviews_number):
    if actual_reviews_number == 0:
        return 0
    if actual_reviews_number < 50:
        return actual_reviews_number
    return min(actual_reviews_number, int(np.log(actual_reviews_number) * 10))

def process_product_reviews(reviews_df, products):
    final_df = pd.DataFrame()
    expected_reviews = 0
    for product in products:
        # Create a copy to avoid setting values on a slice of the original DataFrame
        product_reviews = reviews_df[reviews_df["Product Name"] == product].copy()

        number_of_reviews_to_sample = get_number_of_reviews_to_sample(len(product_reviews))
        expected_reviews += number_of_reviews_to_sample
        if number_of_reviews_to_sample == 0:
            continue

        # Use .loc for safe assignment
        product_reviews.loc[:, "Length of Reviews"] = product_reviews["Reviews"].str.len()
        product_reviews.loc[:, "Review Votes"] = product_reviews["Review Votes"].fillna(0).astype(int)

        # Apply the Pareto frontier function
        selected_reviews = pareto_frontier(product_reviews, number_of_reviews_to_sample)

        # Concatenate the results
        final_df = pd.concat([final_df, selected_reviews])

    return final_df

def pareto_frontier(df, n):
    # Sort the DataFrame by likes (descending) and length (descending)
    sorted_df = df.sort_values(by=['Review Votes', 'Length of Reviews'], ascending=[False, False])

    # Initialize an empty list to store the indices of Pareto optimal points
    pareto_frontier_indices = []

    # Iterate through the sorted DataFrame
    for i in range(len(sorted_df)):
        # Get the current row
        row = sorted_df.iloc[i]

        # Check if the current row is dominated by any of the selected rows
        dominated = False
        for j in pareto_frontier_indices:
            selected_row = sorted_df.iloc[j]
            if selected_row['Review Votes'] >= row['Review Votes'] and selected_row['Length of Reviews'] >= row['Length of Reviews']:
                dominated = True
                break

        # If not dominated, add it to the Pareto frontier
        if not dominated:
            pareto_frontier_indices.append(i)

        # If we have enough Pareto points, break
        if len(pareto_frontier_indices) == n:
            break

    # If the Pareto frontier does not have enough points, add the next best points
    if len(pareto_frontier_indices) < n:
        additional_indices = set(range(len(sorted_df))) - set(pareto_frontier_indices)
        additional_indices = sorted(additional_indices)[:n - len(pareto_frontier_indices)]
        pareto_frontier_indices.extend(additional_indices)

    # Return the rows corresponding to the Pareto frontier and additional points
    return sorted_df.iloc[pareto_frontier_indices]

