import streamlit as st
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
geolocator = Nominatim(user_agent="price_calc")
st.set_page_config(page_title= 'Pet Delivery price calculation project', initial_sidebar_state = 'auto')
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# calculation equation
# base weight price is 50$ for 10 kgs, thereafter price increases by 1$ per kg
# transportation insurance is 0.5*weight price
# transportation charge is 10$ per mile
# International order is 1.5*in-kingdom order
# same-day delivery gets charged 150%, 1 day delivery 125%, 2 day or more delivery 100% 

st.title('Price Calculator')
total= 0

st.subheader('Choose pet requirements.')
col1, col2= st.beta_columns(2)
pet_prices= {'Dog': 59, 'Horse': 450, 'Cat': 0, 'Reptile': 50, 'Bird': 50, 'Eagle': 500, 'Wild Animal': 1000, 'Other': 100}
pet_type= col1.radio('Enter type of pet :', ('Dog', 'Horse', 'Cat', 'Reptile', 'Bird', 'Eagle', 'Wild Animal', 'Other'))
pet_price= pet_prices[pet_type]
col1.text(f'This will cost you additional {pet_price} SAR.')

wt_price= 50
weight= col2.slider('Enter weight of pet: ', 1, 1000, 5)
if weight>10:
  wt_price= 50+(weight-10)
col2.text(f'This will cost you additional {wt_price} SAR.')

vet_price= 0
if col2.checkbox('I need a vet assessment.'):
  vet_price= 150
col2.text(f'This will cost you additional {vet_price} SAR.')

food_price= 0
if col2.checkbox('I need food for my pet in transit.'):
  food_price= 20
col2.text(f'This will cost you additional {food_price} SAR.')

rest_price= 0
if col2.checkbox('I need rest breaks for my pet in transit.'):
  rest_price= 100
col2.text(f'This will cost you additional {rest_price} SAR.')

st.subheader('Choose transit specifications.')
st.write()
col3, col4= st.beta_columns(2)
travel_type = col3.selectbox('What is your order type?', ('In kingdom', 'Out of kingdom'))
col3.text('Out of kingdom travel will cost you 150% of the above price.')
int_doc= 0
int_crt= 0
ins_chg= 0
if travel_type=='Out of kingdom':
  if col4.checkbox('I need documentation services for international transport.'):
    int_doc= 700
  col4.text(f'This will cost you additional {int_doc} SAR.')
  if col4.checkbox('I need pet travel crate for international transport.'):
    int_crt= 200
  col4.text(f'This will cost you additional {int_crt} SAR.')
  if col4.checkbox('I need insurance for international transport.'):
    ins_chg= 500
  col4.text(f'This will cost you additional {ins_chg} SAR.')

if travel_type=='In kingdom':  
  if col4.checkbox('I need pet travel crate for local transport.'):
    int_crt= 45
  col4.text(f'This will cost you additional {int_crt} SAR.')
  if col4.checkbox('I need insurance for domestic transport.'):
    ins_chg= 100
  col4.text(f'This will cost you additional {ins_chg} SAR.')

st.subheader('Provide pickup & delivery instructions.')
st.text('Same day, second day & third day or more pickup costs 120%, 110% & 100% of the above price respectively.')

col5, col6= st.beta_columns(2)
time1= col5.time_input('Order time : ')
date1= col5.date_input('Order date : ')
place1= col5.text_input('Order location : ')
time2= col6.time_input('Pickup time : ')
date2= col6.date_input('Pickup date : ')
days= (date2-date1).days
place2= col6.text_input('Pickup location : ')

if st.button('Calculate charges : ') :
  loc1= geolocator.geocode(place1)
  loc2= geolocator.geocode(place2)
  lat_lon1= (loc1.latitude, loc1.longitude)
  lat_lon2= (loc2.latitude, loc2.longitude)
  distt= geodesic(lat_lon1, lat_lon2).kilometers
  st.text(f'Distance between delivery & pickup location : {round(distt, 2)} kms.')
  if distt==0:
    total= 0
  else:
    trans_charge= distt*0.35
    # sec1 price
    total= pet_price+wt_price+vet_price+food_price+rest_price
    # sec2 price
    total= total+int_doc+int_crt+ins_chg
    # sec3 price
    # calculate for same-day or second-day or third-day delivery
    if days==0:
      st.text('You chose same day pickup. This will cost you 120% of the above price.')
      total= total+(trans_charge*1.2)
    if days==1:
      st.text('You chose second day pickup. This will cost you 110% of the above price.')
      total= total+(trans_charge*1.1)
    if days>1:
      total= total+trans_charge
    # calculate for in kingdom or out of kingdom
    if travel_type=='Out of kingdom':
      total= total*1.5
    total= round(total, 2)
  st.header(f'You will be charged {total} SAR.')
  


