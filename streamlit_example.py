import streamlit_example as st
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Display YOLO introduction
yolo_text = """
## Auto Defect Detection and Classifications

Our platform utilizes YOLO's advanced capabilities to provide rapid and accurate defect detection, essential for maintaining quality control and achieving excellence in manufacturing. YOLO is a state-of-the-art model designed for real-time object detection and classification. YOLO processes images with exceptional speed, ensuring quick identification and classification of defects. It employs a single neural network to deliver precise predictions, enhancing efficiency and accuracy. Its versatile application makes it ideal for automated quality inspection and defect analysis across various manufacturing environments. Enhance your defect detection process with YOLO, combining speed and precision to uphold the highest standards of quality.

"""
st.markdown(yolo_text)

# Main content area
st.title('Select Your Mode')

# Selectbox widget in the main content area
option = st.selectbox(' ', ['Plotting', 'Fin merge', 'Fin merge (Batch process)', 'Fin collapses', 'Fin collapses (Batch process)', 'Poly Gate'])
st.write(f'You selected: {option}')

# File uploader widget
uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True)



# Load your image using OpenCV
image = cv2.imread("1.BMP")  # Replace with your image path
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB

st.title("Interactive Image Plot with X-range Selection")

# Textbox for rotation angle (allow continuous values)
angle = st.number_input("Enter rotation angle (degrees):", value=0.0, format="%.1f", step=0.1)

# angle = st.number_input("Enter rotation angle (degrees):", value=0)

# Rotate the image
if angle != 0:
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image, M, (w, h))
else:
    rotated_image = image

# Get the height and width of the rotated image
height, width, _ = rotated_image.shape

# Create sliders for two x-range selections
x_start_1, x_end_1 = st.slider("Select x-range 1", 0, width, (0, width))
x_start_2, x_end_2 = st.slider("Select x-range 2", 0, width, (0, width))

# Draw vertical lines on the rotated image
image_with_lines = rotated_image.copy()
cv2.line(image_with_lines, (x_start_1, 0), (x_start_1, height), (255, 0, 0), 2)  # Red line for Range 1 Start
cv2.line(image_with_lines, (x_end_1, 0), (x_end_1, height), (255, 0, 0), 2)    # Red line for Range 1 End
cv2.line(image_with_lines, (x_start_2, 0), (x_start_2, height), (0, 255, 0), 2)  # Green line for Range 2 Start
cv2.line(image_with_lines, (x_end_2, 0), (x_end_2, height), (0, 255, 0), 2)    # Green line for Range 2 End

# Display the image with lines
st.image(image_with_lines, caption='Image with Selected Ranges', use_column_width=True)

# Toggle for image processing
if st.checkbox("Apply Image Processing (Convert to Grayscale)"):
    processed_image = cv2.cvtColor(rotated_image, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
    st.image(processed_image, caption='Processed Image (Grayscale)', use_column_width=True)
else:
    st.image(rotated_image, caption='Original Rotated Image', use_column_width=True)

# Display the selected ranges
st.write(f"Selected x-range 1: {x_start_1} to {x_end_1}")
st.write(f"Selected x-range 2: {x_start_2} to {x_end_2}")



if uploaded_files is not None:
    # Step 1: Get the current timestamp and format it to use in the folder name
    if 'timestamp' not in st.session_state:
        st.session_state.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if 'folder_name' not in st.session_state:
        st.session_state.folder_name = 'upload/' + f'{st.session_state.timestamp}'
        if not os.path.exists(st.session_state.folder_name):
            os.makedirs(st.session_state.folder_name)
    
    if 'output_folder' not in st.session_state:
        st.session_state.output_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        st.session_state.output_folder = 'output/' + f'{st.session_state.output_timestamp}'
        if not os.path.exists(st.session_state.output_folder):
            os.makedirs(st.session_state.output_folder)

    # Iterate over each uploaded file and save it to the folder
    for uploaded_file in uploaded_files:
        file_path = os.path.join(st.session_state.folder_name, uploaded_file.name)
        # Save each file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        # Display file information
        st.write(f"File saved to: {file_path}")

        # Process each file based on its type and selected option
        if uploaded_file.type == "text/csv":
            df = pd.read_csv(file_path)

            if option == 'Plotting':
                # Initialize session state variables if they do not exist
                if 'show_dataframe' not in st.session_state:
                    st.session_state['show_dataframe'] = False
                if 'plot_dataframe' not in st.session_state:
                    st.session_state['plot_dataframe'] = False

                # Create columns for layout
                col1, col2 = st.columns([1, 2])  # Adjust the ratios as needed

                # Toggle button for showing/hiding the DataFrame in the left column
                with col1:
                    if st.button('Show DataFrame', key=f"show_dataframe_{uploaded_file.name}"):
                        st.session_state['show_dataframe'] = not st.session_state['show_dataframe']

                    # Display DataFrame if the state is set to True
                    if st.session_state['show_dataframe']:
                        st.write(df)

                # Toggle button for plotting/removing the plot in the right column
                with col2:
                    if st.button('Plot wafer map', key=f"plot_wafer_{uploaded_file.name}"):
                        st.session_state['plot_dataframe'] = not st.session_state['plot_dataframe']

                    # Plot the DataFrame if the state is set to True
                    if st.session_state['plot_dataframe']:
                        st.write("Plotting the DataFrame...")

                        # Create the scatter plot
                        plt.figure(figsize=(8, 6))
                        plt.scatter(df['x'], df['y'], c=df['value'], cmap='viridis', s=100)
                        plt.colorbar(label='Value')
                        plt.xlabel('X-axis')
                        plt.ylabel('Y-axis')
                        plt.title('2D Scatter Plot with Values')

                        # Save the plot
                        plot_path = os.path.join(st.session_state.output_folder, 'scatter_plot.png')
                        plt.savefig(plot_path)
                        st.pyplot(plt)

                        # Provide download button for the saved image
                        with open(plot_path, "rb") as file:
                            st.download_button(
                                label="Download Scatter Plot",
                                data=file,
                                file_name="scatter_plot.png",
                                mime="image/png",
                                key=f"download_scatter_{uploaded_file.name}"  # Unique key
                            )
                        # Export DataFrame to CSV
                        csv_path = os.path.join(st.session_state.output_folder, 'dataframe.csv')
                        df.to_csv(csv_path, index=False)

                        # Provide download button for the CSV file
                        with open(csv_path, "rb") as file:
                            st.download_button(
                                label="Download DataFrame CSV",
                                data=file,
                                file_name="dataframe.csv",
                                mime="text/csv",
                                key=f"download_csv_{uploaded_file.name}"  # Unique key
                            )

        if uploaded_file.type in ["image/jpg", "image/jpeg", "image/png","image/bmp"]:
            image_bytes = uploaded_file.read()
            image_np = np.frombuffer(image_bytes, np.uint8)
            image_cv2 = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
            if option == 'Fin merge (Batch process)':
                print(image_cv2.shape)
            
            if option == 'Plotting':
                # Display the uploaded image
                st.image(cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB), caption='Uploaded Image', use_column_width=True)

            # Example of processing based on option
            if option == 'Fin merge':
                # Example processing: Convert to grayscale
                processed_image = cv2.GaussianBlur(image_cv2, (5, 5), 0)
                st.image(processed_image, caption='Processed Image', use_column_width=True)

                # Save the processed image
                processed_image_path = os.path.join(st.session_state.output_folder, 'processed_image.png')
                cv2.imwrite(processed_image_path, processed_image)

                # Provide download button for the processed image
                with open(processed_image_path, "rb") as file:
                    st.download_button(
                        label="Download Processed Image",
                        data=file,
                        file_name="processed_image.png",
                        mime="image/png",
                        key=f"download_processed_image_{uploaded_file.name}"  # Unique key
                    )
            else:
                st.write(f"Option '{option}' selected. Processing not implemented for this option.")







