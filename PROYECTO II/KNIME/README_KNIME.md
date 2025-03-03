# 1. **Problem Definition**: 
- Project for predictive modeling of housing prices in Barcelona
- Project goal is to **improve the accuracy of the predictive model and provide interactive visualizations**
- Data Science project will be developed following the Data Science Life Cycle (DSLC) framework
exploring and concluding about KNIME tool apabilities, advantages and limitations to support a data science project
- As the problem aims to predict housing prices in Barcelona, a brief complementary information about property types (as named in data) is included as reference.
    - **Study (Estudio)**: Typically the smallest type of dwelling, a studio is a single open space that combines the living area, bedroom, and kitchen, with a separate bathroom. These are ideal for individuals or couples seeking a compact living space.
    - **Attic (Ático)**: An attic refers to a top-floor apartment, often featuring sloped ceilings and sometimes including a terrace. The size can vary, but attics are generally larger than studios and may offer unique architectural features.
    - **Apartment (Apartamento)**: In Spain, the term "apartamento" usually denotes a modest-sized dwelling, typically with one or two bedrooms. These are suitable for small families or individuals desiring separate living and sleeping areas.
    - **Flat (Piso)**: The term "piso" is commonly used to describe larger residential units, often with multiple bedrooms and ample living space. Flats are prevalent in urban areas and cater to families or individuals seeking more spacious accommodations.
- Data Description
    - **price**: The price of the real-state.
    - **rooms**: Number of rooms.
    - **bathroom**: Number of bathrooms.
    - **lift**: whether a building has an elevator (also known as a lift in some regions) or not
    - **terrace**: If it has a terrace or not.
    - **square_meters**: Number of square meters.
    - **real_state**: Kind of real-state.
    - **neighborhood**: Neighborhood
    - **square_meters_price**: Price of the square meter

# 2. **Data Collection**: 
- Dataset provided by the academy
- Notes with format (Knime Node Name)_(Node Description)
- (CSV Reader)_(LOAD ORIGINAL DATA) for data load
    - Target variable for modeling is "price"
    - There are 16376 rows and 10 columns. 
    - Data types are aligned with information, except variables 'rooms' and 'bathroom' being "D" (Double) and expected "I" (integer)

# 3. **Data Preparation**: 
### **Data Overview**
- (Statistics View_(describe) for data overview of numerical variables
    - The variable 'Unnamed' represent index and should be deleted from data
    - The variables 'Unnamed: 0', 'square_meters_price', 'square_meters', 'rooms' and 'bathroom' generates a warning by having over 1000 unique values
    - There are missing data on multiple variables
    - Units size goes from 10m2 to 679m2, with a mean of 84.36m2
    - Units prices goes from 320EUR to 15000EUR/month, with mean of 1437EUR/month
    - price range is assumed referred to monthly rent, so considered as EUR per month
    - Units prices by square meter goes from 4.549EUR/m2/month to 197.272EUR/m2/month, with mean of 17.73EUR/m2/month
    - There are units listed with cero rooms and 10.754 rooms
    - There are units with 0.9 bathroom
    - There are four types of real states being the most common "flat"
    - Most units do not have terrace
    - Most units do have lift
    - The neighborhood with largest unit count is "Eixample"
    - The variable 'rooms' will require feature engineering
    - The variable 'bathroom' will require feature engineering

### **Missing Value handling**
- 389 out of 408 missing "square_meters" values are imputed considering relation "price" / "square_meters_price"
    - (Row Filter)_(389/408) to filter square_meters nulls to be imputed
    - 

### **Feature engineering**

### **Outliers detection and treatment**

### **Data Management**

# 4. **Exploratory Data Analysis (EDA)**:

# 5. **Modeling**:

# 6. **Evaluation**:

# 7. **Deployment**:

# 8. **Monitoring and Maintenance**:

# 9. **Communication and Reporting**:




