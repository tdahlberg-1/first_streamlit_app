import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title ('My Parents New Healthy Diner')
streamlit.header ('Breakfast Menu')
streamlit.text ('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text ('🥗Kale , Spinach & Rocket Smoothie')
streamlit.text ('🐔Hard-Boiled Free-Range Egg')
streamlit.text ('🥑🍞Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error ("Please select a fruit to get more information")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
            
except URLError as e:
    streamlit.error()
    
    
    streamlit.error ("Please select a fruit to get information.")
streamlit.write('The user entered ', fruit_choice)

#import snowflake.connector
streamlit.header("The Fruit List Contains:")
#Snowflake-related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from pc_rivery_db.public.fruit_load_list") #remove if above is used
        return  my_cur.fetchall()
    
#add a buttom to load the fruit
if streamlit.button ('Get Fruit Load List'):
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

#allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('from streamlit')")
        return "thanks for adding" + new_fruit
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('add fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)
    
    
    #dont run anything past here while we troubleshoot
streamlit.stop
fruit_choice = streamlit.text_input('What fruit would you like to add?','jackfruit')


my_cur.execute ("insert into fruit_load_list values ('from streamlit')")
