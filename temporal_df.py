import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Extract data
sizes = []
with open("sizes.txt", "r") as file:
    texto = file.readlines()
    for linha in texto:
        sizes.append(int(linha))
        
dates = []
with open("dates.txt", "r") as file:
    texto = file.readlines()
    for linha in texto:
        dates.append(linha[:-1])

emo_dict_score = []
# print(isabel_schnabel_data["date"])
with open("dict.txt", "r") as file:
    texto = file.readlines()
ite = 0
for linha in texto:
    v = linha.split(" ")
    # print(v)
    vl = [float(v[0][1:]), float(v[1]), float(v[2][:-2])]
    # print(vl)
    emo_dict_score.append(vl)

emo_bigbert_score = []
with open("old_big_bert.txt", "r") as file:
    texto = file.readlines()
ite = 0
for linha in texto:
    v = linha.split(" ")
    # print(v)
    try:
        vl = [float(v[0][1:]), float(v[1]), float(v[2][:-2])]
    except:
        print(v)
        print(v[0][2:])
        print(v[1])
        print(v[2][:-2])
        raise
    # print(vl)
    emo_bigbert_score.append(vl)

emo_bert_score = []
with open("bert.txt", "r") as file:
    texto = file.readlines()
ite = 0
for linha in texto:
    v = linha.split(" ")
    # print(v)
    vl = [float(v[0][1:])*sizes[ite]/10, float(v[1])*sizes[ite]/10, float(v[2][:-2])*sizes[ite]/10]
    # print(vl)
    emo_bert_score.append(vl)
    ite += 1

# emo_cumu_score = []
# for i in range(len(emo_dict_score)):
#     emo_cumu_score.append([emo_dict_score[i][0] + emo_bigbert_score[i][0], emo_dict_score[i][1] + emo_bigbert_score[i][1], emo_dict_score[i][2] + emo_bigbert_score[i][2]])

# Create a dictionary with the data
data = {
    'dates': dates[:55],
    'sizes': sizes[:55],
    'emo_dict_score': emo_dict_score[:55],
    'emo_bigbert_score': emo_bigbert_score[:55],
    'emo_bert_score': emo_bert_score[:55]
    # 'emo_cumu_score': emo_cumu_score[:55]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Divide each list by its norm
df['emo_dict_score'] = [i/np.linalg.norm(i) for i in df['emo_dict_score']]
df['emo_bigbert_score'] = [i/np.linalg.norm(i) for i in df['emo_bigbert_score']]
df['emo_bert_score'] = [i/np.linalg.norm(i) for i in df['emo_bert_score']]
# df['emo_cumu_score'] = [i/np.linalg.norm(i) for i in df['emo_cumu_score']]

emo_cumu_score = []
for i in range(len(emo_dict_score)):
    emo_cumu_score.append(df['emo_bigbert_score'][i] + df['emo_dict_score'][i])

df['emo_cumu_score'] = emo_cumu_score
df['emo_cumu_score'] = [i/np.linalg.norm(i) for i in df['emo_cumu_score']]


# Print the DataFrame
# print(df['emo_bert_score'][0])

df.to_csv("temporal_df.csv", index=False)

temporal_df = df.sort_values(by='dates')
print(temporal_df)

emo_bert = []
emo_bigbert = []
emo_dict = []
emo_cumu = []

for i in range(len(temporal_df)):
    score = temporal_df['emo_bert_score'][i]
    if float(score[0]) > float(score[1]) and float(score[0]) > float(score[2]):
        emo_bert.append('positive')
    elif float(score[1]) > float(score[0]) and float(score[1]) > float(score[2]):
        emo_bert.append('negative')
    else:
        emo_bert.append('neutral')
    
    score = temporal_df['emo_bigbert_score'][i]
    if float(score[0]) > float(score[1]) and float(score[0]) > float(score[2]):
        emo_bigbert.append('positive')
    elif float(score[1]) > float(score[0]) and float(score[1]) > float(score[2]):
        emo_bigbert.append('negative')
    else:
        emo_bigbert.append('neutral')
    
    score = temporal_df['emo_dict_score'][i]
    if float(score[0]) > float(score[1]) and float(score[0]) > float(score[2]):
        emo_dict.append('positive')
    elif float(score[1]) > float(score[0]) and float(score[1]) > float(score[2]):
        emo_dict.append('negative')
    else:
        emo_dict.append('neutral')
    
    score = temporal_df['emo_cumu_score'][i]
    if float(score[0]) > float(score[1]) and float(score[0]) > float(score[2]):
        emo_cumu.append('positive')
    elif float(score[1]) > float(score[0]) and float(score[1]) > float(score[2]):
        emo_cumu.append('negative')
    else:
        emo_cumu.append('neutral')

print(emo_bert)
fig, axs = plt.subplots(2, 2, figsize=(10, 8), sharex=True, sharey=True)

# plt.yticks(['positive', 'neutral', 'negative'])

axs[0, 0].plot(dates, emo_bert)
axs[0, 0].set_title('Emo Bert')

axs[0, 1].plot(dates, emo_bigbert)
axs[0, 1].set_title('Emo Bigbert')

axs[1, 0].plot(dates, emo_dict)
axs[1, 0].set_title('Emo Dict')

axs[1, 1].plot(dates, emo_cumu)
axs[1, 1].set_title('Emo Cumu')

plt.tight_layout()
plt.xticks('')
plt.savefig('temporal.png')
plt.show()