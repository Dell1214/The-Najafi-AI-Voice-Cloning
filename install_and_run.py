!pip install --upgrade --force-reinstall numpy gradio
import os
import re
import datetime
import gradio as gr

# === CONFIG ===
OWNER_JAZZCASH = "03099648389"
OWNER_NAME = "Mujahid Hussain"
MONTHLY_AMOUNT = 800

# Save user subscription data (simple file DB)
def check_subscription(email):
    db_file = "subscriptions.txt"
    now = datetime.datetime.now()

    # If file not exists, no subscription yet
    if not os.path.exists(db_file):
        return None

    with open(db_file, "r") as f:
        for line in f:
            e, expiry = line.strip().split("|")
            if e == email:
                expiry_date = datetime.datetime.strptime(expiry, "%Y-%m-%d")
                if now < expiry_date:
                    return expiry_date
                else:
                    return None
    return None

def save_subscription(email):
    db_file = "subscriptions.txt"
    expiry_date = datetime.datetime.now() + datetime.timedelta(days=30)  # 1 month
    with open(db_file, "a") as f:
        f.write(f"{email}|{expiry_date.strftime('%Y-%m-%d')}\n")
    return expiry_date


# === Main Logic ===
def verify_access(email, token, proof):
    # Step 1: Token validity (7 days)
    issue_date = datetime.datetime.now()
    expiry_date = issue_date + datetime.timedelta(days=7)
    if not token:
        return "❌ Invalid token. Access denied."

    # Step 2: Check subscription
    current_sub = check_subscription(email)
    if current_sub:
        return f"✅ Access granted until {current_sub.strftime('%Y-%m-%d')}. 🚀 Cloning starting..."
    
    # Step 3: Check screenshot (simulate)
    if proof is None:
        return f"❌ Upload required: Payment proof of Rs.{MONTHLY_AMOUNT} sent to {OWNER_NAME} ({OWNER_JAZZCASH})"

    # Very basic check: file name or metadata must mention owner or number
    if (OWNER_NAME.lower() in proof.name.lower()) or (OWNER_JAZZCASH in proof.name):
        expiry = save_subscription(email)
        return f"✅ Payment verified. Access granted until {expiry.strftime('%Y-%m-%d')}. 🚀 Cloning starting..."
    else:
        return "❌ Payment proof invalid. Make sure screenshot shows correct number and name."


# === Gradio UI ===
with gr.Blocks() as demo:
    gr.Markdown("## 🔐 Najafi AI Voice Cloning Access")
    gr.Markdown(f"💳 Pay **Rs.{MONTHLY_AMOUNT} JazzCash** to `{OWNER_NAME}` at **{OWNER_JAZZCASH}** before access.")

    email = gr.Textbox(label="Enter your Gmail")
    token = gr.Textbox(label="Enter 1-week Token", type="password")
    proof = gr.File(label="Upload Payment Screenshot", file_types=[".png", ".jpg", ".jpeg"])

    output = gr.Textbox(label="Result")

    btn = gr.Button("Verify & Start Cloning")
    btn.click(fn=verify_access, inputs=[email, token, proof], outputs=output)

demo.launch(share=True)

# This code is valid for colab
