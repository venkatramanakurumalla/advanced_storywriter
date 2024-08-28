# Creative Story Writer - Story Generation with DistilGPT-2

## Project Overview

This project is a GUI-based application that leverages a fine-tuned DistilGPT-2 model to generate creative  stories. The application allows users to input story prompts, customize settings like temperature and length, and generate coherent and engaging stories. It also supports the loading of custom story elements (settings, characters, plot twists) from a JSON file to further enrich the generated content.

## Features

- **Story Prompt Input**: Users can input custom story prompts to guide the narrative generation.
- **Base Story Input**: Optional base story text can be provided to influence the generated output.
- **Advanced Settings**: Control the length, creativity, and randomness of the generated stories using parameters like max length, temperature, top-k, and top-p.
- **Custom Story Elements**: Load custom story settings, characters, and plot twists from a JSON file to tailor the narrative.
- **Save Generated Stories**: Save the generated stories to text files for future reference.
- **Story History**: View the history of generated stories within the current session.
- **User-Friendly GUI**: A simple and intuitive interface built with Tkinter, featuring a progress bar during story generation.

## Installation

### Prerequisites

- Python 3.7 or higher
- PIP (Python package manager)


### Install Required Packages
transformers==4.31.0
torch==2.0.1
tkinter (comes pre-installed with Python)


```bash
pip install -r requirements.txt
```

### Download the Fine-Tuned Model

1. Download the fine-tuned DistilGPT-2 model from [hugingface].


## Usage

### Running the Application

To start the story generator, run the following command:

```bash
python main.py
```

This will launch the GUI, where you can enter prompts, adjust story parameters, and generate stories.

### Generating a Story

1. **Enter a Story Prompt**: Type a prompt that sets the direction for your story.
2. **Enter a Base Story (Optional)**: Provide some initial text if you want to influence the story further.
3. **Adjust Advanced Settings**:
   - **Max Length**: Set the maximum number of tokens in the generated story.
   - **Temperature**: Control the creativity of the model. A higher value (closer to 1.0) produces more creative results.
   - **Top-k**: Limit the sampling pool to the top-k most likely words.
   - **Top-p**: Use nucleus sampling, where the model chooses from the top cumulative probability.
4. **Generate the Story**: Click the "Generate Story" button. The generated story will be displayed in the output text area.
5. **Save the Story**: Click the "Save Story" button to save the generated story to a text file.

### Loading Custom Story Data

1. Prepare your custom story elements in a JSON file (e.g., `story.json`).
2. Click the "Load Custom Story Data" button and select your JSON file.
3. The application will use these elements to enhance the generated stories.

### Saving Generated Stories

1. After generating a story, click the "Save Story" button.
2. Choose a location to save your story as a `.txt` file.

## Example Story Elements JSON Structure

Here is an example of how the `story.json` file should be structured:

```json
{
  "settings": ["in a dense forest", "on a distant planet", "in an ancient temple"],
  "characters": ["a brave warrior", "a cunning thief", "a mysterious stranger"],
  "plot_twists": ["discovers a shocking truth", "uncovers a hidden treasure", "faces an unexpected enemy"]
}
```

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your changes.

### To-Do List

- [ ] Expand the dataset for better diversity in story generation.
- [ ] Improve the GUI with additional user options.
- [ ] Add more customization options for story generation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Hugging Face** for the amazing `transformers` library,DistilGPT-2.
- **Your Name/Organization** for the initial idea and project creation.

---

