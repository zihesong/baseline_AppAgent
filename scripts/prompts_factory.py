import re
from typing import List, Union
import prompts_naive, prompts
import examples

def get_system_prompt(task_desc: str, app:str) -> str:
    return f"You are an agent that is trained to complete certain tasks on a smartphone. The task you need to complete is to {task_desc} on {app}.\n\nYou will be given a screenshot of a smartphone app. The interactive UI elements on the screenshot are labeled with numeric tags starting from 1. Do not treat the numbers on the tags as the page content. They only represents the elements that you can interact with. Only focus on the elements in the screenshot, and do not assume anything that is not shown in the screenshot."

def get_prompts(prompt_style: str, turn: str, last_act: str, user_interaction: str, image: List[str]) -> Union[str, List[str]]:
    assert prompt_style in ["normal", "naive"], f"Unknown prompt style: {prompt_style}"
    assert turn in ["decision", "QUESTION", "ACTION"], f"Unknown turn: {turn}"
    
    prompt = ""
    example_images = []
    image_list = []
    
    # Get Prompt
    if prompt_style == "naive":
        if turn == "decision":
            prompt = prompts_naive.decision_template
        elif turn == "QUESTION":
            prompt = prompts_naive.question_template
        elif turn == "ACTION":
            prompt = prompts_naive.action_template
    elif prompt_style == "normal":
        if turn == "decision":
            prompt = prompts.decision_template
            example_images = re.findall(r'<([^>]+)>', examples.decision_example)
            cleaned_example_prompt = re.sub(r'<([^>]+)>', '', examples.decision_example)
        elif turn == "QUESTION":
            prompt = prompts.question_template
            example_images = re.findall(r'<([^>]+)>', examples.question_example)
            cleaned_example_prompt = re.sub(r'<([^>]+)>', '', examples.question_example)
        elif turn == "ACTION":
            prompt = prompts.action_template
            example_images = re.findall(r'<([^>]+)>', examples.action_example)
            cleaned_example_prompt = re.sub(r'<([^>]+)>', '', examples.action_example)
        prompt = re.sub(r"<examples>", cleaned_example_prompt, prompt) 
    
    # Sub last act and interactions    
    prompt = re.sub(r"<last_act>", last_act, prompt)
    prompt = re.sub(r"<previous_interactions>", user_interaction, prompt)
    
    # Generate image list
    if example_images:
        image_list = example_images + [image]
    else:
        image_list = [image]
    
    return prompt, image_list