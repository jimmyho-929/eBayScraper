import subprocess

def run_script(request):
    # Replace 'your_script.py' with the actual name of your Python script
    script_name = 'app.py'

    # Replace 'python3' with the appropriate command to run your script
    command = ['streamlit run', script_name]

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stdout
        return f'Script executed successfully:\n{output}'
    except Exception as e:
        return f'Error executing the script:\n{str(e)}'
