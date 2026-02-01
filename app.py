import gradio as gr

# ----------------------
# Dummy in-memory database
users = []
jobs = []
reviews = []

# ----------------------
# Helper functions
def register_user(user_id, name, skills):
    if any(u['id'] == user_id for u in users):
        return f"User ID {user_id} already exists!"
    users.append({"id": user_id, "name": name, "skills": skills.split(","), "balance":0})
    return f"User {name} registered successfully!"

def post_job(job_id, title, skill_required, salary):
    if any(j['id'] == job_id for j in jobs):
        return f"Job ID {job_id} already exists!"
    jobs.append({"id": job_id, "title": title, "skill_required": skill_required, "salary": salary})
    return f"Job '{title}' posted successfully!"

def match_jobs(user_id):
    user = next((u for u in users if u['id'] == int(user_id)), None)
    if not user:
        return "User not found"
    matched = [job["title"] for job in jobs if job["skill_required"] in user["skills"]]
    return matched if matched else "No jobs matched"

def post_review(user_id, reviewer_name, rating, comment):
    reviews.append({"user_id": user_id, "reviewer": reviewer_name, "rating": rating, "comment": comment})
    return f"Review posted for User ID {user_id}!"

def get_reviews(user_id):
    user_reviews = [r for r in reviews if r['user_id'] == user_id]
    if not user_reviews:
        return "No reviews yet."
    return "\n".join([f"{r['reviewer']} rated {r['rating']}/5: {r['comment']}" for r in user_reviews])

def pay_user(user_id, amount):
    user = next((u for u in users if u['id'] == int(user_id)), None)
    if not user:
        return "User not found"
    user['balance'] += amount
    return f"Payment of {amount} RWF successful! Current balance: {user['balance']} RWF"

# ----------------------
# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## Smart Gig Platform Advanced MVP")

    with gr.Tab("Register User"):
        user_id_input = gr.Number(label="User ID")
        user_name_input = gr.Textbox(label="Name")
        user_skills_input = gr.Textbox(label="Skills (comma separated)")
        register_btn = gr.Button("Register")
        register_output = gr.Textbox(label="Output")
        register_btn.click(register_user, 
                           inputs=[user_id_input, user_name_input, user_skills_input],
                           outputs=register_output)

    with gr.Tab("Post Job"):
        job_id_input = gr.Number(label="Job ID")
        job_title_input = gr.Textbox(label="Job Title")
        job_skill_input = gr.Textbox(label="Required Skill")
        job_salary_input = gr.Number(label="Salary")
        post_btn = gr.Button("Post Job")
        post_output = gr.Textbox(label="Output")
        post_btn.click(post_job,
                       inputs=[job_id_input, job_title_input, job_skill_input, job_salary_input],
                       outputs=post_output)

    with gr.Tab("Match Jobs"):
        match_user_id_input = gr.Number(label="User ID")
        match_output = gr.Textbox(label="Matched Jobs")
        match_btn = gr.Button("Find Jobs")
        match_btn.click(match_jobs, inputs=[match_user_id_input], outputs=match_output)

    with gr.Tab("Reviews"):
        review_user_id_input = gr.Number(label="User ID")
        reviewer_name_input = gr.Textbox(label="Reviewer Name")
        rating_input = gr.Number(label="Rating (1-5)")
        comment_input = gr.Textbox(label="Comment")
        review_btn = gr.Button("Post Review")
        review_output = gr.Textbox(label="Output")
        review_btn.click(post_review,
                         inputs=[review_user_id_input, reviewer_name_input, rating_input, comment_input],
                         outputs=review_output)

        get_reviews_user_id_input = gr.Number(label="User ID to See Reviews")
        get_reviews_output = gr.Textbox(label="Reviews")
        get_reviews_btn = gr.Button("Get Reviews")
        get_reviews_btn.click(get_reviews, inputs=[get_reviews_user_id_input], outputs=get_reviews_output)

    with gr.Tab("Payment"):
        pay_user_id_input = gr.Number(label="User ID")
        pay_amount_input = gr.Number(label="Amount (RWF)")
        pay_btn = gr.Button("Pay User")
        pay_output = gr.Textbox(label="Output")
        pay_btn.click(pay_user, inputs=[pay_user_id_input, pay_amount_input], outputs=pay_output)

# ----------------------
demo.launch()
