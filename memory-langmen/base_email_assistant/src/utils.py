from typing import Dict
# from models import Email
from prompts import template

profile = {
    "name": "Junaid",
    "full_name": "Muhammad Junaid Shaukat",
    "user_profile_background": "AI Products Manager Building My AI Agents Workforce.",
}



prompt_instructions = {
    "triage_rules": {
        "ignore": "Marketing newsletters, spam emails, mass company announcements",
        "notify": "Team member out sick, build system notifications, project status updates",
        "respond": "Direct questions from team members, meeting requests, critical bug reports",
    },
    "agent_instructions": "Use these tools when appropriate to help manage Junaid's tasks efficiently."
}


# Example incoming email

# Example incoming email
email = {
    "from": "Alice Smith ",
    "to": "Muhammad Junaid Shaukat",
    "subject": "Quick question about API documentation",
    "body": """
Hi Junaid,

I was reviewing the API documentation for the new authentication service and noticed a few endpoints seem to be missing from the specs. Could you help clarify if this was intentional or if we should update the docs?

Specifically, I'm looking at:
- /auth/refresh
- /auth/validate

Thanks!
Alice""",
}

# email_input = {
#     "from": "Marketing Team <marketing@amazingdeals.com>",
#     "to": "John Doe <john.doe@company.com>",
#     "subject": "🔥 EXCLUSIVE OFFER: Limited Time Discount on Developer Tools! 🔥",
#     "body": """Dear Valued Developer,

# Don't miss out on this INCREDIBLE opportunity!

# 🚀 For a LIMITED TIME ONLY, get 80% OFF on our Premium Developer Suite!

# ✨ FEATURES:
# - Revolutionary AI-powered code completion
# - Cloud-based development environment
# - 24/7 customer support
# - And much more!

# 💰 Regular Price: $999/month
# 🎉 YOUR SPECIAL PRICE: Just $199/month!

# 🕒 Hurry! This offer expires in:
# 24 HOURS ONLY!

# Click here to claim your discount: https://amazingdeals.com/special-offer

# Best regards,
# Marketing Team
# ---
# To unsubscribe, click here
# """,
# }

# # typed_email2 = Email(**email_input)

email_input = {
    "from": "Marketing Team ",
    "to": "Muhammad Junaid Shaukat",
    "subject": "🔥 EXCLUSIVE OFFER: Limited Time Discount on Developer Tools! 🔥",
    "body": """Dear Valued Developer,

Don't miss out on this INCREDIBLE opportunity!

🚀 For a LIMITED TIME ONLY, get 80% OFF on our Premium Developer Suite!

✨ FEATURES:
- Revolutionary AI-powered code completion
- Cloud-based development environment
- 24/7 customer support
- And much more!

💰 Regular Price: 🎉
199/month!

🕒 Hurry! This offer expires in:
24 HOURS ONLY!

Click here to claim your discount: https://amazingdeals.com/special-offer

Best regards,
Marketing Team
---
To unsubscribe, click here
""",
}


def create_prompt(template: str, variables: Dict[str, any]) -> str:
    """Creates a prompt using an f-string and a dictionary of variables."""
    try:
        return template.format(**variables)
    except KeyError as e:
        return f"Error: Missing variable '{e.args[0]}' in the provided dictionary."
    

# Format list of few shots
def format_few_shot_examples(examples):
    print(examples)
    strs = ["Here are some previous examples:"]
    for eg in examples:
        email_data = eg.value.get("email", {})
        subject = email_data.get("subject", "No Subject")
        to_email = email_data.get("to", "No Recipient")
        from_email = email_data.get("author") or email_data.get("from", "No Sender")
        # Use 'email_thread' if available; otherwise fall back to 'body'
        content = email_data.get("email_thread") or email_data.get("body", "")
        # Truncate the content to a maximum of 400 characters
        content = content[:400]
        result = eg.value.get("label", "No Label")

        strs.append(
            template.format(
                subject=subject,
                to_email=to_email,
                from_email=from_email,
                content=content,
                result=result,
            )
        )
    return "\n\n------------\n\n".join(strs)