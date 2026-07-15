
def human_approval_node(state):

    plan = state["plan"]

    print("\n========== IMPLEMENTATION PLAN ==========\n")
    print(plan)

    while True:

        answer = input("\nApprove this plan? (yes/no): ").strip().lower()

        if answer in ["yes", "y"]:
            state["approved"] = True
            state["human_feedback"] = ""
            break

        elif answer in ["no", "n"]:
            state["approved"] = False
            
            feedback = input("\nHow should the plan be changed?\n> ")

            state["human_feedback"] = feedback
            break

        else:
            print("Please enter yes or no")

    return state
            