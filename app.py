import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Entab's Lead Scoring System",
    page_icon="🎓",
    layout="wide"
)

# Title and description
st.title("🎓 Educational Lead Scoring System")
st.markdown("---")


def calculate_lead_score(location_score, how_you_know_us_score, sibling_in_school_score,
                         previous_school_name_score, class_applied_for_score,
                         last_class_percentage_score, communication_email_different_score,
                         whatsapp_number_different_score):
    """Calculate lead score using the corrected formula"""

    # Weights for each factor
    weights = [0.85, 0.70, 0.95, 0.55, 0.50, 0.25, 0.25, 0.20]
    scores = [location_score, how_you_know_us_score, sibling_in_school_score,
              previous_school_name_score, class_applied_for_score,
              last_class_percentage_score, communication_email_different_score,
              whatsapp_number_different_score]

    # Calculate weighted sum
    weighted_sum = sum(score * weight for score, weight in zip(scores, weights))

    # Calculate total weights
    total_weights = sum(weights)

    # Calculate final score (this will be between 0-100)
    lead_score = (weighted_sum / total_weights)

    return lead_score


def categorize_lead(score):
    """Categorize leads based on score"""
    if score >= 80:
        return "Hot Lead"
    elif score >= 60:
        return "Warm Lead"
    else:
        return "Cold Lead"


def get_lead_color(category):
    """Get color for lead category"""
    colors = {
        "Hot Lead": "#FF4B4B",
        "Warm Lead": "#FFA500",
        "Cold Lead": "#4B8BFF"
    }
    return colors.get(category, "#808080")


# Main tabs for navigation
tab1, tab2, tab3 = st.tabs(["🎯 Individual Prediction", "📁 Bulk CSV Analysis", "📖 About Formula"])

with tab1:
    st.header("Individual Lead Scoring")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Student Information")
        location_score = st.slider("Location Score (proximity to school)", 0, 100, 50,
                                   help="How close is the student's location to the school")
        how_you_know_us_score = st.slider("How You Know Us Score", 0, 100, 50,
                                          help="Source through which student learned about the school")
        sibling_in_school_score = st.slider("Sibling in School Score", 0, 100, 50,
                                            help="Whether student has siblings in the school")
        previous_school_name_score = st.slider("Previous School Name Score", 0, 100, 50,
                                               help="Quality/reputation of previous school")

    with col2:
        st.subheader("Academic & Contact Information")
        class_applied_for_score = st.slider("Class Applied For Score", 0, 100, 50,
                                            help="Grade/class student is applying for")
        last_class_percentage_score = st.slider("Last Class Percentage Score", 0, 100, 50,
                                                help="Academic performance in previous class")
        communication_email_different_score = st.slider("Communication Email Different Score", 0, 100, 50,
                                                        help="Whether communication email differs from registration email")
        whatsapp_number_different_score = st.slider("WhatsApp Number Different Score", 0, 100, 50,
                                                    help="Whether WhatsApp number differs from registration number")

    # Calculate score automatically
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
    st.subheader("📊 Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Lead Score", f"{score:.1f}")

    with col2:
        st.markdown(f"**Lead Category:** <span style='color: {color}; font-weight: bold;'>{category}</span>",
                    unsafe_allow_html=True)

    with col3:
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Score"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 60], 'color': "lightblue"},
                    {'range': [60, 80], 'color': "lightyellow"},
                    {'range': [80, 100], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Bulk CSV Analysis")

    # File upload
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)

            st.subheader("📋 Data Preview")
            st.dataframe(df.head())

            # Check if required columns exist
            required_columns = [
                'location_score', 'how_you_know_us_score', 'sibling_in_school_score',
                'previous_school_name_score', 'class_applied_for_score',
                'last_class_percentage_score', 'communication_email_different_score',
                'whatsapp_number_different_score'
            ]

            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                st.error(f"Missing required columns: {', '.join(missing_columns)}")
                st.info("Please ensure your CSV has all required columns with the exact names shown above.")
            else:
                # Calculate lead scores for all rows
                df['lead_score'] = df.apply(lambda row: calculate_lead_score(
                    row['location_score'], row['how_you_know_us_score'],
                    row['sibling_in_school_score'], row['previous_school_name_score'],
                    row['class_applied_for_score'], row['last_class_percentage_score'],
                    row['communication_email_different_score'], row['whatsapp_number_different_score']
                ), axis=1)

                df['lead_category'] = df['lead_score'].apply(categorize_lead)

                # Display summary statistics
                st.subheader("📊 Summary Statistics")
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Total Students", len(df))

                with col2:
                    st.metric("Average Score", f"{df['lead_score'].mean():.1f}")

                with col3:
                    st.metric("Hot Leads", len(df[df['lead_category'] == 'Hot Lead']))

                with col4:
                    st.metric("Warm Leads", len(df[df['lead_category'] == 'Warm Lead']))

                # Create visualizations
                st.subheader("📈 Lead Distribution")

                col1, col2 = st.columns(2)

                with col1:
                    # Pie chart for lead categories
                    category_counts = df['lead_category'].value_counts()

                    fig_pie = px.pie(
                        values=category_counts.values,
                        names=category_counts.index,
                        title="Lead Categories Distribution",
                        color=category_counts.index,
                        color_discrete_map={
                            "Hot Lead": "#FF4B4B",
                            "Warm Lead": "#FFA500",
                            "Cold Lead": "#4B8BFF"
                        }
                    )
                    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_pie, use_container_width=True)

                with col2:
                    # Histogram of lead scores
                    fig_hist = px.histogram(
                        df,
                        x='lead_score',
                        nbins=20,
                        title="Lead Score Distribution",
                        color='lead_category',
                        color_discrete_map={
                            "Hot Lead": "#FF4B4B",
                            "Warm Lead": "#FFA500",
                            "Cold Lead": "#4B8BFF"
                        }
                    )
                    fig_hist.update_layout(xaxis_title="Lead Score", yaxis_title="Count")
                    st.plotly_chart(fig_hist, use_container_width=True)

                # Feature importance analysis
                st.subheader("🔍 Feature Analysis")

                # Calculate correlation with lead score
                feature_columns = required_columns
                correlations = []

                for col in feature_columns:
                    corr = df[col].corr(df['lead_score'])
                    correlations.append({'Feature': col.replace('_', ' ').title(), 'Correlation': corr})

                corr_df = pd.DataFrame(correlations).sort_values('Correlation', ascending=True)

                fig_bar = px.bar(
                    corr_df,
                    x='Correlation',
                    y='Feature',
                    orientation='h',
                    title="Feature Correlation with Lead Score",
                    color='Correlation',
                    color_continuous_scale='RdYlBu_r'
                )
                st.plotly_chart(fig_bar, use_container_width=True)

                # Display detailed results
                st.subheader("📋 Detailed Results")

                # Add filters
                col1, col2 = st.columns(2)
                with col1:
                    category_filter = st.multiselect(
                        "Filter by Lead Category",
                        options=df['lead_category'].unique(),
                        default=df['lead_category'].unique()
                    )

                with col2:
                    score_range = st.slider(
                        "Filter by Score Range",
                        min_value=float(df['lead_score'].min()),
                        max_value=float(df['lead_score'].max()),
                        value=(float(df['lead_score'].min()), float(df['lead_score'].max()))
                    )

                # Apply filters
                filtered_df = df[
                    (df['lead_category'].isin(category_filter)) &
                    (df['lead_score'] >= score_range[0]) &
                    (df['lead_score'] <= score_range[1])
                    ]

                st.dataframe(filtered_df[['lead_score', 'lead_category'] + required_columns])

                # Download button for results
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="Download Results as CSV",
                    data=csv,
                    file_name="lead_scoring_results.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

    else:
        st.info("Please upload a CSV file to begin analysis.")

        # Show sample data format
        st.subheader("📝 Required CSV Format")
        sample_data = {
            'location_score': [85, 60, 40, 90, 70],
            'how_you_know_us_score': [70, 80, 50, 85, 60],
            'sibling_in_school_score': [100, 0, 0, 100, 50],
            'previous_school_name_score': [80, 70, 60, 90, 75],
            'class_applied_for_score': [75, 80, 70, 85, 65],
            'last_class_percentage_score': [90, 75, 60, 95, 80],
            'communication_email_different_score': [0, 100, 50, 0, 25],
            'whatsapp_number_different_score': [0, 100, 75, 0, 50]
        }

        sample_df = pd.DataFrame(sample_data)
        st.dataframe(sample_df)

        # Download sample CSV
        sample_csv = sample_df.to_csv(index=False)
        st.download_button(
            label="Download Sample CSV Template",
            data=sample_csv,
            file_name="lead_scoring_template.csv",
            mime="text/csv"
        )

with tab3:
    st.header("About the Lead Scoring Formula")

    st.markdown("""
    ### Formula Breakdown

    The lead scoring system uses a weighted average of 8 different factors:

    ```
    lead_score = [(location_score × 0.85) + 
                  (how_you_know_us_score × 0.70) + 
                  (sibling_in_school_score × 0.95) + 
                  (previous_school_name_score × 0.65) + 
                  (class_applied_for_score × 0.60) + 
                  (last_class_percentage_score × 0.55) + 
                  (communication_email_different_score × 0.45) + 
                  (whatsapp_number_different_score × 0.40)] 
                  ÷ (0.85 + 0.70 + 0.85 + 0.65 + 0.60 + 0.55 + 0.45 + 0.40)
    ```

    ### Factor Weights & Importance
    """)

    # Create weights visualization
    weights_data = {
        'Factor': [
            'Location Score', 'Sibling in School', 'How You Know Us',
            'Previous School Name', 'Class Applied For', 'Last Class Percentage',
            'Communication Email Different', 'WhatsApp Number Different'
        ],
        'Weight': [0.85, 0.85, 0.70, 0.65, 0.60, 0.55, 0.45, 0.40],
        'Description': [
            'Proximity to school location',
            'Whether student has siblings in school',
            'Source of school awareness',
            'Quality of previous school',
            'Grade level applying for',
            'Academic performance',
            'Email consistency check',
            'Phone number consistency check'
        ]
    }

    weights_df = pd.DataFrame(weights_data)

    fig_weights = px.bar(
        weights_df,
        x='Weight',
        y='Factor',
        orientation='h',
        title="Factor Weights in Lead Scoring",
        color='Weight',
        color_continuous_scale='viridis'
    )
    fig_weights.update_layout(height=500)
    st.plotly_chart(fig_weights, use_container_width=True)

    st.markdown("""
    ### Lead Categories

    - **🔥 Hot Lead (80-100)**: High probability of enrollment
    - **🟡 Warm Lead (60-79)**: Moderate probability of enrollment  
    - **❄️ Cold Lead (0-59)**: Lower probability of enrollment

    ### Key Improvements Made

    1. **Removed sidebar navigation** - Now uses cleaner tabs for better user experience
    2. **Fixed formula calculation** - Lead scores now properly range from 0-100
    3. **Real-time calculation** - Individual scores update automatically without button click
    4. **Improved layout** - More intuitive and streamlined interface

    ### CSV File Requirements

    Your CSV file must contain these exact column names:
    - `location_score`
    - `how_you_know_us_score`
    - `sibling_in_school_score`
    - `previous_school_name_score`
    - `class_applied_for_score`
    - `last_class_percentage_score`
    - `communication_email_different_score`
    - `whatsapp_number_different_score`

    All scores should be between 0-100.
    """)

# Footer
st.markdown("---")
st.markdown("*Educational Lead Scoring System - Developed for optimizing student enrollment processes*")