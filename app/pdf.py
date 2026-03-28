from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import cm
from io import BytesIO
from datetime import date

def gerar_pdf_processo(processo, cliente, prazos):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    elementos = []

    # Título
    titulo_style = ParagraphStyle(
        'titulo',
        parent=styles['Title'],
        fontSize=18,
        textColor=colors.HexColor('#1a1a2e'),
        spaceAfter=12
    )
    elementos.append(Paragraph("⚖ Sistema Jurídico", titulo_style))
    elementos.append(Paragraph("Relatório de Processo", styles['Heading2']))
    elementos.append(Spacer(1, 0.5*cm))

    # Data
    elementos.append(Paragraph(f"Gerado em: {date.today().strftime('%d/%m/%Y')}", styles['Normal']))
    elementos.append(Spacer(1, 0.5*cm))

    # Dados do processo
    elementos.append(Paragraph("Dados do Processo", styles['Heading2']))
    dados_processo = [
        ['Número', processo.numero],
        ['Descrição', processo.descricao or '-'],
        ['Vara', processo.vara or '-'],
        ['Status', processo.status],
    ]
    tabela = Table(dados_processo, colWidths=[4*cm, 13*cm])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#1a1a2e')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (1, 0), (-1, -1), [colors.HexColor('#f0f2f5'), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elementos.append(tabela)
    elementos.append(Spacer(1, 0.5*cm))

    # Dados do cliente
    elementos.append(Paragraph("Dados do Cliente", styles['Heading2']))
    dados_cliente = [
        ['Nome', cliente.nome],
        ['CPF', cliente.cpf],
        ['Email', cliente.email or '-'],
        ['Telefone', cliente.telefone or '-'],
    ]
    tabela2 = Table(dados_cliente, colWidths=[4*cm, 13*cm])
    tabela2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#1a1a2e')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (1, 0), (-1, -1), [colors.HexColor('#f0f2f5'), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elementos.append(tabela2)
    elementos.append(Spacer(1, 0.5*cm))

    # Prazos
    if prazos:
        elementos.append(Paragraph("Prazos", styles['Heading2']))
        dados_prazos = [['Descrição', 'Data limite', 'Status']]
        for p in prazos:
            status = 'Concluído' if p.concluido else 'Pendente'
            dados_prazos.append([p.descricao, str(p.data_limite), status])
        tabela3 = Table(dados_prazos, colWidths=[8*cm, 4*cm, 5*cm])
        tabela3.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a2e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f0f2f5'), colors.white]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elementos.append(tabela3)

    doc.build(elementos)
    buffer.seek(0)
    return buffer