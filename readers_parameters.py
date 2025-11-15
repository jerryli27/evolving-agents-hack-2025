agent_bank_path = "genagents/agent_bank/populations/gss_agents/"


# Parameters
num_readers = 5
novelty_weight = 0.4
relevance_weight = 0.3
quality_weight = 1.0 - novelty_weight - relevance_weight
expectation_rubric = [
    "This question should be answered independantly from how much you resonate with or like the story. How similar do you find this story to the stories you have read or watched before?",
#    "Independant from how much you resonate with or like the story, based on all the stories you have seen before, how similar do you find the characters in the story to characters from other stories?",
#    "Independant from how much you resonate with or like the story, based on all the books you have read before, to what extent can you predict the ending of the story?"
]
relevance_rubric = [
    "How much do you enjoy this episode you just watched based on your personal life experience?", 
    "How much do you resonate with this episode you just watched based on your personal life experience?"
]
quality_rubric = [
    "Independent from your personality or background, and independent from whether you like the story or not, ONLY based on the text describing the episode you just saw, how coherent do you think the plot is? Be critical.",
    "Independent from your personality or background, and independent from whether you like the story or not, how consistent do you think the characters are with them in the previous episode? Be critical."
]
open_ended_feedback = [
    "based on your background and personal experience, what do you like about this story so far?",
    "based on your background and personal experience, what do you dislike about this story so far?"
    "based on your background and personal experience, what would you like to see in the next episode?",
    "based on your background and personal experience, what would you not want to see in the next episode?"
]

# Prompts 
reading_decision_prompt = """
You just got off work. You are tierd and relaxing on the couch. You are scrolling through a list of short drama episode to watch. You saw episode {timestep} of the series {title}. The full story of {title} is summaeized as: {full_story_summary}.
This episode presents the following plot: {summary}.
Would you be interested to watch? Note that you are busy and you have limited time and attention. Only shows that really stand out will be worth your time. 
"""

plot_prediction_prompt = "What do you expect to happen in the next episode?"

prediction_alignment_prompt = "The following is the summary of the story in an episode of a short drama: {actual_story}.\n The following is how the audience expect to happen in this episode: {prediction}. How much does the actual story fall into the audience's anticipation? Answer with an integer number between 1 an 10 (inclusive), with 1 being completely not falling into anticipation and 10 being completely anticpated. Output the number ONLY!"

qualitative_feedback_aggregation_prompt = "Summarize the following feedback for an episode from a show. The feedback are from different audience so they might repeat or contradict with each other. Summarize them into a bullet list that represent the clustered themes of opinions from the audience and capture the significant patterns.\n {all_feedback}"

prediction_aggregation_prompt = "Summarize the following prediction for the next episode of a show into a bullet list. Capture all the predictions. \n {all_prediction}"