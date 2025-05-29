def detect_intent(user_input: str) -> str:
    """
    Basic keyword-based intent detection for demo purposes.

    Args:
        user_input (str): The user's input message.

    Returns:
        str: One of 'support_request', 'sales_inquiry', 'recommendation', or 'greeting'
    """

    user_input = user_input.lower()

    # Keywords for intent detection
    greeting_keywords = ["hi", "hello", "hey", "good morning", "good night", "good evening"]
    support_keywords = ["help", "issue", "problem", "support", "trouble"]
    sales_keywords = ["buy", "price", "purchase", "quote", "sales"]
    recommendation_keywords = ["recommend", "suggest", "which", "best"]

    if any(word in user_input for word in greeting_keywords):
        return "greeting"
    elif any(word in user_input for word in support_keywords):
        return "support_request"
    elif any(word in user_input for word in sales_keywords):
        return "sales_inquiry"
    elif any(word in user_input for word in recommendation_keywords):
        return "recommendation"
    else:
        # Default fallback intent
        return "support_request"
