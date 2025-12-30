# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

cnx=st.connection("snowflake")
session=cnx.session()

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your Smoothie!"""
)

# option = st.selectbox(
#     "What's your favorite fruit?",
#     ("Bananas", "Stawberries", "Peaches"),
#     index=None,
#     placeholder="Select fruit...",
# )

# st.write("Your favorite fruit is:", option)


name_on_order=st.text_input('Name on Smoothie')
st.write('The name on your smaoothie will be: ', name_on_order )

# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list=st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe,
    max_selections=5
)


if ingredient_list:
    # st.write(ingredient_list)
    # st.text(ingredient_list)
    ingredients_string=''

    for x in ingredient_list:
        ingredients_string += x + ' '

    # st.write(ingredients_string)

my_insert_stmt="""insert into smoothies.public.orders(ingredients, name_on_order)
values('""" + ingredients_string + """', '""" + name_on_order + """')"""
# st.write(my_insert_stmt)

time_to_insert=st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
