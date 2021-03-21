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

total= 0
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
    total= pet_price+vet_price+food_price+rest_price
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
    total= int(total)
    st.header(f'You will be charged {total} SAR.')
    
price1= 0
price1= st.number_input('Enter your price : ')
total2= st.number_input('Enter our price : ', key= 'jkl')
if price1<(total2*0.9):
  st.text('Quoted price is too low.')
  st.subheader('Order is cancelled.')
else:
  st.header(f'You will be charged {price1} SAR.')
  st.text('We are agreed on the quoted price.')
  st.subheader('Proceed with order.')   


st.title('House Relocation Price Calculator')
total1= 0

st.subheader('Choose house specifications.')
col11, col12= st.beta_columns(2)

bedrooms= col11.slider('Enter number of bedrooms : ', 0, 30, 1)
col11.text('Relocation cost per bedroom: \n120(no assembly), 200(with assembly)')
if col11.checkbox('I need assembly.', key= '1'):
  temp= bedrooms*200
  col11.text(f'This will cost {temp} SAR.')
else:
  temp= bedrooms*120
  col11.text(f'This will cost {temp} SAR.')
total1= total1+temp

kidrooms= col11.slider('Enter number of kids\' rooms : ', 0, 30, 1)
col11.text('Relocation cost per kids\' room: \n100(no assembly), 150(with assembly)')
if col11.checkbox('I need assembly.', key= '2'):
  temp= kidrooms*150
  col11.text(f'This will cost {temp} SAR.')
else:
  temp= kidrooms*100
  col11.text(f'This will cost {temp} SAR.')
total1= total1+temp

livrooms= col12.slider('Enter number of living rooms : ', 0, 30, 1)
col12.text('Relocation cost per living room: \n140(no assembly), 250(with assembly)')
if col12.checkbox('I need assembly.', key= '3'):
  temp= livrooms*250
  col12.text(f'This will cost {temp} SAR.')
else:
  temp= livrooms*140
  col12.text(f'This will cost {temp} SAR.')
total1= total1+temp

kitchens= col12.slider('Enter number of kitchens : ', 0, 30, 1)
col12.text('Relocation cost per kitchen: \n120(no assembly), 500(with assembly)')
if col12.checkbox('I need assembly.', key= '4'):
  temp= kitchens*500
  col12.text(f'This will cost {temp} SAR.')
else:
  temp= kitchens*120
  col12.text(f'This will cost {temp} SAR.')
total1= total1+temp

col11.subheader('Enter furnishing details.')
col12.subheader('\n')

acs= col11.slider('Enter number of A/C windows : ', 0, 30, 1)
temp= acs*130
col11.text(f'This will cost {temp} SAR.')
total1= total1+temp

evs= col11.slider('Enter number of elevators : ', 0, 30, 1)
temp=evs*100
col11.text(f'This will cost {temp} SAR.')
total1= total1+temp

fls= col12.slider("Enter number of floors : ", 0, 30, 1)
temp=fls*50
col12.text(f'This will cost {temp} SAR.')
total1= total1+temp

col13, col14= st.beta_columns(2)
rooms= bedrooms+kidrooms+livrooms+kitchens

if col13.checkbox('I need blanket wrapping.'):
  col13.text('This costs additional 30 SAR per room.')
  total1= total1+(rooms*30)
if col13.checkbox('I need carpenters.'):
  col13.text('This costs additional 30 SAR per room.')
  total1= total1+(rooms*30)
if col13.checkbox('I need cleaning at drop off location.'):
  col13.text('This costs additional 40 SAR per room.')
  total1= total1+(rooms*40)
if col13.checkbox('I need cleaning at pick up location.'):
  col13.text('This costs additional 30 SAR per room.')
  total1= total1+(rooms*30)
if col14.checkbox('I need people for lifting & handling.'):
  col14.text('This costs additional 30 SAR per room.')
  total1= total1+(rooms*30)
if col14.checkbox('I need packing boxes.'):
  col14.text('This costs additional 30 SAR per room.')
  total1= total1+(rooms*30)
if col14.checkbox('I need packaging for items.'):
  col14.text('This costs additional 30 SAR per room.')
  total1= total1+(rooms*30)
if col14.checkbox('I have fragile items.'):
  col14.text('This costs additional 150 SAR.')
  total1= 150

col15, col16= st.beta_columns(2)
time11= col15.time_input('Order time : ', key= '123')
date11= col15.date_input('Order date : ', key= '1233')
place11= col15.text_input('Order location : ', key= '1234')
time12= col16.time_input('Pickup time : ', key= '1236')
date12= col16.date_input('Pickup date : ', key= '1237')
days= (date12-date11).days
place12= col16.text_input('Pickup location : ', key= '1238')

if st.button('Calculate charges : ', key='button2') :
  loc11= geolocator.geocode(place11)
  loc12= geolocator.geocode(place12)
  lat_lon11= (loc11.latitude, loc11.longitude)
  lat_lon12= (loc12.latitude, loc12.longitude)
  distt1= geodesic(lat_lon11, lat_lon12).kilometers
  st.text(f'Distance between delivery & pickup location : {round(distt1, 2)} kms.')
  if distt1==0:
    total1= 0
  else:
    total1= total1+(distt1*1.7)
  total1= round(total1, 2)
  st.subheader(f'Total relocation cost : {total1} SAR.')

price11= st.number_input('Enter your price : ', key= '567')
total22= st.number_input('Enter our price : ', key= 'jkl')
if price11<(total22*0.9):
  st.text('Quoted price is too low.')
  st.button('Order is cancelled.', key= 'ert')
else:
  st.header(f'You will be charged {price11} SAR.')
  st.text('We are agreed on the quoted price.')
  st.button('Proceed with order.', key= 'tyu')   

