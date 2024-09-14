from generation.src.generator.utils import genitive


async def get_html(
    date: str,
    number: str,
    place: str,
    party_1: str,
    name_1: str,
    position_1: str,
    party_2: str,
    name_2: str,
    position_2: str,
    editor_generation: str,
):
    html_str = (
        f"""<html>

        <head>
        <meta http-equiv=Content-Type content="text/html; charset=utf-8">
        <meta name=Generator content="Microsoft Word 15 (filtered)">
        <style>
        <!--
        /* Font Definitions */
        @font-face
            {{font-family:"Cambria Math";
            panose-1:2 4 5 3 5 4 6 3 2 4;}}
        @font-face
            {{font-family:Calibri;
            panose-1:2 15 5 2 2 2 4 3 2 4;}}
        @font-face
            {{font-family:Georgia;
            panose-1:2 4 5 2 5 4 5 2 3 3;}}
        @font-face
            {{font-family:Cambria;
            panose-1:2 4 5 3 5 4 6 3 2 4;}}
        @font-face
            {{font-family:Tahoma;
            panose-1:2 11 6 4 3 5 4 4 2 4;}}
        @font-face
            {{font-family:"MS Sans Serif";
            panose-1:0 0 0 0 0 0 0 0 0 0;}}
        @font-face
            {{font-family:TimesNewRomanPSMT;
            panose-1:0 0 0 0 0 0 0 0 0 0;}}
        /* Style Definitions */
        p.MsoNormal, li.MsoNormal, div.MsoNormal
            {{margin:0in;
            font-size:10.0pt;
            font-family:"Times New Roman",serif;}}
        .MsoChpDefault
            {{font-size:10.0pt;}}
        /* Page Definitions */
        @page WordSection1
            {{size:595.3pt 841.9pt;
            margin:56.7pt 28.35pt 56.7pt 56.7pt;}}
        div.WordSection1
            {{page:WordSection1;}}
        /* List Definitions */
        ol
            {{margin-bottom:0in;}}
        ul
            {{margin-bottom:0in;}}
        -->
        </style>

        </head>

        <body lang=EN-US style='word-wrap:break-word'>

        <div class=WordSection1>

        <p class=MsoNormal align=center style='text-align:center;text-indent:35.45pt;
        border:none'><b><span lang=RU style='font-size:12.0pt;color:black'>Дополнительное
        соглашение №1</span></b></p>

        <p class=MsoNormal align=center style='text-align:center;text-indent:35.45pt;
        border:none'><b><span lang=RU style='font-size:12.0pt;color:black'>к договору от {date} № {number}</span></b></p>

        <p class=MsoNormal align=center style='text-align:center;text-indent:35.45pt;
        border:none'><span lang=RU style='font-size:12.0pt;color:black'>&nbsp;</span></p>

        <p class=MsoNormal style='display: flex; text-align:justify;border:none'><span lang=RU
        style='font-size:12.0pt;color:black'>{place}</span><span style=" display: inline-block; margin-left: auto;">{date}</span></p>

        <p class=MsoNormal style='text-align:justify;text-indent:35.45pt;border:none'><span
        lang=RU style='font-size:12.0pt;color:black'>&nbsp;</span></p>

        <p class=MsoNormal style='text-align:justify;text-indent:35.45pt;border:none'><b><span
        lang=RU style='font-size:12.0pt;color:black'>{party_1}</span></b><span lang=RU
        style='font-size:12.0pt;color:black'>, в лице {genitive(position_1)} {genitive(name_1)}, действующего на основании ____________, именуемое в дальнейшем «<b>Заказчик</b>», с одной стороны, и </span></p>

        <p class=MsoNormal style='text-align:justify;text-indent:35.45pt;border:none'><b><span
        lang=RU style='font-size:12.0pt;color:black'>{party_2}</span></b><span lang=RU style='font-size:
        12.0pt;color:black'>, именуемое в дальнейшем<b> «Исполнитель», </b>в лице {genitive(position_2)} {genitive(name_2)}, действующего на основании ____________, с другой
        стороны, вместе именуемые «Стороны» и каждый в отдельности «Сторона»,<b> </b>заключили
        настоящее Дополнительное соглашение к договору от {date} № {number} (далее – Договор) о нижеследующем:</span></p>

        <p class=MsoNormal style='margin-left:0in;text-align:justify;text-indent:35.45pt;
        border:none'><span lang=RU style='font-size:12.0pt;color:black'>1.<span
        style='font:7.0pt "Times New Roman"'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        </span></span><span lang=RU style='font-size:12.0pt;color:black'>Стороны приняли решение о внесении следующих изменений в условия Договора:</span></p>"""
        + "\n\n".join(
            [
                f"<p class=MsoNormal style='margin-left:0in;text-align:justify;text-indent:35.45pt; border:none'><span lang=RU style='font-size:12.0pt'>{p}</span></p>"
                for p in editor_generation.split("\n")
            ]
        )
        + f"""<p class=MsoNormal style='margin-left:0in;text-align:justify;text-indent:35.45pt;
        border:none'><span lang=RU style='font-size:12.0pt;color:black'>2.<span
        style='font:7.0pt "Times New Roman"'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        </span></span><span lang=RU style='font-size:12.0pt;color:black'>Настоящее
        Дополнительное соглашение № 1 является неотъемлемой частью Договора.</span></p>

        <p class=MsoNormal style='margin-left:0in;text-align:justify;text-indent:35.45pt;
        border:none'><span lang=RU style='font-size:12.0pt;color:black'>3.<span
        style='font:7.0pt "Times New Roman"'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        </span></span><span lang=RU style='font-size:12.0pt;color:black'>Настоящее
        Дополнительное соглашение № 1 считается заключенным и вступает в силу с даты его подписания Сторонами и действует до полного исполнения
        Сторонами своих обязательств.</span></p>

        <p class=MsoNormal style='margin-left:0in;text-align:justify;text-indent:35.45pt;
        border:none'><span lang=RU style='font-size:12.0pt;color:black'>4.<span
        style='font:7.0pt "Times New Roman"'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        </span></span><span lang=RU style='font-size:12.0pt;color:black'>По всем иным
        вопросам, не затронутым в настоящем Дополнительном соглашении № 1, Стороны
        руководствуются условиями Договора и действующим законодательством РФ.</span></p>

        <p class=MsoNormal style='margin-left:0in;text-align:justify;text-indent:35.45pt;
        border:none'><span lang=RU style='font-size:12.0pt;color:black'>5.<span
        style='font:7.0pt "Times New Roman"'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        </span></span><span lang=RU style='font-size:12.0pt;color:black'>Подписи
        Сторон:</span></p>

        <p class=MsoNormal style='margin-left:35.45pt;text-align:justify;border:none'><span
        lang=RU style='font-size:12.0pt;color:black'>&nbsp;</span></p>

        <div align=center>

        <table class=1 border=0 cellspacing=0 cellpadding=0 width=624 style='border-collapse:
        collapse'>
        <tr style='height:176.95pt'>
        <td width=338 valign=top style='width:253.4pt;padding:0in 4.2pt 0in 4.2pt;
        height:176.95pt'>
        <p class=MsoNormal style='border:none'><b><span lang=RU style='font-size:
        12.0pt;color:black'>Заказчик:</span></b></p>
        <p class=MsoNormal style='margin-right:10.0pt;border:none'><span lang=RU
        style='font-size:12.0pt;color:black'>{party_1}<b> </b></span></p>
        <p class=MsoNormal style='margin-right:10.0pt;border:none'><span lang=RU
        style='font-size:12.0pt;color:black'>&nbsp;</span></p>
        <p class=MsoNormal style='margin-right:10.0pt;border:none'><b><span lang=RU
        style='font-size:12.0pt;color:black'>{position_1.capitalize()}</span></b></p>
        <p class=MsoNormal style='margin-right:10.0pt;border:none'><span lang=RU
        style='font-size:12.0pt;color:black'>&nbsp;</span></p>
        <p class=MsoNormal style='margin-right:10.0pt;border:none'><span lang=RU
        style='font-size:12.0pt;color:black'>&nbsp;</span></p>
        <p class=MsoNormal style='margin-right:10.0pt;border:none'><b><span lang=RU
        style='font-size:12.0pt;color:black'>_____________/ {name_1.split(' ')[0]}</span></b></p>
        <p class=MsoNormal style='margin-right:10.0pt;border:none'><b><span lang=RU
        style='font-size:12.0pt;color:black'>М.П.</span></b></p>
        <p class=MsoNormal style='margin-right:24.1pt;border:none'><span lang=RU
        style='font-size:12.0pt;color:black'>&nbsp;</span></p>
        </td>
        <td width=286 valign=top style='width:214.7pt;padding:0in 4.2pt 0in 4.2pt;
        height:176.95pt'>
        <p class=MsoNormal style='margin-right:24.1pt;border:none'><b><span lang=RU
        style='font-size:12.0pt;color:black'>Поставщик</span></b><span lang=RU
        style='font-size:12.0pt;color:black'>:</span></p>
        <p class=MsoNormal style='margin-right:10.0pt;border:none'><span lang=RU
        style='font-size:12.0pt;color:black'>{party_2}</span></p>
        <p class=MsoNormal style='margin-right:10.0pt;border:none'><span lang=RU
        style='font-size:12.0pt;color:black'>&nbsp;</span></p>
        <p class=MsoNormal style='margin-right:10.0pt;border:none'><b><span lang=RU
        style='font-size:12.0pt;color:black'>{position_2.capitalize()}</span></b></p>
        <p class=MsoNormal style='margin-right:10.0pt;border:none'><span lang=RU
        style='font-size:12.0pt;color:black'>&nbsp;</span></p>
        <p class=MsoNormal style='margin-right:10.0pt;border:none'><span lang=RU
        style='font-size:12.0pt;color:black'>&nbsp;</span></p>
        <p class=MsoNormal style='margin-right:10.0pt;border:none'><span lang=RU
        style='font-size:12.0pt;color:black'>&nbsp;</span></p>
        <p class=MsoNormal style='margin-right:10.0pt;border:none'><b><span lang=RU
        style='font-size:12.0pt;color:black'> _____________/ {name_2.split(' ')[0]}</span></b></p>
        <p class=MsoNormal style='margin-right:24.1pt;border:none'><b><span lang=RU
        style='font-size:12.0pt;color:black'>  М.П.</span></b></p>
        <p class=MsoNormal style='margin-right:24.1pt;border:none'><span lang=RU
        style='font-size:12.0pt;color:black'>&nbsp;</span></p>
        </td>
        </tr>
        </table>

        </div>

        <p class=MsoNormal style='border:none'><span lang=RU style='font-size:12.0pt;
        color:black'>&nbsp;</span></p>

        </div>

        </body>

        </html>
        """
    )

    return html_str
