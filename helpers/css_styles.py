
addon_header_css = """
    <style>    

    .stApp header::before {
        content: "Dataset Configs";
        display: block;
        color: white;
        # display: flex; 
        background-color: black;
        text-align: center;
        # padding: 20px;
        font-size: 30px;
        font-weight: bold;
    }
    .stApp > header {
        # display: flex;  /* Make header a flex container */
        align-items: center;  /* Align logo and title vertically */
        padding: 10px 20px;  /* Add some padding */
        background-color: black;  /* Optional background color */
    }

    .stApp > header > img {
        height: 50px;  /* Adjust logo height */
        margin-right: 10px;  /* Add margin between logo and title */
    }
    </style>
    """

app_styling_css = """
    <style>
    header {
    background: url(BlackRock-logo.jpg) no-repeat center;
    background-size: cover;
    height: 10px;
    padding: 10px;
    text-align: center;
    color: white;
    font-size: 24px;
    }  
    </style>
    <style>
    .main .block-container {
        max-width: 1300px; /* Max width for the main container */
        padding: 2rem;
        background-color: #EEEEEE;
    }
    </style>
    <style>
    .stButton>button {
        background-color: #6495ED;
        color: white;
        border-radius: 5px;
    }    
    </style>
    <style>
    .stApp {
            background-color: #EEEEEE;
        }
    </style>
   <style>
    .stSelectbox select, .stTextInput input, .stCheckbox input, .stNumberInput input, .stDateInput input {
        background-color: white !important;
        color: black !important;
    }
    </style>
    <style>
    [data-testid="stSidebar"]{
        background-color: white; /* Set dark black background for the logo area */
        padding: 5px; /* Optional: Adjust padding for better alignment */
        border-radius: 5px; /* Optional: Rounded edges for aesthetics */
        height: 100%;
    }
    </style>
    <style>
    [data-testid="stSidebarNav"] a {
        # height: 100%; /* Ensure it spans the full vertical height */
        padding-top: 10px; /* Optional: Add spacing at the top */
        padding-bottom: 10px; /* Optional: Add spacing at the bottom */
        color: white;
        font-weight: bold;
        font-size: 18px; /* Increase font size */
        background-color: white;
        padding: 5px; /* Optional: Adjust padding for better alignment */
        border-radius: 5px; /* Optional: Rounded corners */
    }

    </style>
"""
# Custom CSS for full arrowhead titles
arrowhead_css = """
       <style>
       /* Full arrowhead style */
       .arrowhead {
           display: inline-block;
           padding: 10px;
           font-size: 16px;
           color: white;
           background-color: #4CAF50;
           clip-path: polygon(0% 0%, 90% 0%, 100% 50%, 90% 100%, 0% 100%);
           margin-right: 10px;
           width: 220px;
           text-align: center;
           cursor: pointer;
       }

       /* Highlighted arrowhead for active page */
       .highlight {
           background-color: #FF6347;
           clip-path: polygon(0% 0%, 90% 0%, 100% 50%, 90% 100%, 0% 100%);
       }

       /* Flexbox container to align the arrows */
       .arrow-container {
           display: flex;
           align-items: center;
           justify-content: center;
           margin-bottom: 30px;
       }
       </style>
   """