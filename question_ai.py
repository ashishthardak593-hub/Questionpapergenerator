import random


def get_templates(topic):

    topic = topic.lower()

    # Architecture / Model
    if ("architecture" in topic or
        "model" in topic or
        "framework" in topic):

        return [
            "Explain {} with neat diagram.",
            "Discuss components of {}.",
            "Describe architecture and working of {}.",
            "Analyse {} in detail.",
            "Explain layered structure of {}."
        ]

    # Protocol / Communication
    elif ("protocol" in topic or
          "mqtt" in topic or
          "http" in topic or
          "coap" in topic or
          "ble" in topic):

        return [
            "Explain working of {}.",
            "Discuss applications of {}.",
            "Compare {} with suitable examples.",
            "Explain advantages and limitations of {}.",
            "Discuss role of {} in communication."
        ]

    # Security / Algorithm
    elif ("security" in topic or
          "encryption" in topic or
          "algorithm" in topic):

        return [
            "Explain {} in detail.",
            "Discuss working mechanism of {}.",
            "Analyse security features of {}.",
            "Explain advantages and limitations of {}.",
            "Discuss applications of {}."
        ]

    # Cloud / Services / Technologies
    else:

        return [
            "What is {}?",
            "Explain {} in detail.",
            "Discuss working and applications of {}.",
            "Describe advantages and disadvantages of {}.",
            "Write short notes on {}.",
            "Discuss importance of {}.",
            "Explain {} with examples."
        ]


def generate_question_bank(
        syllabus_text,
        difficulty
):

    lines = syllabus_text.split('\n')

    units = {}
    current_unit = ""

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if line.lower().startswith("unit"):

            current_unit = line.upper()
            units[current_unit] = []

        else:

            topics = line.split(',')

            for topic in topics:

                topic = topic.strip()

                if topic:
                    units[current_unit].append(
                        topic
                    )

    question_bank = {}

    for unit, topics in units.items():

        question_bank[unit] = []

        for topic in topics:

            templates = get_templates(
                topic
            )

            # Har topic se 2 different questions
            selected = random.sample(
                templates,
                min(2, len(templates))
            )

            for template in selected:

                question = template.format(
                    topic
                )

                question_bank[unit].append(
                    question
                )

    return question_bank