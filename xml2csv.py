
import xml.etree.ElementTree as ET
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import datetime


def get_namespaced_tag(tag, namespace):
    """
       Returns the namespaced tag.
       """
    return f"{{{namespace}}}{tag}"


def extract_data_from_xml(root, namespace, xml_file_name):
    data = []
    namespaced_managed_object = get_namespaced_tag('managedObject', namespace)
    namespaced_p = get_namespaced_tag('p', namespace)

    # Extract the dateTime from the header log element
    header_log = root.find('.//' + get_namespaced_tag('header', namespace) + '/' + get_namespaced_tag('log', namespace))
    datetime = header_log.get('dateTime') if header_log is not None else 'No dateTime'

    for managedObject in root.findall(".//" + namespaced_managed_object):
        record = {
            'FILENAME': xml_file_name,
            'DATETIME': datetime,
            'VERSION': managedObject.get('version', 'No version'),
            'DISTNAME': managedObject.get('distName', 'No distName'),
            'MOID': managedObject.get('id', 'No id')
        }

        for p in managedObject.findall(namespaced_p):
            record[p.get('name', 'Unnamed')] = p.text

        data.append(record)
    return data


def convert_xml_to_csv(xml_file_path, csv_output_path, namespace):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    xml_file_name = os.path.basename(xml_file_path)
    extracted_data = extract_data_from_xml(root, namespace, xml_file_name)

    if not extracted_data:
        print("No data extracted from XML.")
        return

    df = pd.DataFrame(extracted_data)
    df.to_csv(csv_output_path, index=False)
    print(f"Data exported to {csv_output_path}")


def select_xml_file():
    xml_file_path = filedialog.askopenfilename(title="Select XML File", filetypes=[("XML files", "*.xml")])
    if xml_file_path:
        xml_file_label.config(text="XML File: " + xml_file_path)
        app_data['xml_file_path'] = xml_file_path


def select_output_folder():
    csv_output_folder = filedialog.askdirectory(title="Select Folder to Save CSV")
    if csv_output_folder:
        output_folder_label.config(text="Output Folder: " + csv_output_folder)
        app_data['csv_output_folder'] = csv_output_folder


def start_conversion():
    # Check for expiration date
    current_date = datetime.date.today()
    expiration_date = datetime.date(2023, 11, 13) + datetime.timedelta(days=90)
    if current_date > expiration_date:
        messagebox.showwarning("Warning", "This application has expired.")
        return

    if 'xml_file_path' in app_data and 'csv_output_folder' in app_data:
        xml_file_name = os.path.splitext(os.path.basename(app_data['xml_file_path']))[0]
        csv_output_path = os.path.join(app_data['csv_output_folder'], xml_file_name + '.csv')
        namespace = 'raml20.xsd'
        convert_xml_to_csv(app_data['xml_file_path'], csv_output_path, namespace)
        messagebox.showinfo("Success", "Conversion completed successfully!")
    else:
        messagebox.showwarning("Warning", "Please select an XML file and an output folder.")


# Set up the tkinter application
root = tk.Tk()
root.title("XML to CSV Converter")
root.configure(bg='black')  # Set the background color of the window to black

app_data = {}

# Create and place widgets with specified colors
xml_file_label = tk.Label(root, text="No XML File Selected", bg='black', fg='white')
xml_file_label.pack()

select_xml_button = tk.Button(root, text="Select XML File", command=select_xml_file, bg='white', fg='black')
select_xml_button.pack()

output_folder_label = tk.Label(root, text="No Output Folder Selected", bg='black', fg='white')
output_folder_label.pack()

select_output_button = tk.Button(root, text="Select Output Folder", command=select_output_folder, bg='white',
                                 fg='black')
select_output_button.pack()

start_button = tk.Button(root, text="Start Conversion", command=start_conversion, bg='white', fg='black')
start_button.pack()

# Trademark notice
trademark_label = tk.Label(root, text="Created by Reianjim Ramos", bg='black', fg='white')
trademark_label.pack()

# Start the GUI event loop
root.mainloop()
