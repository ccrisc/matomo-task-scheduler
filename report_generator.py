import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os

def generate_reports(df, templates_dir='templates', output_dir='generated_reports'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(templates_dir))

    # Generate reports
    for _, row in df.iterrows():
        template_name = "template_Lecture.html" if row['type_of'] == 'Lecture' else "template_Exercise.html"
        template = env.get_template(template_name)
        output_file = os.path.join(output_dir, f"{row['language']}_{row['type_of']}_{row['lecture_no']}.html")

        # Render the template with the row data
        with open(output_file, 'w') as f:
            f.write(template.render(row=row))

    return len(df)  # Return number of reports generated
