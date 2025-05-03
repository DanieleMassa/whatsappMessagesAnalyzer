import re
import pandas as pd
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import os

files = [f for f in os.listdir('.') if f.endswith('.txt')]

file_list = '\n'.join(f"{i + 1}: {os.path.splitext(file)[0]}" for i, file in enumerate(files))
print(file_list)

choice = int(input("Inserisci il numero corrispondente al file: "))

file = files[choice - 1].rsplit('.', 1)[0]

with open(f'{file}.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

messages = []
for line in lines:
    match = re.match(r'(\d{2}/\d{2}/\d{4}), (\d{2}:\d{2}) - (.+?): (.+)', line)
    if match:
        date, time, name, content = match.groups()
        messages.append({
            'Date': pd.to_datetime(date, format='%d/%m/%Y'),
            'Time': time,
            'Name': name,
            'Content': content
        })

df = pd.DataFrame(messages)

total_messages = len(df)
print(f"Numero totale di messaggi: {total_messages}")

messages_per_person = df['Name'].value_counts()
print("Numero di messaggi per persona:")
print(messages_per_person)

average_message_length = df['Content'].apply(len).mean()
print(f"Lunghezza media di ogni messaggio: {average_message_length:.2f} caratteri")

df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M').dt.hour
hourly_messages = df['Hour'].value_counts().sort_index()
plt.figure(figsize=(10, 5))
plt.bar(hourly_messages.index, hourly_messages.values)
plt.xlabel('Ora')
plt.ylabel('Numero di messaggi')
plt.title('Ore principali di scrittura dei messaggi')
plt.show()

# Numero totale di media inviati
total_media = df[df['Content'].str.contains(r'<Media omitted>')].shape[0]
print(f"Numero totale di media inviati: {total_media}")


# Numero di media per persona
media_per_person = df[df['Content'].str.contains(r'<Media omitted>')]['Name'].value_counts()
print("Numero di file multimediali per persona:")
print(media_per_person)

# Media dei messaggi nell'ultima settimana, mese e anno
now = pd.Timestamp.now()

# Numero di messaggi nella settimana corrente (dal lunedì alla domenica precedente)
start_of_week = now - pd.Timedelta(days=now.dayofweek + 7)
end_of_week = start_of_week + pd.Timedelta(days=6)
weekly_messages = df[(df['Date'] >= start_of_week) & (df['Date'] <= end_of_week)].shape[0]
print(f"Numero di messaggi nell'ultima settimana: {weekly_messages}")

# Numero di messaggi nel mese corrente
start_of_month = now.replace(day=1)
end_of_month = start_of_month + pd.DateOffset(months=1) - pd.Timedelta(days=1)
monthly_messages = df[(df['Date'] >= start_of_month) & (df['Date'] <= end_of_month)].shape[0]
print(f"Numero di messaggi nell'ultimo mese: {monthly_messages}")

# Numero di messaggi in ogni mese dell'ultimo anno
start_of_year = now.replace(month=1, day=1)
end_of_year = start_of_year + pd.DateOffset(years=1) - pd.Timedelta(days=1)
messages_per_month = df[(df['Date'] >= start_of_year) & (df['Date'] <= end_of_year)].groupby(df['Date'].dt.month).size()

# Stampa il numero di messaggi in ogni mese
print("Numero di messaggi in ogni mese dell'ultimo anno:")
for month, count in messages_per_month.items():
    print(f"Mese {month}: {count} messaggi")

# Grafico numero messaggi inviati ogni giorno dell'ultimo mese
messages_per_day = df[(df['Date'] >= start_of_month) & (df['Date'] <= end_of_month)].groupby(df['Date'].dt.day).size()
plt.figure(figsize=(10, 5))
plt.bar(messages_per_day.index, messages_per_day.values)
plt.xlabel('Giorno del mese')
plt.ylabel('Numero di messaggi')
plt.title('Messaggi nell\'ultimo mese (giorno per giorno)')
plt.xticks(range(1, end_of_month.day + 1))  # Set x-ticks to show all days
plt.show()

# Grafico numero di messaggi inviati ogni mese dell'ultimo anno
messages_per_month = df[(df['Date'] >= start_of_year) & (df['Date'] <= end_of_year)].groupby(df['Date'].dt.month).size()
plt.figure(figsize=(10, 5))
plt.bar(messages_per_month.index, messages_per_month.values)
plt.xlabel('Mese dell\'anno')
plt.ylabel('Numero di messaggi')
plt.title('Messaggi nell\'ultimo anno (mese per mese)')
plt.xticks(range(1, 13))  # Set x-ticks to show all months
plt.show()

# Grafico numero di messaggi inviati da ogni persona
plt.figure(figsize=(10, 5))
plt.bar(messages_per_person.index, messages_per_person.values)
plt.xlabel('Persona')
plt.ylabel('Numero di messaggi')
plt.title('Numero di messaggi per persona')
plt.xticks(rotation=45)  # Rotazione delle etichette sull'asse x per migliore leggibilità
plt.show()

# Calcolo numero di giorni attivi
def calculate_active_days(df):
    unique_dates = df['Date'].dt.date.unique()
    active_days_count = len(unique_dates)
    return active_days_count

# Calcolo e stampa il numero di giorni attivi
active_days = calculate_active_days(df)
print(f"Numero di giorni in cui la chat è stata attiva: {active_days}")

# Calcolo media di messaggi al giorno totale
if active_days > 0:
    average_messages_per_day = total_messages / active_days
    print(f"Media di messaggi al giorno (totale): {average_messages_per_day:.2f}")
else:
    print("La chat non è stata attiva per nessun giorno.")

# Calcolo media di messaggi al giorno per persona
messages_per_person = df['Name'].value_counts()
for name, count in messages_per_person.items():
    person_active_days = len(df[df['Name'] == name]['Date'].dt.date.unique())
    if person_active_days > 0:
        average_messages_per_person = count / person_active_days
        print(f"Media di messaggi al giorno per {name}: {average_messages_per_person:.2f}")
    else:
        print(f"{name} non ha inviato nessun messaggio o la chat non è stata attiva per il suo account.")