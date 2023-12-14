from language_tool_python import LanguageTool

def correct_text(text):
    tool = LanguageTool('ru-RU')
    matches = tool.check(text)
    corrected_text = tool.correct(text)

    return corrected_text
