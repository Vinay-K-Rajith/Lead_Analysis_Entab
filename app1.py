import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import random
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="ENTAB - Lead Scoring System",
    page_icon="🎓",
    layout="wide"
)

# Title and description
st.title("🎓 ENTAB - Student Lead Scoring System")
st.markdown("### Intelligent Student Enrollment Prediction & Analysis")
st.markdown("---")


def generate_sample_data(num_students=100):
    """Generate realistic sample data for demonstration"""

    # Sample student names
    first_names = [
        "Aarav", "Aditi", "Arjun", "Ananya", "Ishaan", "Kavya", "Rohan", "Priya",
        "Vivaan", "Diya", "Aditya", "Siya", "Karan", "Riya", "Vihaan", "Asha",
        "Aryan", "Meera", "Reyansh", "Tara", "Ayaan", "Neha", "Rudra", "Pooja",
        "Shivansh", "Shreya", "Arnav", "Khushi", "Kabir", "Nisha", "Devansh", "Ritika",
        "Atharv", "Sakshi", "Hriday", "Bhavya", "Advait", "Tanvi", "Pranav", "Simran",
        "Samarth", "Avni", "Parth", "Janvi", "Dhruv", "Kiara", "Vedant", "Myra",
        "Anirudh", "Anika", "Shaurya", "Palak", "Krish", "Dia", "Yash", "Ira",
        "Harsh", "Zara", "Nikhil", "Manya", "Raghav", "Mahika", "Siddharth", "Sejal"
    ]

    last_names = [
        "Sharma", "Gupta", "Singh", "Kumar", "Patel", "Shah", "Agarwal", "Bansal",
        "Jain", "Mittal", "Agrawal", "Chopra", "Malhotra", "Arora", "Kapoor", "Mehta",
        "Verma", "Pandey", "Saxena", "Goyal", "Sinha", "Yadav", "Mishra", "Tiwari",
        "Bhardwaj", "Kashyap", "Srivastava", "Chandra", "Bhatia", "Khanna", "Tandon", "Sethi"
    ]

    # Sample previous schools
    previous_schools = [
        "Delhi Public School", "Kendriya Vidyalaya", "Ryan International", "DAV Public School",
        "St. Mary's Convent", "Holy Child School", "Modern School", "Bal Bharati Public School",
        "Cambridge School", "Springdales School", "Amity International", "Gyan Bharati School",
        "Little Angels School", "St. Xavier's School", "Mount Carmel School", "Sacred Heart School",
        "Bharatiya Vidya Bhavan", "Lotus Valley School", "Heritage School", "Birla Public School"
    ]

    # Sample locations (with varying distances from school)
    locations = [
        ("Connaught Place", 95), ("Karol Bagh", 85), ("Lajpat Nagar", 80), ("Rajouri Garden", 75),
        ("Dwarka", 70), ("Rohini", 65), ("Janakpuri", 80), ("Vasant Kunj", 85), ("Saket", 90),
        ("Greater Kailash", 95), ("Nehru Place", 85), ("Tilak Nagar", 70), ("Pitampura", 60),
        ("Preet Vihar", 75), ("Mayur Vihar", 70), ("Ashok Vihar", 65), ("Model Town", 80),
        ("Civil Lines", 85), ("Khan Market", 95), ("Defence Colony", 90), ("Laxmi Nagar", 60),
        ("Shahdara", 50), ("Uttam Nagar", 55), ("Najafgarh", 45), ("Narela", 40)
    ]

    # How they know us options
    know_us_sources = [
        ("School Website", 60), ("Google Search", 65), ("Social Media", 70), ("Friend Referral", 85),
        ("Newspaper Ad", 50), ("Hoarding/Banner", 45), ("Educational Fair", 75), ("Alumni Referral", 90),
        ("Current Parent Referral", 95), ("Teacher Referral", 88), ("Brochure", 55), ("Walk-in", 40)
    ]

    # Classes available
    classes = [
        ("Nursery", 70), ("LKG", 75), ("UKG", 80), ("Class 1", 85), ("Class 2", 80),
        ("Class 3", 75), ("Class 4", 70), ("Class 5", 65), ("Class 6", 85), ("Class 7", 80),
        ("Class 8", 75), ("Class 9", 90), ("Class 10", 85), ("Class 11", 95), ("Class 12", 90)
    ]

    data = []

    for i in range(num_students):
        # Generate student name
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        student_name = f"{first_name} {last_name}"

        # Location
        location, location_score = random.choice(locations)
        location_score += random.randint(-10, 10)
        location_score = max(0, min(100, location_score))

        # How they know us
        source, know_score = random.choice(know_us_sources)
        know_score += random.randint(-5, 15)
        know_score = max(0, min(100, know_score))

        # Sibling in school (30% chance)
        has_sibling = random.random() < 0.3
        sibling_score = 100 if has_sibling else random.randint(0, 20)

        # Previous school
        prev_school = random.choice(previous_schools)
        if "DPS" in prev_school or "St." in prev_school or "Modern" in prev_school:
            prev_school_score = random.randint(80, 95)
        elif "Ryan" in prev_school or "DAV" in prev_school or "Amity" in prev_school:
            prev_school_score = random.randint(70, 85)
        else:
            prev_school_score = random.randint(50, 75)

        # Class applied for
        class_name, class_score = random.choice(classes)
        class_score += random.randint(-5, 10)
        class_score = max(0, min(100, class_score))

        # Last class percentage
        if class_name in ["Nursery", "LKG", "UKG"]:
            percentage_score = random.randint(70, 100)
        else:
            percentage = random.randint(65, 98)
            if percentage >= 90:
                percentage_score = 95
            elif percentage >= 80:
                percentage_score = 80
            elif percentage >= 70:
                percentage_score = 65
            else:
                percentage_score = 40

        # Contact variations
        email_different = random.random() < 0.2
        email_score = 0 if not email_different else random.randint(60, 100)

        whatsapp_different = random.random() < 0.25
        whatsapp_score = 0 if not whatsapp_different else random.randint(50, 100)

        # Generate contact info
        email = f"{first_name.lower()}.{last_name.lower()}@{'gmail.com' if random.random() < 0.7 else random.choice(['yahoo.com', 'hotmail.com', 'outlook.com'])}"
        phone = f"+91-{random.randint(7000000000, 9999999999)}"

        data.append({
            'student_name': student_name,
            'email': email,
            'phone': phone,
            'location': location,
            'location_score': location_score,
            'how_you_know_us': source,
            'how_you_know_us_score': know_score,
            'has_sibling_in_school': "Yes" if has_sibling else "No",
            'sibling_in_school_score': sibling_score,
            'previous_school_name': prev_school,
            'previous_school_name_score': prev_school_score,
            'class_applied_for': class_name,
            'class_applied_for_score': class_score,
            'last_class_percentage': f"{random.randint(65, 98)}%" if class_name not in ["Nursery", "LKG",
                                                                                        "UKG"] else "N/A",
            'last_class_percentage_score': percentage_score,
            'communication_email_different': "Yes" if email_different else "No",
            'communication_email_different_score': email_score,
            'whatsapp_number_different': "Yes" if whatsapp_different else "No",
            'whatsapp_number_different_score': whatsapp_score,
            'application_date': (datetime.now() - timedelta(days=random.randint(1, 60))).strftime("%Y-%m-%d")
        })

    return pd.DataFrame(data)


def calculate_lead_score(location_score, how_you_know_us_score, sibling_in_school_score,
                         previous_school_name_score, class_applied_for_score,
                         last_class_percentage_score, communication_email_different_score,
                         whatsapp_number_different_score):
    """Calculate lead score using weighted formula"""

    weights = [0.85, 0.70, 0.95, 0.55, 0.50, 0.25, 0.25, 0.20]
    scores = [location_score, how_you_know_us_score, sibling_in_school_score,
              previous_school_name_score, class_applied_for_score,
              last_class_percentage_score, communication_email_different_score,
              whatsapp_number_different_score]

    weighted_sum = sum(score * weight for score, weight in zip(scores, weights))
    total_weights = sum(weights)

    lead_score = (weighted_sum / total_weights)
    return round(lead_score, 2) + 5


def categorize_lead(score):
    """Categorize leads based on score"""
    if score >= 80:
        return "🔥 Hot Lead"
    elif score >= 60:
        return "🟡 Warm Lead"
    else:
        return "❄️ Cold Lead"


def get_lead_color(category):
    """Get color for lead category"""
    colors = {
        "🔥 Hot Lead": "#FF4B4B",
        "🟡 Warm Lead": "#FFA500",
        "❄️ Cold Lead": "#4B8BFF"
    }
    return colors.get(category, "#808080")


# Generate sample data
if 'sample_data' not in st.session_state:
    st.session_state.sample_data = generate_sample_data(150)

# Main tabs
tab1, tab2, tab3 = st.tabs(["🎯 Individual Scoring", "📊 Sample Data Analysis", "📁 Upload CSV"])

with tab1:
    st.header("Individual Student Lead Scoring")
    st.markdown("*Enter student information to get instant lead score*")

    # Student basic info
    col1, col2 = st.columns(2)
    with col1:
        student_name = st.text_input("Student Name", placeholder="e.g., Aarav Sharma")
        student_email = st.text_input("Email", placeholder="e.g., aarav.sharma@gmail.com")
    with col2:
        student_phone = st.text_input("Phone", placeholder="e.g., +91-9876543210")
        application_date = st.date_input("Application Date", datetime.now())

    st.markdown("---")

    # Scoring parameters
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📍 Location & Background")

        location_options = {
            "Very Close (< 2 km)": 95,
            "Close (2-5 km)": 85,
            "Moderate (5-10 km)": 70,
            "Far (10-15 km)": 50,
            "Very Far (> 15 km)": 30
        }
        location_choice = st.selectbox("Distance from School", list(location_options.keys()))
        location_score = location_options[location_choice]

        know_us_options = {
            "Current Parent Referral": 95,
            "Alumni Referral": 90,
            "Teacher Referral": 88,
            "Friend/Family Referral": 85,
            "Educational Fair": 75,
            "Social Media": 70,
            "Google Search": 65,
            "School Website": 60,
            "Brochure/Pamphlet": 55,
            "Newspaper Ad": 50,
            "Hoarding/Banner": 45,
            "Walk-in": 40
        }
        know_us_choice = st.selectbox("How did you know about us?", list(know_us_options.keys()))
        how_you_know_us_score = know_us_options[know_us_choice]

        sibling_options = {
            "Yes - Currently studying": 100,
            "Yes - Alumni": 80,
            "No": 0
        }
        sibling_choice = st.selectbox("Sibling in School?", list(sibling_options.keys()))
        sibling_in_school_score = sibling_options[sibling_choice]

    with col2:
        st.subheader("🎓 Academic Information")

        school_options = {
            "Top Tier (DPS, Modern, St. Xavier's)": 90,
            "High Quality (Ryan, DAV, Amity)": 75,
            "Good (Local Reputed Schools)": 60,
            "Average (Local Schools)": 45,
            "Below Average": 30
        }
        school_choice = st.selectbox("Previous School Category", list(school_options.keys()))
        previous_school_name_score = school_options[school_choice]

        class_options = {
            "Class 11 (Science/Commerce)": 95,
            "Class 9": 90,
            "Class 6": 85,
            "Class 1": 85,
            "UKG": 80,
            "LKG": 75,
            "Nursery": 70,
            "Other Classes": 70
        }
        class_choice = st.selectbox("Class Applied For", list(class_options.keys()))
        class_applied_for_score = class_options[class_choice]

        percentage_options = {
            "90% and above": 95,
            "80-89%": 80,
            "70-79%": 65,
            "60-69%": 50,
            "Below 60%": 30,
            "Not Applicable (Early Classes)": 75
        }
        percentage_choice = st.selectbox("Last Class Performance", list(percentage_options.keys()))
        last_class_percentage_score = percentage_options[percentage_choice]

    # Additional information
    st.subheader("📞 Contact Information")
    col1, col2 = st.columns(2)

    with col1:
        email_different = st.selectbox("Communication email different from registration?", ["No", "Yes"])
        communication_email_different_score = 0 if email_different == "No" else 75

    with col2:
        whatsapp_different = st.selectbox("WhatsApp number different from phone?", ["No", "Yes"])
        whatsapp_number_different_score = 0 if whatsapp_different == "No" else 60

    # Calculate score
    score = calculate_lead_score(
        location_score, how_you_know_us_score, sibling_in_school_score,
        previous_school_name_score, class_applied_for_score,
        last_class_percentage_score, communication_email_different_score,
        whatsapp_number_different_score
    )

    category = categorize_lead(score)
    color = get_lead_color(category)

    # Display results
    st.markdown("---")
    st.subheader("📊 Lead Scoring Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Lead Score", f"{score}/100", help="Overall lead quality score")

    with col2:
        st.markdown(
            f"**Category:** <span style='color: {color}; font-weight: bold; font-size: 18px;'>{category}</span>",
            unsafe_allow_html=True)

    with col3:
        # Gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Score", 'font': {'size': 16}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1},
                'bar': {'color': color, 'thickness': 0.3},
                'steps': [
                    {'range': [0, 60], 'color': "#E8F4FD"},
                    {'range': [60, 80], 'color': "#FFF2E8"},
                    {'range': [80, 100], 'color': "#FFE8E8"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 3},
                    'thickness': 0.8,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)

    # Recommendations
    st.subheader("💡 Recommendations")
    if score >= 80:
        st.success("🎉 **High Priority Lead!** Contact immediately and schedule a school visit.")
    elif score >= 60:
        st.warning("📞 **Good Prospect!** Follow up within 2-3 days with personalized communication.")
    else:
        st.info("📧 **Nurture Lead!** Add to newsletter and follow up periodically.")

with tab2:
    st.header("📊 Sample Data Analysis")
    st.markdown("*Analyze our generated sample dataset of 150 prospective students*")

    # Calculate scores for sample data
    df = st.session_state.sample_data.copy()

    df['lead_score'] = df.apply(lambda row: calculate_lead_score(
        row['location_score'], row['how_you_know_us_score'],
        row['sibling_in_school_score'], row['previous_school_name_score'],
        row['class_applied_for_score'], row['last_class_percentage_score'],
        row['communication_email_different_score'], row['whatsapp_number_different_score']
    ), axis=1)

    df['lead_category'] = df['lead_score'].apply(categorize_lead)

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Students", len(df))
    with col2:
        st.metric("Average Score", f"{df['lead_score'].mean():.1f}")
    with col3:
        hot_leads = len(df[df['lead_category'] == '🔥 Hot Lead'])
        st.metric("🔥 Hot Leads", hot_leads)
    with col4:
        warm_leads = len(df[df['lead_category'] == '🟡 Warm Lead'])
        st.metric("🟡 Warm Leads", warm_leads)

    # Visualizations
    col1, col2 = st.columns(2)

    with col1:
        # Category distribution
        category_counts = df['lead_category'].value_counts()
        fig_pie = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title="Lead Category Distribution",
            color=category_counts.index,
            color_discrete_map={
                "🔥 Hot Lead": "#FF4B4B",
                "🟡 Warm Lead": "#FFA500",
                "❄️ Cold Lead": "#4B8BFF"
            }
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Score distribution
        fig_hist = px.histogram(
            df, x='lead_score', nbins=20,
            title="Lead Score Distribution",
            color='lead_category',
            color_discrete_map={
                "🔥 Hot Lead": "#FF4B4B",
                "🟡 Warm Lead": "#FFA500",
                "❄️ Cold Lead": "#4B8BFF"
            }
        )
        fig_hist.update_layout(xaxis_title="Lead Score", yaxis_title="Count")
        st.plotly_chart(fig_hist, use_container_width=True)

    # Top prospects
    st.subheader("🏆 Top 10 Prospects")
    top_prospects = df.nlargest(10, 'lead_score')[
        ['student_name', 'email', 'phone', 'location', 'class_applied_for', 'lead_score', 'lead_category']]
    st.dataframe(top_prospects, use_container_width=True)

    # Detailed data with filters
    st.subheader("🔍 Detailed Analysis")

    col1, col2, col3 = st.columns(3)
    with col1:
        category_filter = st.multiselect(
            "Filter by Category",
            options=df['lead_category'].unique(),
            default=df['lead_category'].unique()
        )
    with col2:
        class_filter = st.multiselect(
            "Filter by Class",
            options=sorted(df['class_applied_for'].unique()),
            default=sorted(df['class_applied_for'].unique())
        )
    with col3:
        score_range = st.slider("Score Range", 0, 100, (0, 100))

    # Apply filters
    filtered_df = df[
        (df['lead_category'].isin(category_filter)) &
        (df['class_applied_for'].isin(class_filter)) &
        (df['lead_score'] >= score_range[0]) &
        (df['lead_score'] <= score_range[1])
        ]

    st.dataframe(filtered_df, use_container_width=True)

    # Download buttons
    col1, col2 = st.columns(2)
    with col1:
        csv_data = filtered_df.to_csv(index=False)
        st.download_button("📥 Download Filtered Data", csv_data, "filtered_leads.csv", "text/csv")
    with col2:
        scoring_template = df[['location_score', 'how_you_know_us_score', 'sibling_in_school_score',
                               'previous_school_name_score', 'class_applied_for_score',
                               'last_class_percentage_score', 'communication_email_different_score',
                               'whatsapp_number_different_score']].head(10)
        template_csv = scoring_template.to_csv(index=False)
        st.download_button("📋 Download Scoring Template", template_csv, "scoring_template.csv", "text/csv")

with tab3:
    st.header("📁 Upload Your CSV File")
    st.markdown("*Upload your own student data for bulk lead scoring*")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv", help="Upload a CSV file with student data")

    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file)

            st.subheader("📋 Uploaded Data Preview")
            st.dataframe(df_upload.head(10))

            # Check required columns
            required_columns = [
                'location_score', 'how_you_know_us_score', 'sibling_in_school_score',
                'previous_school_name_score', 'class_applied_for_score',
                'last_class_percentage_score', 'communication_email_different_score',
                'whatsapp_number_different_score'
            ]

            missing_columns = [col for col in required_columns if col not in df_upload.columns]

            if missing_columns:
                st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
                st.info("💡 Please ensure your CSV has all required scoring columns.")

                # Show required format
                st.subheader("Required CSV Format")
                sample_format = pd.DataFrame({
                    'student_name': ['John Doe', 'Jane Smith'],
                    'location_score': [85, 60],
                    'how_you_know_us_score': [70, 80],
                    'sibling_in_school_score': [100, 0],
                    'previous_school_name_score': [80, 70],
                    'class_applied_for_score': [75, 80],
                    'last_class_percentage_score': [90, 75],
                    'communication_email_different_score': [0, 100],
                    'whatsapp_number_different_score': [0, 100]
                })
                st.dataframe(sample_format)

            else:
                # Calculate scores
                df_upload['lead_score'] = df_upload.apply(lambda row: calculate_lead_score(
                    row['location_score'], row['how_you_know_us_score'],
                    row['sibling_in_school_score'], row['previous_school_name_score'],
                    row['class_applied_for_score'], row['last_class_percentage_score'],
                    row['communication_email_different_score'], row['whatsapp_number_different_score']
                ), axis=1)

                df_upload['lead_category'] = df_upload['lead_score'].apply(categorize_lead)

                # Display results
                st.success("✅ Successfully processed your data!")

                # Summary
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Records", len(df_upload))
                with col2:
                    st.metric("Average Score", f"{df_upload['lead_score'].mean():.1f}")
                with col3:
                    st.metric("Hot Leads", len(df_upload[df_upload['lead_category'] == '🔥 Hot Lead']))
                with col4:
                    st.metric("Warm Leads", len(df_upload[df_upload['lead_category'] == '🟡 Warm Lead']))

                # Results table
                st.subheader("📊 Scoring Results")
                st.dataframe(df_upload, use_container_width=True)

                # Download results
                results_csv = df_upload.to_csv(index=False)
                st.download_button("📥 Download Results", results_csv, "lead_scoring_results.csv", "text/csv")

        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")

    else:
        st.info("👆 Please upload a CSV file to begin bulk analysis")

        # Show template
        st.subheader("📝 CSV Template")
        st.markdown("Your CSV should have these columns with scores between 0-100:")

        template_data = {
            'student_name': ['Aarav Sharma', 'Priya Gupta', 'Rohan Singh'],
            'location_score': [85, 60, 70],
            'how_you_know_us_score': [70, 80, 65],
            'sibling_in_school_score': [100, 0, 50],
            'previous_school_name_score': [80, 70, 75],
            'class_applied_for_score': [75, 80, 70],
            'last_class_percentage_score': [90, 75, 85],
            'communication_email_different_score': [0, 100, 25],
            'whatsapp_number_different_score': [0, 100, 50]
        }

        template_df = pd.DataFrame(template_data)
        st.dataframe(template_df)

        # Download template
        template_csv = template_df.to_csv(index=False)
        st.download_button("📋 Download Template", template_csv, "lead_scoring_template.csv", "text/csv")