import streamlit as st
import random
import difflib

# ------------------------- CUSTOM PAGE CONFIGURATION -------------------------
st.set_page_config(
    page_title="German Sentence Trainer",
    page_icon="🇩🇪",
    layout="centered"
)

# ------------------------- CUSTOM STYLING -------------------------
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    .stTextArea textarea { font-size: 18px; }
    .stButton>button { font-size: 18px; color: white; background-color: #3366cc; border-radius: 5px; padding: 10px 20px; }
    .stButton>button:hover { background-color: #254a99; }
    .correct { background-color: #d4edda; padding: 10px; border-radius: 5px; }
    .incorrect { background-color: #f8d7da; padding: 10px; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# ------------------------- PAGE TITLE -------------------------
st.title("🇩🇪 German Sentence Trainer")
st.subheader("By Learn Language Education Academy")
st.markdown("Practice building correct German sentences and receive instant feedback!")

# ------------------------- CATEGORY CHOICE -------------------------
sentence_types = [
    "Statement",
    "Modal Verb Statement",
    "Separable Verb",
    "Yes/No Question",
    "W-Question",
    "Connector Sentence"
]

sentence_type = st.selectbox("Choose a sentence type to practice:", sentence_types)

# ------------------------- FORMALITY CHOICE -------------------------
formality = "Either"
if sentence_type in ["Yes/No Question", "W-Question"]:
    formality = st.radio("Select formality:", ["Informal (du)", "Formal (Sie)", "Either"])

# ------------------------- PHRASE BANK -------------------------
category_prompts = {
    "Statement": {
        "Translate: I am learning German.": ["Ich lerne Deutsch."],
        "Translate: We are going to the cinema today.": ["Wir gehen heute ins Kino."],
        "Translate: My brother plays football.": ["Mein Bruder spielt Fußball."],
        "Translate: I drink coffee every morning.": ["Ich trinke jeden Morgen Kaffee."],
        "Translate: She works in an office.": ["Sie arbeitet in einem Büro."]
    },
    "Modal Verb Statement": {
        "Translate: I can swim well.": ["Ich kann gut schwimmen."],
        "Translate: We must get up early tomorrow.": ["Wir müssen morgen früh aufstehen."],
        "Translate: He wants to buy a new car.": ["Er möchte ein neues Auto kaufen.", "Er will ein Auto kaufen."],
        "Translate: Can you help me? (informal)": ["Kannst du mir helfen?"],
        "Translate: She may not park here.": ["Sie darf hier nicht parken."]
    },
    "Separable Verb": {
        "Translate: I get up every day at six o’clock.": ["Ich stehe jeden Tag um sechs Uhr auf."],
        "Translate: He calls his girlfriend.": ["Er ruft seine Freundin an."],
        "Translate: We shop at the supermarket.": ["Wir kaufen im Supermarkt ein."],
        "Translate: She opens the door.": ["Sie macht die Tür auf."],
        "Translate: Are you coming along this evening?": ["Kommst du heute Abend mit?"]
    },
    "Yes/No Question": {
        "Translate: Are you from Germany?": ["Kommst du aus Deutschland?", "Kommen Sie aus Deutschland?"],
        "Translate: Do you have time tomorrow?": ["Hast du morgen Zeit?", "Haben Sie morgen Zeit?"],
        "Translate: Do you like eating pizza?": ["Isst du gern Pizza?", "Essen Sie gern Pizza?"],
        "Translate: Are you learning English?": ["Lernst du Englisch?", "Lernen Sie Englisch?"],
        "Translate: Do you live in Berlin?": ["Wohnt ihr in Berlin?", "Wohnen Sie in Berlin?"]
    },
    "W-Question": {
        "Translate: Where do you live?": ["Wo wohnst du?", "Wo wohnen Sie?"],
        "Translate: What are you doing at the weekend?": ["Was machst du am Wochenende?", "Was machen Sie am Wochenende?"],
        "Translate: When does the course begin?": ["Wann beginnt der Kurs?"],
        "Translate: Why are you learning German?": ["Warum lernst du Deutsch?", "Warum lernen Sie Deutsch?"],
        "Translate: What is your name?": ["Wie heißt du?", "Wie heißen Sie?"]
    },
    "Connector Sentence": {
        "Translate: It is raining heavily, therefore I stay at home. (Use deshalb)": ["Es regnet stark, deshalb bleibe ich zu Hause."],
        "Translate: I am hungry, therefore I cook something. (Use deshalb)": ["Ich habe Hunger, deshalb koche ich etwas."],
        "Translate: I would like to know if you have time tomorrow. (Use ob)": ["Ich möchte wissen, ob du morgen Zeit hast.", "Ich möchte wissen, ob Sie morgen Zeit haben."],
        "Translate: I would like to know if he speaks German. (Use ob)": ["Ich möchte wissen, ob er Deutsch spricht."],
        "Translate: I am staying at home because I am sick. (Use denn)": ["Ich bleibe zu Hause, denn ich bin krank."],
        "Translate: I cannot come because I have to work. (Use weil)": ["Ich kann nicht kommen, weil ich arbeiten muss."],
        "Translate: I eat bread and drink tea.": ["Ich esse Brot und trinke Tee."],
        "Translate: Would you like tea or coffee?": ["Möchtest du Tee oder Kaffee?", "Möchten Sie Tee oder Kaffee?"]
    }
}

# ------------------------- RANDOM PROMPTS -------------------------
type_prompts = list(category_prompts[sentence_type].keys())

if "previous_type" not in st.session_state or st.session_state.previous_type != sentence_type:
    st.session_state.progress = 0
    st.session_state.total = min(5, len(type_prompts))
    st.session_state.prompts = random.sample(type_prompts, st.session_state.total)
    st.session_state.show_next = False
    st.session_state.previous_type = sentence_type
    st.session_state.student_sentence = ""
    st.session_state.correct_answers = []
    st.session_state.wrong_answers = []

# ------------------------- DISPLAY CURRENT PROMPT -------------------------
if st.session_state.progress < st.session_state.total:
    current_prompt = st.session_state.prompts[st.session_state.progress]
    st.markdown(f"### 🔎 Prompt {st.session_state.progress + 1} of {st.session_state.total}")
    st.write(f"**{current_prompt}**")
    st.session_state.student_sentence = st.text_area(
        "✍ Type your German sentence here:",
        value=st.session_state.student_sentence,
        key=f"input_{st.session_state.progress}"
    )
else:
    st.success("🎉 You have completed all prompts for this section!")
    st.markdown(f"**✅ Correct answers:** {len(st.session_state.correct_answers)} / {st.session_state.total}")
    if st.session_state.wrong_answers:
        st.warning("Here are the ones you need to review:")
        for item in st.session_state.wrong_answers:
            st.markdown(f"- 🔄 **{item[0]}** → Correct answer: *{item[1]}*")
    st.balloons()
    if st.button("🔁 Start Again"):
        st.session_state.progress = 0
        st.session_state.prompts = random.sample(type_prompts, st.session_state.total)
        st.session_state.show_next = False
        st.session_state.student_sentence = ""
        st.session_state.correct_answers = []
        st.session_state.wrong_answers = []

def spelling_similarity(student, correct):
    return difflib.SequenceMatcher(None, student.lower(), correct.lower()).ratio()

def find_word_differences(student, correct):
    student_words = student.lower().split()
    correct_words = correct.lower().split()
    differences = []

    for word in student_words:
        if word not in correct_words:
            differences.append(word)
    return differences
# ------------------------- SUBMIT BUTTON -------------------------
if st.button("✅ Submit"):
    sentence = st.session_state.student_sentence.strip()

    if not sentence:
        st.error("❗ Please type a sentence before submitting.")
    else:
        all_possible_answers = category_prompts[sentence_type][current_prompt]

        # ----------- FORMALITY FILTER -----------
        filtered_answers = []
        for ans in all_possible_answers:
            if formality == "Informal (du)" and "Sie" not in ans:
                filtered_answers.append(ans)
            elif formality == "Formal (Sie)" and "Sie" in ans:
                filtered_answers.append(ans)
            else:
                filtered_answers.append(ans)  # Accept both if "Either" selected

        # ------------------------- CHECK FOR EXACT MATCH FIRST -------------------------
        sentence_clean = sentence.strip().lower()
        exact_match = False

        for correct in filtered_answers:
            if sentence_clean == correct.strip().lower():
                exact_match = True
                closest_answer = correct
                break

        # ------------------------- IF EXACT MATCH FOUND -------------------------
        if exact_match:
            st.success("✅ Perfect! Your sentence exactly matches one of the correct answers.")
            st.markdown(
                f"<div class='correct'>Your sentence is accepted without errors.</div>", unsafe_allow_html=True)
            st.session_state.correct_answers.append(current_prompt)

        else:
            # ------------------------- FALL BACK TO SIMILARITY CHECK -------------------------
            best_similarity = 0
            closest_answer = filtered_answers[0]

            for correct in filtered_answers:
                similarity = spelling_similarity(sentence, correct)
                if similarity > best_similarity:
                    best_similarity = similarity
                    closest_answer = correct

            if best_similarity >= 0.90:
                st.success("✅ Good! Your sentence is very close or correct.")
                st.markdown(
                    f"<div class='correct'>Your sentence matched {round(best_similarity * 100)}%.</div>",
                    unsafe_allow_html=True)
                st.session_state.correct_answers.append(current_prompt)
            else:
                st.error("❌ Your sentence has differences. See suggestions below.")
                st.markdown(
                    f"<div class='incorrect'>Closest correct answer: {closest_answer}</div>", unsafe_allow_html=True)
                st.session_state.wrong_answers.append(
                    (current_prompt, closest_answer))

                differences = find_word_differences(sentence, closest_answer)
                if differences:
                    st.write("⚠ Words that seem different or extra: " +
                             ", ".join(differences))
                else:
                    st.write("✅ No major word differences detected.")

        st.session_state.show_next = True
# ------------------------- NEXT BUTTON -------------------------
if st.session_state.show_next:
    if st.button("➡ Next"):
        st.session_state.progress += 1
        st.session_state.show_next = False
        st.session_state.student_sentence = ""  # Clear input box for next sentence
