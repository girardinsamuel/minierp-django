# -*- coding: utf-8 -*-
import os

from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf import settings
from django.conf.urls.static import static

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import mm
from reportlab.lib import utils
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# TODO check how to use real STATIC variable
# from gestion.settings import BASE_DIR
static = 'minierp/static'
# static = '/home/samuel/Projects/In Progress/minierp-django/minierp/static'
IMG_HEADER = static + '/img/entete.png'
IMG_FOOTER = static + '/img/pied.png'

# register two fonts: italic and demi
afmFile = static +'/fonts/ErasLightITC.afm'
pfbFile = static +'/fonts/ErasLightITC.pfb'
justFace = pdfmetrics.EmbeddedType1Face(afmFile, pfbFile)
faceName = 'ErasITC-Light' # pulled from AFM file
pdfmetrics.registerTypeFace(justFace)

afmFile = static +'/fonts/ErasDemiITC.afm'
pfbFile = static +'/fonts/ErasDemiITC.pfb'
justFace = pdfmetrics.EmbeddedType1Face(afmFile, pfbFile)
faceName = 'ErasITC-Demi' # pulled from AFM file
pdfmetrics.registerTypeFace(justFace)

# set global size variables
H = 297 * mm
W = 210 * mm
mX1 = 60
d = 20
MAX_NEW_PAGE = 700
MAX_ONE_PAGE = 410
LINE_HEIGHT = 18
backColor = '#FFFF00' # debug
dateline = 'Nolay, le %s'
l_prixht = 'Total HT'
l_prixttc = 'Prix TTC'
l_tva = 'Total TVA'
l_acompte = 'Déjà réglé TTC'
l_netapayer = 'Net à payer'


def get_image(path, width=1*mm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return aspect


def init_pdf(response):
    pdf = canvas.Canvas(response)
    pdf.setLineWidth(.3)
    pdf.setFont('ErasITC-Light', 13)
    pdf.translate(0, 297 * mm)

    return pdf


def add_header(pdf):
    w = 210/1.8*mm
    h = w * get_image(IMG_HEADER)
    pdf.drawImage(IMG_HEADER, W/2-w/2, -100, width=w, height=h,  mask='auto')


def add_footer(pdf):
    w = 210/1.2*mm
    h = w * get_image(IMG_FOOTER)
    pdf.drawImage(IMG_FOOTER, W/2-w/2, -H+20, width=w, height=h,  mask='auto')


def add_description_step(pdf, formset, h):
    print 'h', h
    title = '<u>' + formset.step_title + '</u>'
    description_step = formset.step_description
    # add description steps
    # 1 add title
    p = ParagraphStyle(name='Description', fontName='ErasITC-Light', fontSize=13,  leading=20)
    p_title = Paragraph(title, p)
    p_title.wrapOn(pdf, (210-2*mX1)*mm, 100)
    p_title.drawOn(pdf, mX1, -300-h)

    # 2 add description
    p = ParagraphStyle(name='Description', fontName='ErasITC-Light', fontSize=12,  leading=18) #, backColor='red')
    p_description = Paragraph(description_step, p)
    w, h2 = p_description.wrap(153*mm, 300)
    p_description.drawOn(pdf, mX1 +20, -310-h2-h)


def add_prices(pdf, prices):
    ph = 690
    pdf.drawString(mX1, -ph, l_prixht)
    pdf.drawString(mX1 + 95, -ph, l_tva)
    pdf.setFont('ErasITC-Demi', 13)
    pdf.drawString(mX1 + 190, -ph, l_prixttc)
    pdf.setFont('ErasITC-Light', 13)
    pdf.drawString(mX1 + 290, -ph, l_acompte)
    pdf.setFont('ErasITC-Demi', 13)
    pdf.drawString(mX1 + 410, -ph, l_netapayer)
    pdf.setFont('ErasITC-Light', 13)
    ph = 720
    pdf.drawString(mX1, -ph, '%.2f' % prices[0])
    pdf.drawString(mX1 + 95, -ph, '%.2f' % prices[1])
    pdf.setFont('ErasITC-Demi', 13)
    pdf.drawString(mX1 + 190, -ph, '%.2f' % prices[2])
    pdf.setFont('ErasITC-Light', 13)
    pdf.drawString(mX1 + 290, -ph, '%.2f' % prices[3])
    pdf.setFont('ErasITC-Demi', 13)
    pdf.drawString(mX1 + 410, -ph, '%.2f' % prices[4])
    pdf.setFont('Helvetica', 14)
    pdf.drawString(mX1 + 480, -ph, '€')


def add_client_and_title(pdf, title, c, date):
    pdf.setFont('ErasITC-Demi', 13)
    pdf.drawString(mX1 + 280, -180, c.civilite + ' ' + c.nom + ' ' + c.prenom)
    pdf.setFont('ErasITC-Light', 13)
    pdf.drawString(mX1 + 280, -180 - d, c.adresse)
    if c.cp:
        pdf.drawString(mX1 + 280, -180 - 2 * d, str(c.cp) + ' ' + c.ville)
    else:
        pdf.drawString(mX1 + 280, -180 - 2 * d, c.ville)
    # Nf
    pdf.drawString(mX1, -200 - 3 * d, title)
    # Date
    pdf.drawString(mX1 + 280, -200 - 3 * d, dateline % date)


def add_additional_text(pdf, text):
    p = ParagraphStyle(name='Description', fontName='ErasITC-Light', fontSize=12, leading=12)
    p_description = Paragraph(unicode(text).replace('\r', '<br />\n'), p)
    p_description.wrap(210 * mm, 400)
    p_description.drawOn(pdf, mX1 + 20, -750)


def get_height_step(formset):
    description_step = formset.step_description
    # number of lines of description + 1 one for title
    nb = description_step.count('\n') + 2
    h = nb * d + 30 # interligne
    # TODO change with wrap paragraph to get height ?
    return h


def change_page(pdf):
    pass


def generate_quote(response, q):

    nq_line = 'Devis'

    pass


def generate_invoice(response, f, formset):

    # parse data
    date = DateFormat(f.date).format(get_format('DATE_FORMAT'))
    c = f.id_client
    prices = [f.prixht, f.parttva, f.prixttc, f.dejaregle, f.netapayer]
    nf = int(f.pk)
    nf_line = 'Facture n°%d' % nf

    # init pdf canvas
    pdf = init_pdf(response)
    add_header(pdf)
    add_footer(pdf)

    # add client block
    add_client_and_title(pdf, nf_line, c, date)

    hmax = MAX_ONE_PAGE
    first = True
    add_txt = unicode(f.add_description).replace(r'\r', '</br>\n')

    for step in formset:
        step.step_description = unicode(step.step_description).replace('\n','<br />\n')
        h = get_height_step(step)
        print 'loop h=', h
        if h < hmax and h < MAX_NEW_PAGE and first:
            print 'first'
            first = False
            hmax = MAX_NEW_PAGE
            add_description_step(pdf, step, h=0)
            # continue
        else:
            if not h < hmax:
                print 'change'
                change_page(pdf)
            print 'second'
            add_description_step(pdf, step, h)

    # if f.add_description:
    #     h = get_height(f.add_description)
    #     if not h < hmax:
    #         change_page(pdf)
    #     add_additional_text(pdf, f.add_description)

    add_prices(pdf, prices)

    return pdf