from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.rl_config import defaultPageSize

PAGE_WIDTH = defaultPageSize[0]
PAGE_HEIGHT = defaultPageSize[1]


class FeedbackDocument:
    def __init__(self, file_name, feedback_to, questions, answers):
        self.questions = questions
        self.answers = answers
        self.canvas = canvas.Canvas(file_name, pagesize=letter)
        self.feedback_to = feedback_to
        self.block_offset_y = 0

    def generate(self):
        canvas = self.canvas
        canvas.setLineWidth(0.3)
        canvas.setFont("Helvetica", 12)
        self.__add_header()

        for i in range(len(self.questions)):
            question = self.questions[i]
            answers = self.answers[i]
            self.__add_block(question, answers, i)

        canvas.save()

    def __add_header(self):
        canvas = self.canvas
        canvas.drawString(30, 750, "Junior Philippine Computer Society - APC")
        canvas.drawString(30, 735, "Peer Evaluation Results (Term 2 A.Y. 2020-2021)")

        canvas.drawString(500, 750, "May 1, 2021")

        canvas.drawString(30, 683, "This evaluation is given to:")
        canvas.line(180, 680, 580, 680)
        canvas.drawString(
            180,
            683,
            self.feedback_to,
        )

        text = "* This document is automatically formatted from the peer review form results. *"
        text_width = stringWidth(text, "Helvetica", 11)

        paragraph_style = ParagraphStyle(name="Normal", fontSize=11, textColor="#DCDCDC")
        paragraph = Paragraph(text, style=paragraph_style)
        w, h = paragraph.wrap(600, 100)
        paragraph.drawOn(canvas, (PAGE_WIDTH - text_width) / 2.0, 80)

    def __add_block(self, question, answers, index):
        question_y = 650 - self.block_offset_y
        question_spacing_y = 6
        question_paragraph = self.__draw_paragraph(
            f"<b>{index + 1}. {question}</b>",
            x=30,
            y=question_y,
        )

        question_height = question_paragraph.height
        answer_y = question_y - question_height - question_spacing_y
        answer_spacing_y = 3
        answer_block_height = question_height

        for answer in answers:
            answer_paragraph = self.__draw_paragraph(
                f"&#8226; {answer}", x=40, y=answer_y
            )
            answer_height = answer_paragraph.height
            answer_block_height += answer_height
            answer_y -= answer_height + answer_spacing_y

        self.block_offset_y += answer_block_height + 30

    def __draw_paragraph(self, text, x, y, max_width=560, max_height=100):
        paragraph_style = ParagraphStyle(name="Normal", fontSize=11)
        paragraph = text.replace("\n", "<br />")
        paragraph = Paragraph(paragraph, style=paragraph_style)

        # Set wrapping
        w, h = paragraph.wrap(max_width, max_height)
        paragraph.drawOn(self.canvas, x, y - h)

        return paragraph