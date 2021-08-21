import streamlit            as st
import pandas               as pd

from PIL import Image


# =================================================
# ================== PAGE SET UP ==================
# =================================================

# === page titles
st.set_page_config(page_title="Rossmann Sales Predictions", page_icon="https://img.icons8.com/ios/250/000000/total-sales-1.png",
                   layout="wide")


st.markdown('*Additional information about House Rocket and this streamlit creator are by the end of this page.*')
st.write('')

# image
photo = Image.open('rossmann.png')
st.image(photo, width=500)

# headers
welcome_format = '<p style="font-family:sans-serif;' \
                       'color:#e01c3c;' \
                       'font-size: 40px;' \
                       'font-style: italic;' \
                       'text-align: left;' \
                       '">Welcome to Rossmann Sales Predictions</p>'
st.markdown(welcome_format, unsafe_allow_html=True)

# =================================================
# =============== HELPER FUNCTIONS ================
# =================================================

@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)
    data = data.head(1300) # filter data to edit faster

    # data.style.format(formatter={('buying_price', 'median_price_zipcode',
    #                               'selling_price_suggestion', 'expected_profit'): '{:,.2f}'})

    return data

def set_features(data):
    # create columns as needed

    return data

def data_information(data):
    st.header("**Stores General Information**")
    exp_data = st.beta_expander("Click here to expand and see the dataset general information", expanded=False)
    with exp_data:
        st.subheader("Data Dimensions")
        st.write("Number of Sales:", data.shape[0])
        st.write("Number of Stores:", data['store'].unique().shape[0])

        st.subheader("Time Interval")
        st.write("", data['date'].min())
        st.write("", data['date'].max())

    exp_data.write("")
    exp_data.write("*End of data overview*")

    return None

def sales_prediction(data):
    st.header("**Sales Predictions**")
    exp_data = st.beta_expander("Click here to expand and see the dataset general information", expanded=False)
    with exp_data:
        st.subheader("Predictions")

        # creating filters
        f_store = st.multiselect('Type or select the store code',
                                 data['store'].sort_values(ascending=True).unique())

        # filtering data
        if f_store!=[]:
            f_data = data.loc[data['store'].isin(f_store),:]
        else:
            f_data = data.copy()

        st.dataframe(f_data)
        st.write('')
        st.write('**Number of selected stores:', '{:,}**'.format(f_data['store'].unique().shape[0]))
        st.write('**Sum of expected sales for subset above:', 'US$ {:,.2f}**'.format(f_data['sales'].sum()))

    exp_data.write("")
    exp_data.write("*End of sales predictions*")

    return None

# =================================================
# ================ MAIN FUNCTION ==================
# =================================================

if __name__ == '__main__':
    # ====== DATA EXTRACTION
    data = get_data('sales_prediction_fulldata.csv')

    # geofile_raw = get_geofile('https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson')

    set_features(data)

    data_information(data)

    sales_prediction(data)


st.markdown('---')
st.markdown('---')

st.title('Additional Information')

st.header("Report Purpose:")

st.write('Rossmann is a drugstore chain... model consists of purchasing and reselling properties through a digital platform.')
st.write("This report was created by a request from Rossmann's CEO to visualize stores sales predictions "
         "for the next 6 weeks to preview the amount it can be invested on stores reformations.")

st.write('')
st.markdown('This data visualization is part of **Sales Predictions Project** made by **Mariana Borges**.')
st.markdown('You can read the business context and check the code for this streamlit on [github](https://github.com/marianaborgal/P002_Sales_Predictions_Drugstore).')
st.markdown('Other Projects: [Portfolio](https://github.com/marianaborgal)')
st.markdown('Contact me: [LinkedIn](https://www.linkedin.com/in/marianaborgal/)')
