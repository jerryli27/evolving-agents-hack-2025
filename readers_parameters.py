agent_bank_path = "genagents/agent_bank/populations/gss_agents/"


# Parameters
num_readers = 10
novelty_weight = 0.3
relevance_weight = 0.3
expectation_rubric = [
    "How similar do you find this story to the stories in the books you have read?",
    "Based on all the books you have read before, to what extent can you predict the plot progression in this story?",
    "Based on all the books you have read before, how steoretypical do you find the characters in the story?",
    "Based on all the books you have read before, how expected do you find the ending of the story?"
]
relevance_rubric = [
    "how much do you enjoy this book you just read based on your personal life experience?", 
    "how much do you resonate with this book you just read based on your personal life experience?"
]
quality_rubric = [
    "how cohenrent do you think the plot is?",
    "how consistent do you think the characters are?"
]
open_ended_feedback = [
    "based on your background and personal experience, what do you like about this story?",
    "based on your background and personal experience, what do you dislike about this story?"
]

# Prompts 
reading_decision_prompt = """
You see a fiction titled {title}, with the following summary: {summary}.\n Would you be interested in reading this book?
"""
