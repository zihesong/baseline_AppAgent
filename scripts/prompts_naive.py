decision_template = """Your past actions to proceed with this task are summarized as follows: <last_act>. 

Based on the given information, your job is to decide whether to ask the user for clarification questions or directly choose an action to interact with the smartphone. Respond in the following format:

Action: <Answer QUESTION if have questions, answer ACTION if have no questions, and answer FINISH if you believe the task is completed. You cannot output anything else in this field.>
"""


action_template = """
Your past actions to proceed with this task are summarized as follows: <last_act>. 

To interact with a smartphone, you can call the following four functions to interact with those labeled elements to control the smartphone:

1. tap(element: int)
This function is used to tap a UI element shown on the smartphone screen.
"element" is a numeric tag assigned to a UI element shown on the smartphone screen.
A simple use case can be tap(5), which taps the UI element labeled with the number 5.

2. text(text_input: str)
This function is used to insert text input in an input field/box. text_input is the string you want to insert and must be wrapped with double quotation marks. When you see a keyboard showing in the lower half of the screen, it means the input text area is ready and you can use this function to insert text.
A simple use case can be text("Hello, world!"), which inserts the string "Hello, world!" into the input area on the smartphone screen. 

3. long_press(element: int)
This function is used to long press a UI element shown on the smartphone screen. "element" is a numeric tag assigned to a UI element shown on the smartphone screen.
A simple use case can be long_press(5), which long presses the UI element labeled with the number 5.

4. swipe(element: int, direction: str, dist: str)
This function is used to swipe a UI element shown on the smartphone screen, usually a scroll view or a slide bar. "element" is a numeric tag assigned to a UI element shown on the smartphone screen. "direction" is a string that represents one of the four directions: up, down, left, right. "direction" must be wrapped with double quotation marks. "dist" determines the distance of the swipe and can be one of the three options: short, medium, long. You should choose the appropriate distance option according to your needs.
A simple use case can be swipe(21, "up", "medium"), which swipes up the UI element labeled with the number 21 for a medium distance.

Based on the given information, your job is to choose only one UI element that can make us closer to the test target. Do not treat the numbers on the tags as the page content. They only represents the elements that you can interact with. Respond in the following format:

Action: <The function call with the correct parameters to proceed with the task. If you believe the task is completed or there is nothing to be done, you should output FINISH. You cannot output anything else except a function call or FINISH in this field.>
Summary: <Briefly recap your most recent action, along with prior interactions, in one or two sentences, omitting the numeric tags.>
"""

question_template = """
Your past actions to proceed with this task are summarized as follows: <last_act>. 

Based on the given information, your job is to decide what clarification questions you should ask the user. Respond in the following format:
Action: <Use clarification(question: str) to initiate a clarification dialogue. "question" is a string that represents the question you want to ask and must be wrapped with double quotation marks.
A simple use case can be clarification("I need more information about the current task."), which asks for more information about the current task.>
"""
