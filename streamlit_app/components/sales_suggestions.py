import streamlit as st

def show_sales_suggestions(user_query: str):
    st.subheader("💼 Sales Suggestions")

    # Very basic keyword-based suggestions
    if "price" in user_query.lower():
        return st.markdown("""
        - ✅ **We offer competitive pricing with seasonal discounts.**
        - 💰 **Bundle deals** are available if you buy multiple items.
        - 📅 Keep an eye on our **flash sales** every Friday!
        """)
    elif "discount" in user_query.lower() or "offer" in user_query.lower():
        return st.markdown("""
        - 🎉 **New users** get a 10% discount on their first purchase!
        - 🏷️ **Festive offers** are live now with up to 30% off.
        - 💌 Subscribe to our newsletter for **exclusive promo codes**.
        """)
    elif "feature" in user_query.lower():
        return st.markdown("""
        - 🚀 Our product comes with **AI-powered automation** features.
        - 🔒 Security-first architecture with **end-to-end encryption**.
        - 📊 Real-time dashboards with **custom analytics** support.
        """)
    else:
        return st.markdown("""
        - 📦 Get help with pricing, features, discounts, and plans!
        - 👤 Ask about custom packages for enterprise users.
        - ☎️ Want to talk to a human? We’ll help you schedule a call!
        """)
