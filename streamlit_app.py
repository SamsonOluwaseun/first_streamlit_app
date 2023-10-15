import streamlit
import requests
import pandas
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Dinner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Bluberry Oatmeal')
streamlit.text('🥗 Kale, Spinash & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index('Fruit')
# streamlit.dataframe(my_fruit_list) -- Shows the dataframe
# Let's put a picklist here so they can pick the fruit they want to include
fruits_selected= streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
#Filter data to show only what is selected
fruits_to_show = my_fruit_list.loc[fruits_selected]
#Display table on the page
streamlit.dataframe(fruits_to_show)
    
# Create the repeatable codeblock (called a function)
def get_fruityvice_data(this_fruit_choice):
    # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ this_fruit_choice)
    # take the json version of the response and normalize it
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

#New section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
      #fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
      fruit_choice = streamlit.text_input('What fruit would you like information about?')
      if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
      else:
          back_from_function = get_fruityvice_data(fruit_choice)
            # output on the screen as a table
          streamlit.dataframe(back_from_function)  #
except URLError as e:
      streamlit.error()
    
streamlit.header("The fruit load list contains:")
#Snowflakes related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()
        
#Add a botton to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]) #Getting value from the secret file in stramlit
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

    
streamlit.stop()

streamlit.write('The user entered ', fruit_choice)

#import request
#streamlit.text(fruityvice_response.json()) #Just write data on the screen

#Connecting to snowflakes
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")

#my_data_row = my_cur.fetchone()

#streamlit.text("Hello from Snowflake:")
streamlit.header("The fruit load list contains:")


#Allow end users to add fruits
add_my_fruit = streamlit.text_input('What fruit would you like add?')
streamlit.write('Thank you for adding  ', add_my_fruit)

my_cur.execute("insert into fruit_load_list values ('from stramlit')")





















