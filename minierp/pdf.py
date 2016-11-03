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
# from gestion.settings import STATIC_ROOT
static = '/home/samuel/Projets/Archives/Old/GestionPME/gestionpme/djpgirardin/static'
IMG_HEADER = static + '/images/entete.png'
IMG_FOOTER = static + '/images/pied.png'

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


def add_description_step(pdf, formset):
    title = formset.step_title
    description_step = formset.step_description
    # add description steps
    # 1 add title
    p = ParagraphStyle(name='Description', fontName='ErasITC-Demi', fontSize=13,  leading = 20)
    p_title = Paragraph(title, p)
    p_title.wrapOn(pdf, (210-2*mX1)*mm, 100)
    p_title.drawOn(pdf, mX1, -300)

    # 2 add description
    p = ParagraphStyle(name='Description', fontName='ErasITC-Light', fontSize=12,  leading = 20)
    p_description = Paragraph(unicode(description_step).replace('\r','<br />\n'), p)
    w,h = p_description.wrap(210*mm, 400)
    p_description.drawOn(pdf, mX1 +20, -310-h)


def add_prices(pdf, prices):
    ph = 660
    pdf.drawString(mX1, -ph, l_prixht)
    pdf.drawString(mX1 + 95, -ph, l_tva)
    pdf.setFont('ErasITC-Demi', 13)
    pdf.drawString(mX1 + 190, -ph, l_prixttc)
    pdf.setFont('ErasITC-Light', 13)
    pdf.drawString(mX1 + 290, -ph, l_acompte)
    pdf.setFont('ErasITC-Demi', 13)
    pdf.drawString(mX1 + 410, -ph, l_netapayer)
    pdf.setFont('ErasITC-Light', 13)
    ph = 690
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
    add_txt = """J'&eacute;mets une r&eacute;serve en ce qui concerne les parties totalement invisibles.\r
    \r
    Pose sur dalle, carrelage ou plancher.\r
    Pr&eacute;voir la rehausse devant &#171; l'autel &#187;.\r
    \r
    JP Girardin."""

    # init pdf canvas
    pdf = init_pdf(response)
    add_header(pdf)
    add_footer(pdf)

    # add client block
    add_client_and_title(pdf, nf_line, c, date)

    # check total height of steps
    # check if add txt
    # if inferior to max height -> ok
    # else put add_txt on other page
    # if inferior to max height -> ok
    # else check how many can fit
    # then put remanings on next page
    # add add txt
    # add prices

    # loop on steps
    # while fit ok ((with max p1)
    # add txt ?
    # other page or not
    # prices
    # if not fit next page
    # while fit (with max p2)
    # add txt ?
    # other page or note
    # add prices

    add_description_step(pdf, formset)

    add_additional_text(pdf, add_txt)

    add_prices(pdf, prices)

    return pdf

# def generate_facture(response, date, client, nf, title, description, prices):
#     # Parse data
#     dateline = 'Nolay, le %s' % date
#     nfline = 'Facture n° %d' % nf
#     l_prixht = 'Total HT'
#     l_prixttc = 'Prix TTC'
#     l_tva = 'Total TVA'
#     l_acompte = 'Déjà réglé TTC'
#     l_netapayer = 'Net à payer'
#
#     # Settings
#     img_header = static +'/images/entete.png'
#     img_footer = static +'/images/pied.png'
#     pdf = canvas.Canvas(response)
#     H = 297*mm
#     W = 210*mm
#     mX1 = 60
#     d = 20
#     pdf.setLineWidth(.3)
#     pdf.setFont('ErasITC-Light', 13)
#     pdf.translate(0,297*mm)
#
#     # Header
#     w = 210/1.8*mm
#     h = w * get_image(img_header)
#     pdf.drawImage(img_header, W/2-w/2, -100, width=w, height=h,  mask='auto')
#
#     # Bloc adresse
#     pdf.setFont('ErasITC-Demi', 13)
#     pdf.drawString(mX1 +280,-180, client[0] + ' ' + client[1] + ' ' + client[2])
#     pdf.setFont('ErasITC-Light', 13)
#     pdf.drawString(mX1 +280,-180 - d, client[3])
#     if client[4]:
#         pdf.drawString(mX1 +280,-180 - 2*d, client[4] + ' ' + client[5])
#     else:
#         pdf.drawString(mX1 +280,-180 - 2*d, client[5])
#     # Nf
#     pdf.drawString(mX1,-200 -3*d, nfline)
#     # Date
#     pdf.drawString(mX1 + 280 ,-200 -3*d, dateline)
#
#     # Description
#     p = ParagraphStyle(name='Description', fontName='ErasITC-Light', fontSize=13,  leading = 20)
#     # backColor = '#FFFF00' debug
#
#     p_title = Paragraph('<u>'+title+'</u>', p)
#     p_title.wrapOn(pdf, (210-2*mX1)*mm, 100)
#     p_title.drawOn(pdf, mX1, -300)
#
#     p_description = Paragraph(unicode(description).replace('\r','<br />\n'), p)
#     # p_description.wrapOn(pdf, (210-2*(mX1+10))*mm, 300)
#     # p_description.wrapOn(pdf, (210-2*(mX1+10))*mm, 300)
#     w,h = p_description.wrap((210-2*(mX1+10))*mm, 400)
#     p_description.drawOn(pdf, mX1 +20, -310-h)
#
#     # Prix
#     ph = 660
#     pdf.drawString(mX1  ,-ph , l_prixht)
#     pdf.drawString(mX1 + 95  ,-ph, l_tva)
#     pdf.setFont('ErasITC-Demi', 13)
#     pdf.drawString(mX1 + 190 ,-ph , l_prixttc)
#     pdf.setFont('ErasITC-Light', 13)
#     pdf.drawString(mX1 + 290 ,-ph , l_acompte)
#     pdf.setFont('ErasITC-Demi', 13)
#     pdf.drawString(mX1 + 410 ,-ph , l_netapayer)
#     pdf.setFont('ErasITC-Light', 13)
#     ph = 690
#     pdf.drawString(mX1  ,-ph , '%.2f' % prices[0])
#     pdf.drawString(mX1 + 95  ,-ph, '%.2f' % prices[1])
#     pdf.setFont('ErasITC-Demi', 13)
#     pdf.drawString(mX1 + 190 ,-ph , '%.2f' % prices[2])
#     pdf.setFont('ErasITC-Light', 13)
#     pdf.drawString(mX1 + 290 ,-ph , '%.2f' % prices[3])
#     pdf.setFont('ErasITC-Demi', 13)
#     pdf.drawString(mX1 + 410 ,-ph , '%.2f' % prices[4])
#     pdf.setFont('Helvetica', 14)
#     pdf.drawString(mX1 + 480 ,-ph ,'€')
#
#     # Footer
#     w = 210/1.2*mm
#     h = w * get_image(img_footer)
#     pdf.drawImage(img_footer, W/2-w/2, -H+20, width=w, height=h,  mask='auto')
#
#     return pdf