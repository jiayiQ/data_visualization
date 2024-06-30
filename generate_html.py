import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_excel('/Users/careyqiu/Desktop/YouGov_2024_general_election_MRP_2.xlsx', sheet_name='data-5sWjS (1)')

# Define a modern pastel color palette similar to "Chartr"
color_discrete_map = {
    'ConShare': '#8ecae6',  # Light Blue
    'LabShare': '#ffb703',  # Light Yellow
    'LibDemShare': '#fb8500',  # Light Orange
    'GreenShare': '#219ebc',  # Soft Green
    'ReformShare': '#adb5bd'  # Soft Grey
}

# Function to generate the plotly graph
def generate_graph(selected_constituencies):
    filtered_df = df[df['const'].isin(selected_constituencies)]
    melted_df = filtered_df.melt(id_vars=['const', 'area'], 
                                 value_vars=['ConShare', 'LabShare', 'LibDemShare', 'GreenShare', 'ReformShare'],
                                 var_name='Party', value_name='Vote Share')
    
    # Highlight the winning party in each constituency
    filtered_df['Winner'] = filtered_df[['ConShare', 'LabShare', 'LibDemShare', 'GreenShare', 'ReformShare']].idxmax(axis=1)
    melted_df['Winner'] = melted_df.apply(lambda row: 'Yes' if row['Party'] == filtered_df[filtered_df['const'] == row['const']]['Winner'].values[0] else 'No', axis=1)
    
    fig = px.bar(melted_df, x='area', y='Vote Share', color='Party', 
                 title='Vote Shares by Constituency',
                 color_discrete_map=color_discrete_map,
                 labels={'area': 'Constituency', 'Vote Share': 'Vote Share (%)'},
                 barmode='group',
                 hover_data={'Vote Share': ':.2f', 'Winner': False})
    
    # Update layout for better readability and aesthetics
    fig.update_layout(
        title={'x':0.5, 'xanchor': 'center', 'font': {'size': 20, 'family': 'Arial', 'color': '#023047'}},
        font=dict(family='Arial', size=14, color='#023047'),
        plot_bgcolor='#f9f9f9',
        paper_bgcolor='#f9f9f9',
        hovermode='closest',
        xaxis_tickangle=-45,  # Rotate x-axis labels for better readability
        margin=dict(l=40, r=40, t=40, b=40),  # Add some margin for better layout
        legend_title_text='Party',
        legend=dict(font=dict(family='Arial', size=12, color='#023047'))
    )
    
    # Add annotations for the winning party
    for i, row in filtered_df.iterrows():
        winner = row['Winner']
        winner_vote_share = row[winner]
        winner_party = winner.replace('Share', '')
        fig.add_annotation(
            x=row['area'],
            y=winner_vote_share,
            text=f"{winner_party} Wins",
            showarrow=True,
            arrowhead=2,
            ax=-30,
            ay=-30,
            bgcolor="#fff",  # White background for annotation
            opacity=0.7
        )
    
    return fig

# Select some constituencies to display
selected_constituencies = df['const'].unique()[:5]
fig = generate_graph(selected_constituencies)

# Save the figure as an HTML file
fig.write_html("plot.html")

