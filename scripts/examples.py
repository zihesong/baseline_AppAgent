self_explore_task_example = """
[Example 1]
Current task is to delete Dallas from favorite list on AccuWeather. Previously we have asked clarification and known that user refer Dallas, Georgia as Dallas. We successfully navigate to edit favourites page. Given the screenshot, I have seen a Remove button next to the Dallas, Georgia. However, since removing an entry from favorite can be hard to recover, I should ask for user to confirm the action. Therefore, I should generate QUESTION action.
<scripts/example_images/accuweather_delete_favorites.png>

[Example 2]
Current task is to delete 9:00 AM clock on Clock. Given the screenshot, the components are actually for creating a new alarm. This is happenning because previously we have navigated to the wrong page. Therefore, in this case, even though you are unsure about what to do the current step. You should not ask question given the current situation. Because user intent are clear and the question can only ask to clarify user intent instead of asking about UI navigation question. Therefore, I should generate ACTION action.
<scripts/example_images/clock_delete_navigation.png>

[Example 3]
Current task is to delete Dallas from favorite list on AccuWeather. Previously we have asked confirmation from user that he confirms the action even though we have informed him/her with possible outcome. Given the screenshot, I have seen multiple entries names next to UI component 4 and 7. They are Dallas, Georgia and Dallas, Oregon. Thus, I should ask for user to provide more detailed information about clarifying user's intent on which Dallas he/she is referring to. Therefore, I should generate QUESTION action.
<scripts/example_images/accuweather_delete_multiple.png>

[Example 4]
Current task is to delete a 9:00 AM clock on Clock. Previously we have asked confirmation from user that he/she confirms the action even though we have informed him/her with possible outcome. Given the screenshot, it shows two 9:00 AM clocks next to UI component 7 and 10. To make sure I understant which one he/she is referring to, I need to ask for clarification. Therefore, I should generate QUESTION action.
<scripts/example_images/clock_delete_multiple.png>

"""
self_explore_task_example_image = "/examples/self_explore_task_example.png"

self_explore_task_action_example = """"""

self_explore_task_question_example = """
Example 1: User wants to delete London from favorite list on weather app. However, since delete action can be considered irreversible, even though we can add it back to the favorite list later on, but to avoid any potential misunderstanding, we should ask for user to confirm the action. Therefore, I should generate CONFIRMATION action.

Example 2: User wants to add London to favorite list on weather app. However, the user did not specify which London he/she is referring to. In this case, we should not assume that user means London, UK. We should ask for user to provide more detailed information. Therefore, I should generate CLARIFICATION action.

Example 3: User wants to search for highest-rating restaurant near him/her. Even though he/she provides clear intention, the application itself does not activate location service, thus the application will not know user's current location. We need to ask user how to solve this problem that stopped us from achieveing what he/she instructs. Therefore, I should generate CLARIFICATION action.
"""