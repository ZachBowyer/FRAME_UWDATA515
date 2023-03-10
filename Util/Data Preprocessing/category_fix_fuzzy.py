import pandas as pd

# Create a DataFrame with the column "Menuitemcategory"
df = pd.DataFrame({
    'Menuitemcategory': [
        'Picked for you',
        'Starters (all vegetarian)',
        'Vegetarian Entrees',
        'Entrees',
        'Desserts and Beverages',
        'Side Orders',
        'Sweets',
        'Sides',
        'Saj',
        'Mezze',
        'Salads',
        'Plates',
        'Sandwiches',
        'Platters',
        'Appetizers',
        'More Items',
        'Sandwich',
        'Beverages',
        'Combo Sides',
        'Build Your Own',
        'Seasonal Salads',
        'Signature Salads',
        'Everyday Ice Cream',
        'Add Ons',
        'Merch',
        'Mains',
        'Our Mainstay Pints',
        'Our Seasonal Pints',
        'Whatâ€™s New?',
        'Get Loaded Weekend',
        'Taco Packs',
        'Burritos',
        'Tacos',
        'Nachos',
        'Bowls',
        'Desserts',
        'EntrÃ©es',
        'Curried EntrÃ©es w/Rice',
        'Dessert',
        'Sandwiches and Wraps',
        'Drinks',
        'Starters',
        'Dhalpurie Roti',
        'Paratha Roti',
        'Milk Teas',
        'Fresh Milk Series',
        'Refreshing Fruit Teas',
        'Blended Drinks',
        'Salted Cloud Series',
        'Specialties',
        'Yakult Series',
        'Dessert &amp; Snacks',
        'Coffee',
        'Simply Teas',
        'Salads',
        'Pizza',
        'Individual Cookies'
    ]
})

# Define a function that maps each value to its corresponding group
def map_to_group(value):
    if 'Salad' in value:
        return 'Salads'
    elif 'Dessert' in value or 'Sweet' in value or 'Ice Cream' in value:
        return 'Desserts and Beverages'
    elif 'Sandwich' in value or 'Wrap' in value:
        return 'Sandwiches and Wraps'
    elif 'Appetizer' in value or 'Starter' in value:
        return 'Appetizers'
    elif 'Side' in value or 'Add On' in value or 'Combo' in value:
        return 'Sides'
    elif 'Pizza' in value:
        return 'Entrees'
    elif 'Beverage' in value or 'Drink' in value or 'Tea' in value or 'Coffee' in value:
        return 'Drinks'
    else:
        return 'Entrees'

# Apply the function to the "Menuitemcategory" column using the apply() method and group the DataFrame by the resulting groups
grouped = df.groupby(df['Menuitemcategory'].apply(map_to_group))

# Print the groups
for group_name, group_df in grouped:
    print(f'{group_name}:')
    print(group_df)

new_df = pd.DataFrame({
    'Menuitemcategory': df['Menuitemcategory'],
    'Group': df['Menuitemcategory'].apply(map_to_group)
})

# Write the new DataFrame to a CSV file with only the "Menuitemcategory" and "Group" columns
new_df.to_csv('menuitemcategory.csv', columns=['Menuitemcategory', 'Group'], index=False)