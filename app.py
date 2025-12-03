import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Survey Dashboard",
    page_icon="📊",
    layout="wide"
)

# Password Protection
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.write("*Please enter the password to access the dashboard.*")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct
        return True

if not check_password():
    st.stop()  # Do not continue if check_password is not True

# File Upload
st.sidebar.title("📁 Data Upload")
uploaded_file = st.sidebar.file_uploader(
    "Upload Survey CSV",
    type=['csv'],
    help="Upload your Rocscience Core Values Survey CSV file"
)

if uploaded_file is None:
    st.info("👈 Please upload your survey CSV file using the sidebar to begin.")
    st.markdown("""
    ### Instructions:
    1. Use the file uploader in the sidebar
    2. Select your survey CSV file
    3. The dashboard will load automatically
    
    **Expected file format:** Rocscience Core Values Survey CSV
    """)
    st.stop()

@st.cache_data
def load_data(uploaded_file):
    """Load and process the survey data"""
    # Read the CSV file with proper encoding
    df = pd.read_csv(uploaded_file, skiprows=1, encoding='cp1252')
    
    # Reset file pointer and get questions from first row
    uploaded_file.seek(0)
    questions_df = pd.read_csv(uploaded_file, nrows=1, encoding='cp1252')
    questions = questions_df.columns.tolist()
    
    # Rename columns to match questions
    df.columns = questions
    
    # Clean column names for easier access
    df = df.rename(columns={
        'Please check the Department or Team you primarily work with.': 'Department',
        'How long have you been with Rocscience?': 'Tenure',
        'Respondent ID': 'Respondent_ID'
    })
    
    # Drop the "Other (please specify)" column and "Response" columns if they exist
    cols_to_drop = [col for col in df.columns if 'Other (please specify)' in str(col) or col == 'Response']
    df = df.drop(columns=cols_to_drop, errors='ignore')
    
    return df

def get_likert_columns(df):
    """Get columns that contain Likert scale responses"""
    likert_values = ['Strongly Agree', 'Agree', 'Disagree', 'Strongly Disagree', "Don't Know"]
    likert_cols = []
    
    for col in df.columns:
        if col not in ['Respondent_ID', 'Department', 'Tenure'] and not col.startswith('Open-Ended'):
            # Check if column has Likert responses
            unique_vals = df[col].dropna().unique()
            if any(val in likert_values for val in unique_vals):
                likert_cols.append(col)
    
    return likert_cols

def categorize_questions(likert_cols):
    """Categorize questions by theme based on keywords"""
    categories = {
        'Customer Focused': [],
        'Innovation': [],
        'Excellence': [],
        'Accountability': [],
        'Supportive': [],
        'Culture & Values Awareness': [],
        'Growth & Change': [],
        'Other': []
    }
    
    for col in likert_cols:
        col_lower = col.lower()
        if 'customer' in col_lower:
            categories['Customer Focused'].append(col)
        elif 'innov' in col_lower or 'new' in col_lower or 'bold' in col_lower:
            categories['Innovation'].append(col)
        elif 'excellence' in col_lower or 'high standard' in col_lower or 'deliver great' in col_lower or 'pride' in col_lower or 'best' in col_lower:
            categories['Excellence'].append(col)
        elif 'accountab' in col_lower or 'own' in col_lower or 'decision' in col_lower and 'own' in col_lower:
            categories['Accountability'].append(col)
        elif 'support' in col_lower or 'help' in col_lower or 'encourag' in col_lower:
            categories['Supportive'].append(col)
        elif 'value' in col_lower or 'culture' in col_lower or 'mission' in col_lower or 'recommend' in col_lower:
            categories['Culture & Values Awareness'].append(col)
        elif 'growth' in col_lower or 'change' in col_lower or 'acquisition' in col_lower or 'anxious' in col_lower or 'expand' in col_lower:
            categories['Growth & Change'].append(col)
        else:
            categories['Other'].append(col)
    
    # Remove empty categories
    return {k: v for k, v in categories.items() if v}

def group_responses(series, group_mode, exclude_dont_know=False):
    """Group responses based on mode and optionally exclude Don't Know"""
    if group_mode:
        # Grouped mode: Positive, Negative, Don't Know
        mapping = {
            'Strongly Agree': 'Positive',
            'Agree': 'Positive',
            'Strongly Disagree': 'Negative',
            'Disagree': 'Negative',
            "Don't Know": "Don't Know"
        }
        result = series.map(mapping)
    else:
        # Original mode: keep all 5 categories
        result = series
    
    # Remove Don't Know if requested
    if exclude_dont_know:
        result = result[result != "Don't Know"]
    
    return result

def calculate_response_distribution(df, columns, group_mode, exclude_dont_know=False):
    """Calculate response distribution for selected columns"""
    all_responses = []
    
    for col in columns:
        responses = df[col].dropna()
        grouped = group_responses(responses, group_mode, exclude_dont_know)
        all_responses.extend(grouped.tolist())
    
    if not all_responses:
        return pd.Series(dtype=int)
    
    distribution = pd.Series(all_responses).value_counts()
    return distribution

def main():
    st.title("📊 Survey Data Dashboard")
    st.markdown("### Rocscience Core Values Survey Analysis")
    
    # Load data
    try:
        df = load_data(uploaded_file)
    except Exception as e:
        st.error(f"⚠️ Error loading CSV file: {str(e)}")
        st.info("Please make sure you've uploaded a valid Rocscience Core Values Survey CSV file.")
        return
    
    likert_cols = get_likert_columns(df)
    question_categories = categorize_questions(likert_cols)
    
    # Logout button
    if st.sidebar.button("🔒 Logout"):
        st.session_state["password_correct"] = False
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Department filter
    departments = df['Department'].dropna().unique().tolist()
    selected_departments = st.sidebar.multiselect(
        "Department",
        options=departments,
        default=departments
    )
    
    # Tenure filter
    tenure_options = df['Tenure'].dropna().unique().tolist()
    selected_tenure = st.sidebar.multiselect(
        "Tenure",
        options=tenure_options,
        default=tenure_options
    )
    
    st.sidebar.markdown("---")
    
    # Question category selector
    st.sidebar.header("Question Categories")
    selected_categories = st.sidebar.multiselect(
        "Select Categories",
        options=list(question_categories.keys()),
        default=list(question_categories.keys())
    )
    
    st.sidebar.markdown("---")
    
    # Response options
    st.sidebar.header("Response Options")
    group_responses_mode = st.sidebar.checkbox(
        "Group responses",
        value=False,
        help="When enabled: Groups 'Strongly Agree' + 'Agree' into 'Positive', and 'Strongly Disagree' + 'Disagree' into 'Negative'. 'Don't Know' remains separate."
    )
    
    exclude_dont_know = st.sidebar.checkbox(
        "Exclude 'Don't Know'",
        value=False,
        help="When enabled: Removes all 'Don't Know' responses from calculations and visualizations."
    )
    
    # Filter data
    filtered_df = df[
        (df['Department'].isin(selected_departments)) &
        (df['Tenure'].isin(selected_tenure))
    ]
    
    # Get selected question columns
    selected_questions = []
    for cat in selected_categories:
        selected_questions.extend(question_categories.get(cat, []))
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Responses", len(filtered_df))
    
    with col2:
        st.metric("Selected Questions", len(selected_questions))
    
    # Calculate overall sentiment
    if selected_questions:
        distribution = calculate_response_distribution(filtered_df, selected_questions, group_responses_mode, exclude_dont_know)
        
        if group_responses_mode and 'Positive' in distribution.index:
            total = distribution.sum()
            positive_pct = (distribution.get('Positive', 0) / total * 100) if total > 0 else 0
            with col3:
                st.metric("Positive Responses", f"{positive_pct:.1f}%")
        else:
            agree_count = distribution.get('Strongly Agree', 0) + distribution.get('Agree', 0)
            total = distribution.sum()
            agree_pct = (agree_count / total * 100) if total > 0 else 0
            with col3:
                st.metric("Agree + Strongly Agree", f"{agree_pct:.1f}%")
    
    st.markdown("---")
    
    # Create tabs
    tab1, tab2 = st.tabs(["📊 Overview", "📋 Detailed Questions"])
    
    # Main visualizations
    if not selected_questions:
        st.warning("⚠️ Please select at least one question category to view results.")
        return
    
    with tab1:
        # Overall Distribution
        st.subheader("Overall Response Distribution")
        
        distribution = calculate_response_distribution(filtered_df, selected_questions, group_responses_mode, exclude_dont_know)
        
        if not distribution.empty:
            # Calculate percentages
            total_responses = distribution.sum()
            distribution_pct = (distribution / total_responses * 100).round(1)
            
            # Create bar chart
            if group_responses_mode:
                color_map = {
                    'Positive': '#2ecc71',
                    'Negative': '#e74c3c',
                    "Don't Know": '#95a5a6'
                }
                if exclude_dont_know:
                    order = ['Positive', 'Negative']
                else:
                    order = ['Positive', "Don't Know", 'Negative']
            else:
                color_map = {
                    'Strongly Agree': '#27ae60',
                    'Agree': '#2ecc71',
                    "Don't Know": '#95a5a6',
                    'Disagree': '#e67e22',
                    'Strongly Disagree': '#e74c3c'
                }
                if exclude_dont_know:
                    order = ['Strongly Agree', 'Agree', 'Disagree', 'Strongly Disagree']
                else:
                    order = ['Strongly Agree', 'Agree', "Don't Know", 'Disagree', 'Strongly Disagree']
            
            # Reorder based on available responses
            ordered_distribution = distribution_pct.reindex([o for o in order if o in distribution_pct.index])
            
            fig = go.Figure(data=[
                go.Bar(
                    x=ordered_distribution.index,
                    y=ordered_distribution.values,
                    text=[f"{v:.1f}%<br>({distribution[k]} responses)" for k, v in zip(ordered_distribution.index, ordered_distribution.values)],
                    textposition='auto',
                    marker_color=[color_map.get(x, '#3498db') for x in ordered_distribution.index]
                )
            ])
            
            fig.update_layout(
                xaxis_title="Response",
                yaxis_title="Percentage (%)",
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("No responses to display with current filters.")
        
        # Comparison by Department
        st.subheader("Response Distribution by Department")
        
        dept_data = []
        for dept in selected_departments:
            dept_df = filtered_df[filtered_df['Department'] == dept]
            dist = calculate_response_distribution(dept_df, selected_questions, group_responses_mode)
            
            if not dist.empty:
                total = dist.sum()
                for response_type, count in dist.items():
                    dept_data.append({
                        'Department': dept,
                        'Response': response_type,
                        'Percentage': (count / total * 100) if total > 0 else 0,
                        'Count': count
                    })
        
        if dept_data:
            dept_df_plot = pd.DataFrame(dept_data)
            
            if group_responses_mode:
                if exclude_dont_know:
                    category_order = ['Positive', 'Negative']
                else:
                    category_order = ['Positive', "Don't Know", 'Negative']
            else:
                if exclude_dont_know:
                    category_order = ['Strongly Agree', 'Agree', 'Disagree', 'Strongly Disagree']
                else:
                    category_order = ['Strongly Agree', 'Agree', "Don't Know", 'Disagree', 'Strongly Disagree']
            
            fig = px.bar(
                dept_df_plot,
                x='Department',
                y='Percentage',
                color='Response',
                barmode='group',
                category_orders={'Response': [c for c in category_order if c in dept_df_plot['Response'].unique()]},
                color_discrete_map=color_map,
                hover_data=['Count']
            )
            
            fig.update_layout(
                xaxis_title="Department",
                yaxis_title="Percentage (%)",
                height=450
            )
            
            st.plotly_chart(fig, width='stretch')
        
        # Comparison by Tenure
        st.subheader("Response Distribution by Tenure")
        
        tenure_data = []
        for tenure in selected_tenure:
            tenure_df = filtered_df[filtered_df['Tenure'] == tenure]
            dist = calculate_response_distribution(tenure_df, selected_questions, group_responses_mode)
            
            if not dist.empty:
                total = dist.sum()
                for response_type, count in dist.items():
                    tenure_data.append({
                        'Tenure': tenure,
                        'Response': response_type,
                        'Percentage': (count / total * 100) if total > 0 else 0,
                        'Count': count
                    })
        
        if tenure_data:
            tenure_df_plot = pd.DataFrame(tenure_data)
            
            fig = px.bar(
                tenure_df_plot,
                x='Tenure',
                y='Percentage',
                color='Response',
                barmode='group',
                category_orders={'Response': [c for c in category_order if c in tenure_df_plot['Response'].unique()]},
                color_discrete_map=color_map,
                hover_data=['Count']
            )
            
            fig.update_layout(
                xaxis_title="Tenure",
                yaxis_title="Percentage (%)",
                height=450
            )
            
            st.plotly_chart(fig, width='stretch')
        
        # Individual Question Analysis
        st.markdown("---")
        st.subheader("Quick Question Analysis")
        
        # Search functionality for questions
        search_query = st.text_input(
            "Search questions:",
            value="",
            key="question_search_overview",
            placeholder="Type to filter questions..."
        )
        
        # Filter questions based on search
        if search_query:
            filtered_questions = [q for q in selected_questions if search_query.lower() in q.lower()]
        else:
            filtered_questions = selected_questions
        
        # Show count of filtered questions
        if search_query:
            st.caption(f"Showing {len(filtered_questions)} of {len(selected_questions)} questions")
        
        # Allow user to select a specific question
        if filtered_questions:
            selected_question = st.selectbox(
                "Select a question to analyze in detail:",
                options=filtered_questions,
                key="question_selector_overview"
            )
        else:
            st.warning("No questions match your search.")
            selected_question = None
        
        if selected_question:
            question_responses = filtered_df[selected_question].dropna()
            grouped_responses = group_responses(question_responses, group_responses_mode, exclude_dont_know)
            
            if not grouped_responses.empty:
                dist = grouped_responses.value_counts()
                total = dist.sum()
                dist_pct = (dist / total * 100).round(1)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Pie chart
                    fig = go.Figure(data=[go.Pie(
                        labels=dist.index,
                        values=dist.values,
                        marker_colors=[color_map.get(x, '#3498db') for x in dist.index],
                        textinfo='label+percent',
                        hovertemplate='%{label}<br>%{value} responses<br>%{percent}<extra></extra>'
                    )])
                    
                    fig.update_layout(
                        title=f"Response Distribution",
                        height=400
                    )
                    
                    st.plotly_chart(fig, width='stretch')
                
                with col2:
                    # Summary statistics
                    st.markdown("**Response Summary**")
                    for response_type in dist.index:
                        count = dist[response_type]
                        pct = dist_pct[response_type]
                        st.markdown(f"- **{response_type}**: {count} responses ({pct:.1f}%)")
                    
                    st.markdown(f"\n**Total Responses**: {total}")
        
        # Determine sort options based on grouping mode (used by both heatmaps)
        if group_responses_mode:
            if exclude_dont_know:
                sort_options = ['None', 'Positive', 'Negative']
            else:
                sort_options = ['None', 'Positive', "Don't Know", 'Negative']
        else:
            if exclude_dont_know:
                sort_options = ['None', 'Strongly Agree', 'Agree', 'Disagree', 'Strongly Disagree']
            else:
                sort_options = ['None', 'Strongly Agree', 'Agree', "Don't Know", 'Disagree', 'Strongly Disagree']
        
        # Heatmap of responses by category
        st.markdown("---")
        st.subheader("Response Heatmap by Question Category")
        
        # Add sorting for category heatmap
        category_sort_by = 'None'  # Default value
        category_sort_ascending = True
        if len(selected_categories) > 1:
            col_cat_sort1, col_cat_sort2, col_cat_sort3 = st.columns([2, 1, 1])
            
            with col_cat_sort2:
                category_sort_by = st.selectbox(
                    "Sort categories by:",
                    options=sort_options,
                    index=0,
                    key="category_heatmap_sort",
                    help="Sort categories by percentage of selected response"
                )
            
            with col_cat_sort3:
                if category_sort_by != 'None':
                    category_sort_ascending = st.checkbox(
                        "Ascending",
                        value=True,
                        key="category_sort_order",
                        help="Check for ascending (low to high), uncheck for descending (high to low)"
                    )
            
            with col_cat_sort1:
                if category_sort_by != 'None':
                    cat_sort_direction = "ascending (low to high)" if category_sort_ascending else "descending (high to low)"
                    st.markdown(f"Categories sorted by **{category_sort_by}** ({cat_sort_direction})")
                else:
                    st.markdown("")
        
        if len(selected_categories) > 1:
            heatmap_data = []
            
            for cat in selected_categories:
                cat_questions = question_categories.get(cat, [])
                if cat_questions:
                    dist = calculate_response_distribution(filtered_df, cat_questions, group_responses_mode)
                    
                    if not dist.empty:
                        total = dist.sum()
                        for response_type in dist.index:
                            heatmap_data.append({
                                'Category': cat,
                                'Response': response_type,
                                'Percentage': (dist[response_type] / total * 100) if total > 0 else 0
                            })
            
            if heatmap_data:
                heatmap_df = pd.DataFrame(heatmap_data)
                pivot_df = heatmap_df.pivot(index='Category', columns='Response', values='Percentage').fillna(0)
                
                # Reorder columns
                if group_responses_mode:
                    if exclude_dont_know:
                        col_order = ['Positive', 'Negative']
                    else:
                        col_order = ['Positive', "Don't Know", 'Negative']
                else:
                    if exclude_dont_know:
                        col_order = ['Strongly Agree', 'Agree', 'Disagree', 'Strongly Disagree']
                    else:
                        col_order = ['Strongly Agree', 'Agree', "Don't Know", 'Disagree', 'Strongly Disagree']
                
                pivot_df = pivot_df[[col for col in col_order if col in pivot_df.columns]]
                
                # Sort if a sort option is selected
                if category_sort_by != 'None' and category_sort_by in pivot_df.columns:
                    pivot_df = pivot_df.sort_values(by=category_sort_by, ascending=category_sort_ascending)
                
                fig = go.Figure(data=go.Heatmap(
                    z=pivot_df.values,
                    x=pivot_df.columns,
                    y=pivot_df.index,
                    colorscale='RdYlGn',
                    text=pivot_df.values.round(1),
                    texttemplate='%{text}%',
                    textfont={"size": 12},
                    hovertemplate='Category: %{y}<br>Response: %{x}<br>Percentage: %{z:.1f}%<extra></extra>'
                ))
                
                fig.update_layout(
                    xaxis_title="Response Type",
                    yaxis_title="Question Category",
                    height=max(400, len(selected_categories) * 60)
                )
                
                st.plotly_chart(fig, width='stretch')
        
        # Detailed heatmap by individual question
        st.markdown("---")
        st.subheader("Response Heatmap by Individual Question")
        
        # Sorting options
        col_sort1, col_sort2, col_sort3 = st.columns([2, 1, 1])
        
        with col_sort2:
            sort_by = st.selectbox(
                "Sort by:",
                options=sort_options,
                index=0,
                key="heatmap_sort",
                help="Sort questions by percentage of selected response"
            )
        
        with col_sort3:
            if sort_by != 'None':
                sort_ascending = st.checkbox(
                    "Ascending",
                    value=True,
                    key="heatmap_sort_order",
                    help="Check for ascending (low to high), uncheck for descending (high to low)"
                )
            else:
                sort_ascending = True
        
        with col_sort1:
            if sort_by != 'None':
                sort_direction = "ascending (low to high)" if sort_ascending else "descending (high to low)"
                st.markdown(f"Questions sorted by **{sort_by}** ({sort_direction}). Scroll to view all questions.")
            else:
                st.markdown("Each row represents a single question, showing the distribution of responses. Scroll to view all questions.")
        
        # Build heatmap data for all questions
        question_heatmap_data = []
        
        # Wrap text helper function
        def wrap_text(text, max_len=60):
            """Wrap text at word boundaries"""
            words = text.split()
            lines = []
            current_line = []
            current_length = 0
            
            for word in words:
                if current_length + len(word) + 1 <= max_len:
                    current_line.append(word)
                    current_length += len(word) + 1
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
                    current_length = len(word)
            
            if current_line:
                lines.append(' '.join(current_line))
            
            return '<br>'.join(lines)
        
        for question in selected_questions:
            question_responses = filtered_df[question].dropna()
            grouped_question = group_responses(question_responses, group_responses_mode, exclude_dont_know)
            
            if not grouped_question.empty:
                dist = grouped_question.value_counts()
                total = len(grouped_question)
                
                wrapped_question = wrap_text(question)
                
                row_data = {
                    'Question': wrapped_question,
                    'FullQuestion': question  # Keep full question for hover
                }
                
                # Add percentage for each response type
                if group_responses_mode:
                    if exclude_dont_know:
                        col_order = ['Positive', 'Negative']
                    else:
                        col_order = ['Positive', "Don't Know", 'Negative']
                else:
                    if exclude_dont_know:
                        col_order = ['Strongly Agree', 'Agree', 'Disagree', 'Strongly Disagree']
                    else:
                        col_order = ['Strongly Agree', 'Agree', "Don't Know", 'Disagree', 'Strongly Disagree']
                
                for resp_type in col_order:
                    row_data[resp_type] = (dist.get(resp_type, 0) / total * 100) if total > 0 else 0
                
                question_heatmap_data.append(row_data)
        
        if question_heatmap_data:
            q_heatmap_df = pd.DataFrame(question_heatmap_data)
            
            # Extract full questions before setting index
            full_questions = q_heatmap_df['FullQuestion'].tolist()
            
            # Set index and remove FullQuestion column from display
            q_heatmap_df = q_heatmap_df.set_index('Question')
            q_heatmap_df = q_heatmap_df.drop(columns=['FullQuestion'])
            
            # Reorder columns
            if group_responses_mode:
                if exclude_dont_know:
                    col_order = ['Positive', 'Negative']
                else:
                    col_order = ['Positive', "Don't Know", 'Negative']
            else:
                if exclude_dont_know:
                    col_order = ['Strongly Agree', 'Agree', 'Disagree', 'Strongly Disagree']
                else:
                    col_order = ['Strongly Agree', 'Agree', "Don't Know", 'Disagree', 'Strongly Disagree']
            
            q_heatmap_df = q_heatmap_df[[col for col in col_order if col in q_heatmap_df.columns]]
            
            # Sort if a sort option is selected
            if sort_by != 'None' and sort_by in q_heatmap_df.columns:
                # Create a temporary dataframe with full questions for reordering
                temp_df = q_heatmap_df.copy()
                temp_df['FullQuestion'] = full_questions
                temp_df = temp_df.sort_values(by=sort_by, ascending=sort_ascending)
                
                # Extract sorted full questions and drop the column
                full_questions = temp_df['FullQuestion'].tolist()
                q_heatmap_df = temp_df.drop(columns=['FullQuestion'])
            
            # Create custom hover text with full questions
            hover_text = []
            for idx, full_q in enumerate(full_questions):
                row_hover = []
                for col in q_heatmap_df.columns:
                    hover_val = q_heatmap_df.iloc[idx][col]
                    hover_str = f"<b>Question:</b><br>{full_q}<br><br><b>Response:</b> {col}<br><b>Percentage:</b> {hover_val:.1f}%"
                    row_hover.append(hover_str)
                hover_text.append(row_hover)
            
            fig = go.Figure(data=go.Heatmap(
                z=q_heatmap_df.values,
                x=q_heatmap_df.columns,
                y=q_heatmap_df.index,
                colorscale='RdYlGn',
                text=q_heatmap_df.values.round(1),
                texttemplate='%{text}%',
                textfont={"size": 11},
                hovertemplate='%{customdata}<extra></extra>',
                customdata=hover_text
            ))
            
            # Calculate height: give each question more space (50px per question minimum)
            chart_height = max(1000, len(selected_questions) * 50)
            
            fig.update_layout(
                height=chart_height,
                yaxis={
                    'tickfont': {'size': 11},
                    'tickmode': 'linear',
                    'side': 'left',
                    'title': 'Question'
                },
                margin=dict(l=400, r=50, t=100, b=100)  # More top/bottom margin for labels
            )
            
            # Configure x-axis to show on both top and bottom
            fig.update_xaxes(
                side='top',
                tickfont={'size': 11},
                title_text='Response Type',
                title_standoff=15,
                mirror='ticks',
                showticklabels=True,
                ticks='outside'
            )
            
            # Use container with specific height to enable scrolling
            st.markdown(
                """
                <style>
                .scrollable-chart {
                    height: 800px;
                    overflow-y: scroll;
                    overflow-x: hidden;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("No question data available for heatmap.")
    
    with tab2:
        # Detailed question-by-question analysis
        st.subheader("Detailed Question Analysis")
        st.markdown("Explore each question individually with response breakdowns by department and tenure.")
        
        # Search functionality for questions
        search_query_detailed = st.text_input(
            "Search questions:",
            value="",
            key="question_search_detailed",
            placeholder="Type to filter questions..."
        )
        
        # Filter questions based on search
        if search_query_detailed:
            filtered_questions_detailed = [q for q in selected_questions if search_query_detailed.lower() in q.lower()]
        else:
            filtered_questions_detailed = selected_questions
        
        # Show count of filtered questions
        if search_query_detailed:
            st.caption(f"Showing {len(filtered_questions_detailed)} of {len(selected_questions)} questions")
        
        # Question selector
        if filtered_questions_detailed:
            question_to_analyze = st.selectbox(
                "Select a question:",
                options=filtered_questions_detailed,
                key="detailed_question_selector"
            )
        else:
            st.warning("No questions match your search.")
            question_to_analyze = None
        
        if question_to_analyze:
            st.markdown(f"**Question:** {question_to_analyze}")
            st.markdown("---")
            
            # Get responses for this question
            question_data = filtered_df[question_to_analyze].dropna()
            grouped_data = group_responses(question_data, group_responses_mode, exclude_dont_know)
            
            if not grouped_data.empty:
                # Overall stats for this question
                col1, col2, col3 = st.columns(3)
                
                total_resp = len(grouped_data)
                dist = grouped_data.value_counts()
                
                with col1:
                    st.metric("Total Responses", total_resp)
                
                if group_responses_mode:
                    positive_count = dist.get('Positive', 0)
                    negative_count = dist.get('Negative', 0)
                    with col2:
                        st.metric("Positive", f"{(positive_count/total_resp*100):.1f}%", f"{positive_count} responses")
                    with col3:
                        st.metric("Negative", f"{(negative_count/total_resp*100):.1f}%", f"{negative_count} responses")
                else:
                    agree_count = dist.get('Strongly Agree', 0) + dist.get('Agree', 0)
                    disagree_count = dist.get('Strongly Disagree', 0) + dist.get('Disagree', 0)
                    with col2:
                        st.metric("Agree/Strongly Agree", f"{(agree_count/total_resp*100):.1f}%", f"{agree_count} responses")
                    with col3:
                        st.metric("Disagree/Strongly Disagree", f"{(disagree_count/total_resp*100):.1f}%", f"{disagree_count} responses")
                
                st.markdown("---")
                
                # Overall distribution
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("#### Overall Distribution")
                    dist_pct = (dist / total_resp * 100).round(1)
                    
                    # Order responses
                    if group_responses_mode:
                        if exclude_dont_know:
                            order = ['Positive', 'Negative']
                        else:
                            order = ['Positive', "Don't Know", 'Negative']
                    else:
                        if exclude_dont_know:
                            order = ['Strongly Agree', 'Agree', 'Disagree', 'Strongly Disagree']
                        else:
                            order = ['Strongly Agree', 'Agree', "Don't Know", 'Disagree', 'Strongly Disagree']
                    
                    ordered_dist = dist.reindex([o for o in order if o in dist.index])
                    ordered_dist_pct = dist_pct.reindex([o for o in order if o in dist_pct.index])
                    
                    fig = go.Figure(data=[go.Bar(
                        y=ordered_dist.index,
                        x=ordered_dist.values,
                        orientation='h',
                        text=[f"{v:.1f}%" for v in ordered_dist_pct.values],
                        textposition='auto',
                        marker_color=[color_map.get(x, '#3498db') for x in ordered_dist.index]
                    )])
                    
                    fig.update_layout(
                        xaxis_title="Number of Responses",
                        yaxis_title="Response",
                        height=300,
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig, width='stretch')
                
                with col2:
                    st.markdown("#### Response Breakdown")
                    for resp_type in ordered_dist.index:
                        count = ordered_dist[resp_type]
                        pct = ordered_dist_pct[resp_type]
                        st.markdown(f"**{resp_type}:** {count} ({pct:.1f}%)")
                
                st.markdown("---")
                
                # By Department
                st.markdown("#### Breakdown by Department")
                
                dept_question_data = []
                for dept in selected_departments:
                    dept_responses = filtered_df[filtered_df['Department'] == dept][question_to_analyze].dropna()
                    grouped_dept = group_responses(dept_responses, group_responses_mode, exclude_dont_know)
                    
                    if not grouped_dept.empty:
                        dept_dist = grouped_dept.value_counts()
                        dept_total = len(grouped_dept)
                        
                        for resp_type, count in dept_dist.items():
                            dept_question_data.append({
                                'Department': dept,
                                'Response': resp_type,
                                'Count': count,
                                'Percentage': (count / dept_total * 100) if dept_total > 0 else 0
                            })
                
                if dept_question_data:
                    dept_q_df = pd.DataFrame(dept_question_data)
                    
                    fig = px.bar(
                        dept_q_df,
                        x='Department',
                        y='Percentage',
                        color='Response',
                        barmode='group',
                        category_orders={'Response': [c for c in order if c in dept_q_df['Response'].unique()]},
                        color_discrete_map=color_map,
                        hover_data=['Count'],
                        text='Percentage'
                    )
                    
                    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                    
                    fig.update_layout(
                        xaxis_title="Department",
                        yaxis_title="Percentage (%)",
                        height=400
                    )
                    
                    st.plotly_chart(fig, width='stretch')
                else:
                    st.info("No department data available for this question.")
                
                st.markdown("---")
                
                # By Tenure
                st.markdown("#### Breakdown by Tenure")
                
                tenure_question_data = []
                for tenure in selected_tenure:
                    tenure_responses = filtered_df[filtered_df['Tenure'] == tenure][question_to_analyze].dropna()
                    grouped_tenure = group_responses(tenure_responses, group_responses_mode, exclude_dont_know)
                    
                    if not grouped_tenure.empty:
                        tenure_dist = grouped_tenure.value_counts()
                        tenure_total = len(grouped_tenure)
                        
                        for resp_type, count in tenure_dist.items():
                            tenure_question_data.append({
                                'Tenure': tenure,
                                'Response': resp_type,
                                'Count': count,
                                'Percentage': (count / tenure_total * 100) if tenure_total > 0 else 0
                            })
                
                if tenure_question_data:
                    tenure_q_df = pd.DataFrame(tenure_question_data)
                    
                    fig = px.bar(
                        tenure_q_df,
                        x='Tenure',
                        y='Percentage',
                        color='Response',
                        barmode='group',
                        category_orders={'Response': [c for c in order if c in tenure_q_df['Response'].unique()]},
                        color_discrete_map=color_map,
                        hover_data=['Count'],
                        text='Percentage'
                    )
                    
                    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                    
                    fig.update_layout(
                        xaxis_title="Tenure",
                        yaxis_title="Percentage (%)",
                        height=400
                    )
                    
                    st.plotly_chart(fig, width='stretch')
                else:
                    st.info("No tenure data available for this question.")
            else:
                st.warning("No responses available for this question with the current filters.")

if __name__ == "__main__":
    main()

