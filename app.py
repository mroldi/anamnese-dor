"""
ANAMNESE DOR · HC-FMUSP
Backend FastAPI — Google Sheets + PDF
"""

import os
import json
import io
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import gspread
from google.oauth2.service_account import Credentials
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ─── CONFIG ────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

# Google Sheets IDs (configurar no .env)
SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")
BACKUP_SHEET_ID = os.getenv("GOOGLE_BACKUP_SHEET_ID", "")

# Service account key — pode ser caminho para arquivo JSON ou JSON string
GOOGLE_CREDS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON", "")
GOOGLE_CREDS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")


def get_gspread_client():
    """Retorna cliente autenticado do gspread."""
    if GOOGLE_CREDS_JSON:
        # Credenciais via variável de ambiente (recomendado para Render)
        creds_dict = json.loads(GOOGLE_CREDS_JSON)
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    elif Path(GOOGLE_CREDS_FILE).exists():
        # Credenciais via arquivo local (desenvolvimento)
        creds = Credentials.from_service_account_file(GOOGLE_CREDS_FILE, scopes=SCOPES)
    else:
        raise RuntimeError(
            "Credenciais do Google não encontradas. "
            "Configure GOOGLE_CREDENTIALS_JSON ou coloque credentials.json na raiz."
        )
    return gspread.authorize(creds)


# ─── CABEÇALHOS DA PLANILHA ────────────────────────────────
# Ordem das colunas na planilha Google Sheets
SHEET_HEADERS = [
    # Identificação
    "data", "nome", "estado_civil", "escolaridade", "mora_em", "trabalho",
    "alergias", "antecedentes", "muc", "cirurgias",
    # HMA
    "encaminhamento", "tempo_dor", "queixa",
    # Dor
    "regioes_dor", "qualidade_dor", "componente_emocional", "vas",
    "frequencia", "predominio", "instalacao",
    "fatores_melhora", "fatores_piora", "tratamentos_anteriores",
    "medicamentos_dor", "red_flags",
    # Sono
    "percepcao_sono", "horas_sono", "med_sono", "caracteristicas_sono",
    "posicao_dormir", "travesseiro_aux", "altura_travesseiro", "colchao",
    # Hábitos
    "cafe", "almoco", "jantar", "intestino", "atividade_fisica", "humor",
    # Exame físico (resumidos)
    "inspecao", "comportamentos_dolorosos", "marcha", "marcha_desc",
    "equilibrio", "tonus", "horner", "reflexos_superficiais",
    # Exames complementares
    "exames_complementares",
    # Timestamp
    "timestamp_registro",
]


def ensure_headers(sheet):
    """Garante que a primeira linha da planilha tenha os cabeçalhos."""
    try:
        first_row = sheet.row_values(1)
        if not first_row:
            sheet.insert_row(SHEET_HEADERS, 1)
    except Exception:
        sheet.insert_row(SHEET_HEADERS, 1)


def data_to_row(data: dict) -> list:
    """Converte dicionário de dados em linha para a planilha."""
    data["timestamp_registro"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return [str(data.get(h, "")) for h in SHEET_HEADERS]


# ─── APP ────────────────────────────────────────────────────
app = FastAPI(title="Anamnese Dor HC-FMUSP")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ─── SALVAR NO GOOGLE SHEETS ───────────────────────────────
@app.post("/salvar")
async def salvar(request: Request):
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="JSON inválido")

    if not SHEET_ID:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "GOOGLE_SHEET_ID não configurado"}
        )

    try:
        client = get_gspread_client()
        row = data_to_row(data)

        # Planilha principal
        sh = client.open_by_key(SHEET_ID)
        ws = sh.sheet1
        ensure_headers(ws)
        ws.append_row(row)
        row_num = len(ws.get_all_values())

        # Planilha de backup (se configurada)
        if BACKUP_SHEET_ID:
            try:
                sh_bk = client.open_by_key(BACKUP_SHEET_ID)
                ws_bk = sh_bk.sheet1
                ensure_headers(ws_bk)
                ws_bk.append_row(row)
            except Exception as bk_err:
                print(f"[AVISO] Backup falhou: {bk_err}")

        return {"status": "ok", "row": row_num}

    except RuntimeError as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Erro ao salvar: {str(e)}"}
        )


# ─── GERAR PDF ─────────────────────────────────────────────
@app.post("/gerar-pdf")
async def gerar_pdf(request: Request):
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="JSON inválido")

    buffer = io.BytesIO()
    _build_pdf(data, buffer)
    buffer.seek(0)

    nome = data.get("nome", "paciente").replace(" ", "_")
    data_str = data.get("data", datetime.now().strftime("%Y-%m-%d"))
    filename = f"anamnese_{nome}_{data_str}.pdf"

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


def _build_pdf(data: dict, buffer: io.BytesIO):
    """Gera o PDF de anamnese com ReportLab."""
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2.2 * cm,
        rightMargin=2.2 * cm,
        topMargin=2.2 * cm,
        bottomMargin=2.2 * cm,
    )

    styles = getSampleStyleSheet()
    W = A4[0] - 4.4 * cm  # largura útil

    # Estilos customizados
    style_title = ParagraphStyle(
        "DocTitle", fontName="Helvetica-Bold", fontSize=16,
        textColor=colors.HexColor("#9b1c2e"), alignment=TA_CENTER,
        spaceAfter=4
    )
    style_subtitle = ParagraphStyle(
        "DocSubtitle", fontName="Helvetica", fontSize=10,
        textColor=colors.HexColor("#5a5450"), alignment=TA_CENTER,
        spaceAfter=2
    )
    style_section = ParagraphStyle(
        "Section", fontName="Helvetica-Bold", fontSize=11,
        textColor=colors.HexColor("#9b1c2e"),
        spaceBefore=14, spaceAfter=6
    )
    style_field_label = ParagraphStyle(
        "FieldLabel", fontName="Helvetica-Bold", fontSize=8,
        textColor=colors.HexColor("#5a5450"), spaceAfter=1
    )
    style_field_value = ParagraphStyle(
        "FieldValue", fontName="Helvetica", fontSize=9,
        textColor=colors.HexColor("#1a1714"), spaceAfter=6
    )
    style_small = ParagraphStyle(
        "Small", fontName="Helvetica", fontSize=7,
        textColor=colors.HexColor("#9a9490"), alignment=TA_RIGHT
    )

    def section(title):
        return [
            Spacer(1, 8),
            HRFlowable(width=W, thickness=0.5, color=colors.HexColor("#9b1c2e"), spaceAfter=4),
            Paragraph(title.upper(), style_section),
        ]

    def field(label, value, empty_text="Não informado"):
        v = str(value).strip() if value else empty_text
        return [
            Paragraph(label, style_field_label),
            Paragraph(v, style_field_value),
        ]

    def two_col(pairs):
        """Duas colunas lado a lado."""
        rows = []
        for i in range(0, len(pairs), 2):
            left = pairs[i]
            right = pairs[i + 1] if i + 1 < len(pairs) else ("", "")
            rows.append([
                [Paragraph(left[0], style_field_label), Paragraph(str(left[1] or "—"), style_field_value)],
                [Paragraph(right[0], style_field_label), Paragraph(str(right[1] or "—"), style_field_value)],
            ])

        tables = []
        for row in rows:
            t = Table([row], colWidths=[W / 2 - 5, W / 2 - 5])
            t.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]))
            tables.append(t)
        return tables

    def muscle_table(muscles_dict):
        """Tabela de força muscular."""
        rows = [["Músculo", "Força", "Músculo", "Força"]]
        items = list(muscles_dict.items())
        for i in range(0, len(items), 2):
            l = items[i]
            r = items[i + 1] if i + 1 < len(items) else ("", "")
            rows.append([l[0], l[1] or "—", r[0], r[1] or "—"])

        t = Table(rows, colWidths=[W * 0.35, W * 0.15, W * 0.35, W * 0.15])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f5e8ea")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#9b1c2e")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#faf9f7")]),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#ddd9d0")),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        return t

    def test_table(tests_dict):
        """Tabela de testes."""
        rows = [["Teste", "Resultado", "Teste", "Resultado"]]
        items = list(tests_dict.items())
        for i in range(0, len(items), 2):
            l = items[i]
            r = items[i + 1] if i + 1 < len(items) else ("", "")
            rows.append([l[0], l[1] or "—", r[0], r[1] or "—"])

        t = Table(rows, colWidths=[W * 0.38, W * 0.12, W * 0.38, W * 0.12])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f5e8ea")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#9b1c2e")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 7.5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#faf9f7")]),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#ddd9d0")),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        return t

    # ── Reconstruir dicionários de exame físico a partir dos dados ──
    musculos_sup = {
        k.replace("forca_", "").replace("_", " ").title(): v
        for k, v in data.items()
        if k.startswith("forca_") and v
    }
    reflexos = {
        k.replace("reflexo_", "").replace("_", " ").title(): v
        for k, v in data.items()
        if k.startswith("reflexo_") and v
    }
    testes = {
        k.replace("teste_", "").replace("_", " ").title(): v
        for k, v in data.items()
        if k.startswith("teste_") and v
    }
    sensibilidade = {
        k.replace("sens_", "").replace("_", " ").title(): v
        for k, v in data.items()
        if k.startswith("sens_") and v
    }
    gatilhos = {
        k.replace("gatilho_", "").replace("_", " ").title(): v
        for k, v in data.items()
        if k.startswith("gatilho_") and v
    }

    # ── Montagem do documento ──
    story = []

    # Cabeçalho
    story += [
        Paragraph("GRUPO DE DOR · HC-FMUSP", style_title),
        Paragraph("Anamnese Padronizada de Dor", style_subtitle),
        Paragraph(
            f"Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
            style_small
        ),
        HRFlowable(width=W, thickness=1.5, color=colors.HexColor("#9b1c2e"), spaceAfter=8),
    ]

    # 1. Identificação
    story += section("01 · Identificação")
    story += two_col([
        ("Nome", data.get("nome")),
        ("Data", data.get("data")),
        ("Estado civil", data.get("estado_civil")),
        ("Escolaridade", data.get("escolaridade")),
        ("Mora em", data.get("mora_em")),
        ("Trabalho", data.get("trabalho")),
        ("Alergias", data.get("alergias")),
        ("Cirurgias prévias", data.get("cirurgias")),
    ])
    story += field("Antecedentes patológicos", data.get("antecedentes"))
    story += field("Medicamentos em uso contínuo (MUC)", data.get("muc"))

    # 2. HMA
    story += section("02 · História da Moléstia Atual")
    story += two_col([
        ("Encaminhamento", data.get("encaminhamento")),
        ("Tempo de dor", data.get("tempo_dor")),
    ])
    story += field("Queixa principal", data.get("queixa"))

    # 3. Localização
    story += section("03 · Localização da Dor")
    story += field("Regiões marcadas no mapa corporal", data.get("regioes_dor"))

    # 4. Caracterização
    story += section("04 · Caracterização da Dor")
    story += two_col([
        ("Qualidade da dor", data.get("qualidade_dor")),
        ("Componente emocional", data.get("componente_emocional")),
        (f"VAS ({data.get('vas', '?')}/10)", f"{'█' * int(data.get('vas') or 0)}{'░' * (10 - int(data.get('vas') or 0))}  {data.get('vas', '?')}/10"),
        ("Frequência", data.get("frequencia")),
        ("Predomínio", data.get("predominio")),
        ("Instalação", data.get("instalacao")),
    ])
    story += field("Fatores de melhora", data.get("fatores_melhora"))
    story += field("Fatores de piora", data.get("fatores_piora"))
    story += field("Tratamentos anteriores", data.get("tratamentos_anteriores"))
    story += field("Medicamentos para dor", data.get("medicamentos_dor"))

    red_flags = data.get("red_flags", "")
    if red_flags:
        story += [
            Paragraph("⚠ RED FLAGS", ParagraphStyle("RF", fontName="Helvetica-Bold", fontSize=9,
                       textColor=colors.HexColor("#c0392b"), spaceAfter=2)),
            Paragraph(red_flags, style_field_value),
        ]

    # 5. Sono
    story += section("05 · Sono")
    story += two_col([
        ("Percepção", data.get("percepcao_sono")),
        ("Horas/noite", data.get("horas_sono")),
        ("Medicamento p/ dormir", data.get("med_sono")),
        ("Posição", data.get("posicao_dormir")),
        ("Travesseiro auxiliar", data.get("travesseiro_aux")),
        ("Altura do travesseiro", data.get("altura_travesseiro")),
        ("Colchão", data.get("colchao")),
        ("Características", data.get("caracteristicas_sono")),
    ])

    # 6. Hábitos
    story += section("06 · Hábitos")
    story += two_col([
        ("Café da manhã", data.get("cafe")),
        ("Almoço", data.get("almoco")),
        ("Jantar", data.get("jantar")),
        ("Intestino", data.get("intestino")),
        ("Atividade física", data.get("atividade_fisica")),
        ("Humor", data.get("humor")),
    ])

    # 7. Exame Físico
    story += section("07 · Exame Físico")
    story += field("Inspeção geral", data.get("inspecao"))
    story += two_col([
        ("Comportamentos dolorosos", data.get("comportamentos_dolorosos")),
        ("Marcha", f"{data.get('marcha', '')} — {data.get('marcha_desc', '')}"),
        ("Equilíbrio", data.get("equilibrio")),
        ("Tônus", data.get("tonus")),
        ("Horner", data.get("horner")),
        ("Reflexos superficiais", data.get("reflexos_superficiais")),
    ])

    # Força muscular
    if musculos_sup:
        story.append(Paragraph("Força Muscular", style_field_label))
        story.append(Spacer(1, 4))
        story.append(muscle_table(musculos_sup))
        story.append(Spacer(1, 8))

    # Reflexos
    if reflexos:
        story.append(Paragraph("Reflexos Miotáticos", style_field_label))
        story.append(Spacer(1, 4))
        story.append(test_table(reflexos))
        story.append(Spacer(1, 8))

    # 8. Testes Específicos
    if testes:
        story += section("08 · Testes Específicos")
        story.append(test_table(testes))
        story.append(Spacer(1, 8))

    # 9. Sensibilidade
    if sensibilidade:
        story += section("09 · Sensibilidade Superficial")
        story.append(test_table(sensibilidade))
        story.append(Spacer(1, 8))

    # 10. Pontos-Gatilho
    if gatilhos:
        story += section("10 · Pontos-Gatilho Positivos")
        positivos = [k for k, v in gatilhos.items() if v == "Presente"]
        if positivos:
            story.append(Paragraph(", ".join(positivos), style_field_value))

    # 11. Exames Complementares
    story += section("11 · Exames Complementares")
    story += field("", data.get("exames_complementares"))

    # Rodapé
    story += [
        Spacer(1, 16),
        HRFlowable(width=W, thickness=0.5, color=colors.HexColor("#ddd9d0"), spaceAfter=6),
        Paragraph(
            f"Documento gerado automaticamente · Grupo de Dor HC-FMUSP · {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            ParagraphStyle("Footer", fontName="Helvetica", fontSize=7,
                           textColor=colors.HexColor("#9a9490"), alignment=TA_CENTER)
        ),
    ]

    doc.build(story)


# ─── HEALTH CHECK ──────────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}
