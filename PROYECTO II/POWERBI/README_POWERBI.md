1. **Problem Definition**: 
- Project for predictive modeling of housing prices in Barcelona
- Project goal is to **improve the accuracy of the predictive model and provide interactive visualizations**
- Data Science project will be developed following the Data Science Life Cycle (DSLC) framework, exploring and concluding about POWERBI tool apabilities, advantages and limitations to support a data science project
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

2. **Data Collection**: 
- PowerBI allows direct connectivity to multiple data sources including databases, web services, files, and cloud platforms
- Power Query Editor for data transformation, cleaning, and reshaping
- Noted Power Query first and automatic data transformation was "Changed Type" and this transformation might lead to issues
- On this data set with only 9 columns is simple to check all data types, and was found  decimal numbers as whole numbers and booleans as text.
- Used built-in data profiling tools to identify quality issues



Advantages:

User-friendly interface for complex data transformations without coding
Incremental refresh capabilities to efficiently update large datasets
Standardized data connectors that handle authentication and schema changes
Strong integration with Microsoft ecosystem, especially Excel and Azure

Limitations:

Limited support for unstructured data like images or audio
Data transformation capabilities less robust than specialized ETL tools
Memory constraints when handling very large datasets
Less suitable for real-time streaming data compared to dedicated solutions


3. **Data Preparation**: Cleaning, preprocessing, and organizing the data. This includes handling missing values, outliers, data transformations, and feature engineering.

4. **Exploratory Data Analysis (EDA)**: Analyzing the data to understand patterns, relationships, and potential anomalies. This step often involves data visualization and statistical analysis to generate insights.

5. **Modeling**: Selecting and applying appropriate machine learning or statistical models. This step includes training, validating, and fine-tuning models to optimize their performance.

6. **Evaluation**: Assessing the model's performance using metrics such as accuracy, precision, recall, or others relevant to the project. Ensuring the model meets the required standards for deployment.

7. **Deployment**: Implementing the model in a production environment, making it accessible for real-world use. This might involve integrating the model with existing systems or deploying it via APIs or cloud platforms.

8. **Monitoring and Maintenance**: Continuously monitoring the model's performance in production to ensure its accuracy and relevance over time. This stage may also involve retraining the model as new data becomes available.

9. **Communication and Reporting**: Presenting findings and results to stakeholders in a clear and actionable manner, often through dashboards, visualizations, or reports.
