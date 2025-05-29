import streamlit as st

def show_recommendations(user_id):
    st.subheader("🎯 AI Recommendations for You")
    recommendations = {
        "u1": [
            "Consider the Snowflake Business Tier for growing analytics teams.",
            "Enable AI-powered insights for marketing with Snowpark.",
            "Try Snowflake's free trial with 400 credits."
        ]
    }

    for i, rec in enumerate(recommendations.get(user_id, []), 1):
        st.markdown(f"**{i}.** {rec}")
