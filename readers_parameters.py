agent_bank_path = "genagents/agent_bank/populations/gss_agents/"


# Parameters
num_readers = 1
novelty_weight = 0.4
relevance_weight = 0.3
quality_weight = 1.0 - novelty_weight - relevance_weight
expectation_rubric = [
    "Independant from how much you resonate with or like the story, how similar do you find this story to the stories in the books you have read?",
    "Independant from how much you resonate with or like the story, based on all the books you have read before, how similar do you find the characters in the story to characters from other books?",
    "Independant from how much you resonate with or like the story, based on all the books you have read before, to what extent can you predict the ending of the story?"
]
relevance_rubric = [
    "How much do you enjoy this book you just read based on your personal life experience?", 
    "How much do you resonate with this book you just read based on your personal life experience?"
]
quality_rubric = [
    "Independent from your personality or background, and independent from whether you like the story or not, ONLY based on the text of the story you saw, how coherent do you think the plot is? Be critical.",
    "Independent from your personality or background, and independent from whether you like the story or not,  ONLY based on the text of the story you saw, how consistent do you think the characters are? Be critical."
]
open_ended_feedback = [
    "based on your background and personal experience, what do you like about this story?",
    "based on your background and personal experience, what do you dislike about this story?"
]

# Prompts 
reading_decision_prompt = """
You see a fiction titled {title}, with the following summary: {summary}.\n Would you be interested in reading this book? Note that you are busy and you have limited time and attention. Only books that really stand out will be worth your time.
"""
