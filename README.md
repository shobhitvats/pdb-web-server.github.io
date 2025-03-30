# PDB Web Server

This project is a web application that allows users to upload PDB files or provide PDB IDs to analyze sulfur-mediated chalcogen interactions. The application processes the input using a Python script and displays the results on the web interface.

## Features

- Upload PDB files directly from your computer.
- Enter a PDB ID to retrieve the corresponding PDB file from the internet.
- Analyze the PDB file for chalcogen interactions using the provided Python script.
- Display results in a user-friendly format.

## Project Structure

```
pdb-web-server
├── app
│   ├── __init__.py
│   ├── routes.py
│   ├── static
│   └── templates
│       └── index.html
├── scripts
│   └── initial_code.py
├── uploads
├── requirements.txt
├── app.py
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd pdb-web-server
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python app.py
   ```

2. Open your web browser and navigate to `http://127.0.0.1:5000`.

3. Use the interface to upload a PDB file or enter a PDB ID.

4. View the results of the analysis directly on the web page.

## Dependencies

- Flask
- Biopython

## License

This project is licensed under the MIT License.