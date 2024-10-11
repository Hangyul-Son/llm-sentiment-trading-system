import os
from datetime import datetime

class ResearchOrganizer:
    def __init__(self, project_name):
        self.project_name = project_name
        self.filename = f"{project_name.lower().replace(' ', '_')}.md"
        self.file_path = os.path.join('Documentation History', self.filename)

    def create_document(self):
        os.makedirs('Documentation History', exist_ok=True)
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(f"# {self.project_name} Research Document\n\n")
            f.write(f"Created on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            sections = [
                "## 1. Literature Review",
                "### Key Papers",
                "### Other Sentiment-Based Trading Systems",
                "## 2. System Requirements",
                "### Core Functionalities",
                "### Data Sources",
                "#### News Data",
                "#### Market Data",
                "### Sentiment Analysis Approach",
                "## 3. Tools and Libraries Evaluation",
                "### Sentiment Analysis",
                "### Financial Data APIs",
                "### Other Relevant Libraries",
                "## 4. Project Outline",
                "### High-Level System Architecture",
                "### Project Milestones",
                "## 5. Notes and Ideas",
                "## 6. Summary of New Findings",
                "### Improving Sentiment Analysis Accuracy",
                "### Optimizing Execution Time",
                "### Reducing Costs"
            ]
            f.write('\n\n'.join(sections))

    def update_section(self, section, content):
        with open(self.file_path, 'r') as f:
            lines = f.readlines()

        section_start = None
        section_end = None
        for i, line in enumerate(lines):
            if line.strip() == section:
                section_start = i
            elif section_start is not None and line.startswith('#') and line.count('#') <= section.count('#'):
                section_end = i
                break

        if section_start is None:
            print(f"Section '{section}' not found.")
            return

        if section_end is None:
            section_end = len(lines)

        updated_lines = lines[:section_start + 1] + ['\n' + content + '\n\n'] + lines[section_end:]

        with open(self.file_path, 'w') as f:
            f.writelines(updated_lines)

        print(f"Updated section: {section}")

def document_research_results(organizer, research_goal):
    title = input("Enter the title of your research: ").strip()
    findings = input("Enter your findings: ").strip()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"Title: {title}\nFindings: {findings}\nDocumented on: {current_time}\n\n"

    organizer.update_section("## 1. Literature Review", content)
    if research_goal == "accuracy":
        organizer.update_section("### Improving Sentiment Analysis Accuracy", content)
    elif research_goal == "execution_time":
        organizer.update_section("### Optimizing Execution Time", content)
    elif research_goal == "costs":
        organizer.update_section("### Reducing Costs", content)

def add_manual_notes(organizer):
    note = input("Enter your note for 'Summary of New Findings': ")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"[{current_time}] {note}\n\n"
    organizer.update_section("## 6. Summary of New Findings", content)

def save_documentation(organizer):
    print(f"Research documentation saved to {os.path.abspath(organizer.file_path)}")

if __name__ == "__main__":
    project_name = "Sentiment-Based Trading System"
    organizer = ResearchOrganizer(project_name)
    if not os.path.exists(organizer.file_path):
        organizer.create_document()

    user_choice = input("Do you want to conduct new research or add manual notes? (research/notes): ").strip().lower()

    if user_choice == "research":
        research_goal = input("What is the goal of this research? (accuracy/execution_time/costs): ").strip().lower()
        if research_goal not in ["accuracy", "execution_time", "costs"]:
            print("Invalid goal. Please enter 'accuracy', 'execution_time', or 'costs'.")
        else:
            document_research_results(organizer, research_goal)
    elif user_choice == "notes":
        add_manual_notes(organizer)
    else:
        print("Invalid choice. Please enter 'research' or 'notes'.")

    save_documentation(organizer)