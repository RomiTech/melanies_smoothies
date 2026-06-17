# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
# Adding in the Table Select
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Get Your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!""")

name_on_order = st.text_input("Name on Smoothie:")
st.write('the name on your smoothie will be:', name_on_order)

session = get_active_session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

#No need to show the whole table anymore.
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
    )

#look at the contents of the datatype:LIST in {ingredients_list}
#add logic to NOT dispay the contents if nothing is selected.

#by Saying : IF ingredients_list:  It is implying IF {object} <> FALSE.
#as long as ingredients_list has SOMETHING in it, it is not NULL and thus not false.

if ingredients_list:
    ingredients_string = ''

    # "fruit_chosen" has not been defined yet.  But Python knows it is some
    # sort of place holder for a Counter of items in a list based on context.
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # st.write(ingredients_string)

    #Now a SQL statement will write the selected fruits to the ORDER table that was made before.
    
    my_insert_stmt = """ insert into SMOOTHIES.PUBLIC.ORDERS(INGREDIENTS,name_on_order)
                    values ('""" + ingredients_string + """','""" + name_on_order +  """')"""

    #this was failing until these grants were made in SQL. 
    #Apperently one of the levels of the Database, Schema, Table
    #did not have permissions....
    
    #GRANT USAGE ON DATABASE SMOOTHIES TO ROLE PUBLIC;
    #GRANT USAGE ON SCHEMA SMOOTHIES.PUBLIC TO ROLE PUBLIC;
    #GRANT SELECT, INSERT ON TABLE SMOOTHIES.PUBLIC.ORDERS TO ROLE PUBLIC;
    
    st.write(my_insert_stmt)

    #adding a SUBMIT button
    
    time_to_insert = st.button("Submit Order")
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered!', icon="✅")
        
