import os
import csv
import xml.etree.ElementTree as ET

# Set your folder path here
folder_path = "path/to/your/folder"
output_csv = "xml_message_summary.csv"

# List to hold extracted data
data_rows = []

# Process each .xml file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".xml"):
        filepath = os.path.join(folder_path, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()

            # Split file content into individual messages using '@@'
            messages = [m.strip() for m in content.split('@@') if m.strip()]

            for message_text in messages:
                try:
                    root = ET.fromstring(message_text)

                    # Extract fields with fallback to blank if not found
                    msg_id = root.findtext('.//MsgID', default='').strip()
                    msg_type = root.findtext('.//MsgType', default='').strip()
                    trade_type = root.findtext('.//TradeType', default='').strip()
                    receiver = root.findtext('.//Receiver', default='').strip()
                    sender = root.findtext('.//Sender', default='').strip()

                    # Remove terminal code (9th character) if BIC is 12 characters
                    if len(receiver) == 12:
                        receiver = receiver[:8] + receiver[9:]
                    if len(sender) == 12:
                        sender = sender[:8] + sender[9:]

                    data_rows.append([
                        filename,
                        msg_id,
                        msg_type,
                        trade_type,
                        receiver,
                        sender
                    ])
                except ET.ParseError:
                    print(f"⚠️ Skipped malformed XML message in file: {filename}")

# Write results to CSV
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["File Name", "Message ID", "Message Type", "Trade Type", "Receiver BIC", "Sender BIC"])
    writer.writerows(data_rows)

print(f"✅ CSV file '{output_csv}' has been created with extracted XML message data.")
