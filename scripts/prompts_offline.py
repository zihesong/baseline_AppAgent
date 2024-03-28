decision_template = """You will be given a screenshot of a smartphone app. Based on the given information, your job is to decide: based on the current screen, whether to ask questions about user intention before choosing an action. Remember our test target is to <task_description> on <app>, only focus on the elements in the screenshot, and do not assume anything that is not shown. Answer in format with the following information:
decision: <Answer true if have questions, answer false if have no questions, answer finish if you believe the task is completed.>
"""

question_template = """You will be given a screenshot of a smartphone app. You decide to ask questions about user intention before choosing an action. Based on the given information, your job is to decide what questions to ask the user. Remember our test target is to <task_description> on <app>, only focus on the elements in the screenshot, and do not assume anything that is not shown. Answer in the format with the following information:
question: <All questions you want to ask the user. Answer None if you have no question>
"""
