import streamlit as st
import openai

# --- Set Your OpenAI API Key ---
openai.api_key = "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"  # Replace with your OpenAI API key

# --- All Questions and Markschemes ---
questions = [
    {
        "text": """
        ### 🧮 Question 1: Annuity Calculation

        Daniel invests in an annuity fund at 4.5% per year, compounded monthly. He withdraws $3600 monthly.

        **Tasks:**
        - (a) Find the value after 5 years. _(3 marks)_
        - (b) Calculate how many times Daniel can make these withdrawals. _(3 marks)_

        **Include:**
        - GDC inputs (N, I%, PV, PMT, FV, P/Y, C/Y)
        - Clear explanation of your steps and final answer
        """,
        "markscheme": """
        (a) N = 60, I% = 4.5, PV = 400000, PMT = -3600, FV = 259000, P/Y = 12, C/Y = 12
        Final FV should be $259,000.
        (b) N = 144 (FV = 0 means 144 withdrawals)
        """
    },
    {
        "text": """
        ### 🐶 Question 2: Dog Food Arithmetic Sequence

        Scott's bag had 115.5 cups on day 3 and 108 cups on day 8.

        **Tasks:**
        - (a.i) Find cups fed per day. _(3 marks)_
        - (a.ii) Find remaining cups after day 1. _(1 mark)_
        - (b) Calculate how many days the bag lasts. _(2 marks)_
        - (c) Find 2025 cost if 2021 cost was $625 and rises by 6.4% per year. _(3 marks)_
        - (d.i) Calculate total cost over 10 years. _(1 mark)_
        - (d.ii) Explain what this value represents. _(2 marks)_
        - (e) Comment on geometric model appropriateness. _(1 mark)_
        """,
        "markscheme": """
        (a.i) 1.5 cups/day
        (a.ii) 118.5 cups
        (b) 80 days
        (c) $801 in 2025
        (d.i) $8390 total
        (d.ii) Total cost over 10 years
        (e) Accepts model limitations or validity with inflation, discrete quantities
        """
    },
    {
        "text": """
        ### 🏠 Question 3: Home Loan Calculation

        Tiffany buys a house for $285,000 with a 15% down payment.

        **Tasks:**
        - (a.i) Find the loan amount. _(2 marks)_
        - (a.ii) Calculate monthly payment over 30 years at 4%. _(3 marks)_
        - (b) Find total repayment. _(2 marks)_
        - (c) If she pays $1300/month, how many months to repay? _(2 marks)_
        - (d) Calculate the final payment. _(4 marks)_
        - (e) Calculate total savings. _(3 marks)_

        **Include:**
        - GDC inputs (N, I%, PV, PMT, FV, P/Y, C/Y)
        - Clear explanation of your steps and final answer
        """,
        "markscheme": """
        (a.i) $242,250
        (a.ii) $1156.54/month
        (b) $416,354 total
        (c) 292 months
        (d) $874.82 final payment
        (e) $37,180 saved
        """
    }
]

# --- Streamlit Layout ---
st.title("📊 Chapter 1 revision")

# --- Readable, styled instructions using HTML ---
st.markdown("""
<div style="
    background-color: #ffffff;
    padding: 1.5rem;
    border-radius: 8px;
    border: 1px solid #cccccc;
    color: #000000;
    font-size: 17px;
    line-height: 1.6;
">
    <strong>✅ Instructions:</strong><br>
    • Use <strong>exact values</strong> (fractions, π) where appropriate.<br>
    • Round decimal answers to <strong>3 significant figures</strong>, unless stated otherwise.<br>
    • Clearly show all <strong>GDC inputs</strong> (N, I%, PV, PMT, FV, P/Y, C/Y).<br>
    • <strong>Explain each step</strong> in your own words to earn full marks.
</div>
""", unsafe_allow_html=True)

st.info("""
### ✅ Important Instructions:
- 📝 Leave exact values when appropriate (fractions, π, symbols).
- ➂ Round decimal answers to **3 significant figures**, unless stated otherwise.
- 🎛️ Provide **GDC inputs** and explain your calculation steps clearly.
""")

student_name = st.text_input("👤 Please enter your full name:")

if student_name.strip():
    if "responses" not in st.session_state:
        st.session_state.responses = [""] * len(questions)

    st.markdown("## 📝 Answer All Questions Below")
    st.markdown("---")

    for idx, question in enumerate(questions):
        st.markdown(question["text"])
        st.session_state.responses[idx] = st.text_area(
            f"✏️ **Your Response to Question {idx + 1}:**",
            value=st.session_state.responses[idx],
            key=f"response_{idx}"
        )
        st.markdown("---")

    if st.button("🚀 Submit All Answers for Feedback"):
        with st.spinner("Evaluating your responses..."):
            combined_feedback = f"Student Name: {student_name}\n\n"
            total_score = 0
            total_possible = 0

            for idx, question in enumerate(questions):
                evaluation_prompt = f"""
                Evaluate the student's response based on the provided markscheme.

                Question {idx + 1}:
                {question["text"]}

                Student's Response:
                {st.session_state.responses[idx]}

                Markscheme:
                {question["markscheme"]}

                Important:
                - Leave exact values when appropriate.
                - Round decimals to 3 sig figs unless otherwise stated.
                - Penalize if not followed.
                - Comment on rounding or exactness.

                Start with: "Marks Awarded: X/Y"
                """

                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": evaluation_prompt}],
                    temperature=0.4,
                    max_tokens=500
                )

                feedback_text = response.choices[0].message.content.strip()
                combined_feedback += f"### Feedback for Question {idx + 1}:\n{feedback_text}\n\n"

                try:
                    score_line = feedback_text.splitlines()[0]
                    marks_awarded, marks_total = map(int, score_line.replace("Marks Awarded:", "").strip().split("/"))
                    total_score += marks_awarded
                    total_possible += marks_total
                except Exception:
                    pass

            st.balloons()
            st.success(f"🎉 Congratulations {student_name}! You scored {total_score}/{total_possible}.")
            with st.expander("📄 Click here to view your detailed feedback"):
                st.markdown(combined_feedback.replace("\n", "\n\n"))

else:
    st.warning("👋 Please enter your name to begin the assessment.")
