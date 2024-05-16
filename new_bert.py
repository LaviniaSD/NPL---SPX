import matplotlib.pyplot as plt
import pandas
import re

def get_date(speaker):
    # Add your code to get the dates for the speaker
    # Return the dates as a list
    with open("dates.txt", "r") as file:
        don = False
        dates = []
        for line in file.readlines():
            if speaker in line:
                don = True
            elif don:
                if "Speaker" in line:
                    break
                else:
                    dates.append(line.strip())
    # Add your code to extract only the years from the dates
    years = [re.search(r'\d{4}', date).group() for date in dates]

    return years


with open("new_bert.txt", "r") as file:
    for line in file.readlines():
        if "Speaker" in line:
            # Start your loop here
            # Add your code to process the line with "Speaker"
            # Continue the loop until the end of the file
            pos = []
            neg = []
            neu = []
            speaker = line.split(" ")[1].replace("Speaker ", "")
            dates = get_date(speaker)
        else:
            # Add your code to process the line with the scores
            # Write the scores to the new file
            scores = line.split(" ")  # Assuming scores are separated by spaces
            pos.append(float(scores[0]))
            neg.append(float(scores[1]))
            neu.append(float(scores[2]))

        # Create a figure and axis
        fig, ax = plt.subplots()

        # Plot the scores for each speaker
        ax.plot(dates, pos, label='Positive')
        ax.plot(dates, neg, label='Negative')
        ax.plot(dates, neu, label='Neutral')

        # Set the title and labels
        ax.set_title(f"Scores for Speaker {speaker}")
        ax.set_xlabel('Time')
        ax.set_ylabel('Score')

        # Add a legend
        ax.legend()

        # Save the plot with a name related to the speaker
        plt.savefig(f"/home/kalil/Documents/Fields/NPL---SPX/series/{speaker}_scores.png")